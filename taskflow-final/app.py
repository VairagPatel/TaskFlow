import sqlite3
import bcrypt
import jwt
import os
import random
from datetime import datetime, timedelta, date
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

DB_PATH = os.environ.get('DB_PATH', 'taskflow.db')
JWT_SECRET = os.environ.get('JWT_SECRET', 'taskflow-secret-2024')
JWT_ALGO = 'HS256'

# ─── DB ────────────────────────────────────────────────────────────────────
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
        g.db.execute('PRAGMA journal_mode = WAL')
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    with app.app_context():
        db = sqlite3.connect(DB_PATH)
        db.execute('PRAGMA foreign_keys = ON')
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'member' CHECK(role IN ('admin','member')),
                avatar TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                color TEXT DEFAULT '#6366f1',
                owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS project_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                role TEXT NOT NULL DEFAULT 'member' CHECK(role IN ('admin','member')),
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(project_id, user_id)
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo','in_progress','review','done')),
                priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high','urgent')),
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                creator_id INTEGER NOT NULL REFERENCES users(id),
                due_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS task_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        db.commit()
        db.close()

def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ─── AUTH ────────────────────────────────────────────────────────────────────
def make_token(user_id):
    payload = {'id': user_id, 'exp': datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        token = auth[7:]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except Exception:
            return jsonify({'error': 'Invalid token'}), 401

        db = get_db()
        user = row_to_dict(db.execute(
            'SELECT id,name,email,role,avatar,created_at FROM users WHERE id=?', (payload['id'],)
        ).fetchone())
        if not user:
            return jsonify({'error': 'User not found'}), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated

def require_project_access(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        project_id = kwargs.get('project_id')
        if g.user['role'] == 'admin':
            g.project_role = 'admin'
            return f(*args, **kwargs)
        db = get_db()
        member = db.execute(
            'SELECT role FROM project_members WHERE project_id=? AND user_id=?',
            (project_id, g.user['id'])
        ).fetchone()
        if not member:
            return jsonify({'error': 'Not a project member'}), 403
        g.project_role = member['role']
        return f(*args, **kwargs)
    return decorated

def require_project_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.user['role'] == 'admin' or g.project_role == 'admin':
            return f(*args, **kwargs)
        return jsonify({'error': 'Project admin access required'}), 403
    return decorated

# ─── AUTH ROUTES ───────────────────────────────────────────────────────────
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    role = data.get('role', 'member')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400

    db = get_db()
    if db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone():
        return jsonify({'error': 'Email already registered'}), 409

    count = db.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
    user_role = 'admin' if count == 0 else role

    initials = ''.join(w[0] for w in name.split() if w).upper()[:2]
    colors = ['#6366f1','#ec4899','#f59e0b','#10b981','#3b82f6','#8b5cf6']
    avatar = f"{initials}|{random.choice(colors)}"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor = db.execute(
        'INSERT INTO users (name,email,password,role,avatar) VALUES (?,?,?,?,?)',
        (name, email, hashed, user_role, avatar)
    )
    db.commit()

    user = {'id': cursor.lastrowid, 'name': name, 'email': email, 'role': user_role, 'avatar': avatar}
    token = make_token(user['id'])
    return jsonify({'user': user, 'token': token}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    db = get_db()
    user = row_to_dict(db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone())
    if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = make_token(user['id'])
    user.pop('password', None)
    return jsonify({'user': user, 'token': token})

@app.route('/api/auth/me')
@authenticate
def me():
    return jsonify({'user': g.user})

@app.route('/api/auth/users')
@authenticate
def list_users():
    db = get_db()
    users = rows_to_list(db.execute('SELECT id,name,email,role,avatar FROM users ORDER BY name').fetchall())
    return jsonify({'users': users})

# ─── PROJECT ROUTES ─────────────────────────────────────────────────────────
@app.route('/api/projects')
@authenticate
def list_projects():
    db = get_db()
    if g.user['role'] == 'admin':
        rows = db.execute('''
            SELECT p.*, u.name as owner_name,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id) as task_count,
              (SELECT COUNT(*) FROM project_members WHERE project_id=p.id) as member_count,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id AND status='done') as done_count,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id AND due_date < date('now') AND status!='done') as overdue_count
            FROM projects p JOIN users u ON p.owner_id=u.id
            ORDER BY p.created_at DESC
        ''').fetchall()
    else:
        rows = db.execute('''
            SELECT p.*, u.name as owner_name, pm.role as my_role,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id) as task_count,
              (SELECT COUNT(*) FROM project_members WHERE project_id=p.id) as member_count,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id AND status='done') as done_count,
              (SELECT COUNT(*) FROM tasks WHERE project_id=p.id AND due_date < date('now') AND status!='done') as overdue_count
            FROM projects p
            JOIN users u ON p.owner_id=u.id
            JOIN project_members pm ON pm.project_id=p.id AND pm.user_id=?
            ORDER BY p.created_at DESC
        ''', (g.user['id'],)).fetchall()
    return jsonify({'projects': rows_to_list(rows)})

@app.route('/api/projects', methods=['POST'])
@authenticate
def create_project():
    data = request.json or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Project name is required'}), 400

    db = get_db()
    cursor = db.execute(
        'INSERT INTO projects (name,description,color,owner_id) VALUES (?,?,?,?)',
        (name, data.get('description',''), data.get('color','#6366f1'), g.user['id'])
    )
    pid = cursor.lastrowid
    db.execute('INSERT INTO project_members (project_id,user_id,role) VALUES (?,?,?)', (pid, g.user['id'], 'admin'))
    db.commit()
    project = row_to_dict(db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone())
    return jsonify({'project': project}), 201

@app.route('/api/projects/<int:project_id>')
@authenticate
@require_project_access
def get_project(project_id):
    db = get_db()
    project = row_to_dict(db.execute('''
        SELECT p.*, u.name as owner_name FROM projects p JOIN users u ON p.owner_id=u.id WHERE p.id=?
    ''', (project_id,)).fetchone())
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    members = rows_to_list(db.execute('''
        SELECT u.id,u.name,u.email,u.role as global_role,u.avatar,pm.role as project_role,pm.joined_at
        FROM project_members pm JOIN users u ON pm.user_id=u.id
        WHERE pm.project_id=? ORDER BY u.name
    ''', (project_id,)).fetchall())
    return jsonify({'project': project, 'members': members})

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@authenticate
@require_project_access
@require_project_admin
def update_project(project_id):
    data = request.json or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Project name is required'}), 400
    db = get_db()
    db.execute(
        "UPDATE projects SET name=?,description=?,color=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (name, data.get('description',''), data.get('color','#6366f1'), project_id)
    )
    db.commit()
    project = row_to_dict(db.execute('SELECT * FROM projects WHERE id=?', (project_id,)).fetchone())
    return jsonify({'project': project})

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@authenticate
@require_project_access
@require_project_admin
def delete_project(project_id):
    db = get_db()
    db.execute('DELETE FROM projects WHERE id=?', (project_id,))
    db.commit()
    return jsonify({'message': 'Project deleted'})

@app.route('/api/projects/<int:project_id>/members', methods=['POST'])
@authenticate
@require_project_access
@require_project_admin
def add_member(project_id):
    data = request.json or {}
    user_id = data.get('user_id')
    role = data.get('role', 'member')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    db = get_db()
    if not db.execute('SELECT id FROM users WHERE id=?', (user_id,)).fetchone():
        return jsonify({'error': 'User not found'}), 404
    try:
        db.execute('INSERT INTO project_members (project_id,user_id,role) VALUES (?,?,?)', (project_id, user_id, role))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already a member'}), 409
    return jsonify({'message': 'Member added'}), 201

@app.route('/api/projects/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@authenticate
@require_project_access
@require_project_admin
def remove_member(project_id, user_id):
    db = get_db()
    db.execute('DELETE FROM project_members WHERE project_id=? AND user_id=?', (project_id, user_id))
    db.commit()
    return jsonify({'message': 'Member removed'})

# ─── TASK ROUTES ─────────────────────────────────────────────────────────────
@app.route('/api/projects/<int:project_id>/tasks')
@authenticate
@require_project_access
def list_tasks(project_id):
    db = get_db()
    q = '''
        SELECT t.*, u.name as assignee_name, u.avatar as assignee_avatar, c.name as creator_name,
          CASE WHEN t.due_date < date('now') AND t.status!='done' THEN 1 ELSE 0 END as is_overdue
        FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id JOIN users c ON t.creator_id=c.id
        WHERE t.project_id=?
    '''
    params = [project_id]
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee_id = request.args.get('assignee_id')
    if status: q += ' AND t.status=?'; params.append(status)
    if priority: q += ' AND t.priority=?'; params.append(priority)
    if assignee_id: q += ' AND t.assignee_id=?'; params.append(assignee_id)
    q += " ORDER BY CASE t.priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END, t.due_date ASC NULLS LAST, t.created_at DESC"
    return jsonify({'tasks': rows_to_list(db.execute(q, params).fetchall())})

@app.route('/api/projects/<int:project_id>/tasks', methods=['POST'])
@authenticate
@require_project_access
def create_task(project_id):
    data = request.json or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Task title is required'}), 400

    assignee_id = data.get('assignee_id') or None
    db = get_db()
    cursor = db.execute('''
        INSERT INTO tasks (title,description,status,priority,project_id,assignee_id,creator_id,due_date)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (title, data.get('description',''), data.get('status','todo'),
          data.get('priority','medium'), project_id, assignee_id,
          g.user['id'], data.get('due_date') or None))
    db.commit()
    task = row_to_dict(db.execute('''
        SELECT t.*, u.name as assignee_name, u.avatar as assignee_avatar, c.name as creator_name
        FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id JOIN users c ON t.creator_id=c.id
        WHERE t.id=?
    ''', (cursor.lastrowid,)).fetchone())
    return jsonify({'task': task}), 201

@app.route('/api/projects/<int:project_id>/tasks/<int:task_id>')
@authenticate
@require_project_access
def get_task(project_id, task_id):
    db = get_db()
    task = row_to_dict(db.execute('''
        SELECT t.*, u.name as assignee_name, u.avatar as assignee_avatar, c.name as creator_name,
          CASE WHEN t.due_date < date('now') AND t.status!='done' THEN 1 ELSE 0 END as is_overdue
        FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id JOIN users c ON t.creator_id=c.id
        WHERE t.id=? AND t.project_id=?
    ''', (task_id, project_id)).fetchone())
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    comments = rows_to_list(db.execute('''
        SELECT tc.*, u.name as user_name, u.avatar as user_avatar
        FROM task_comments tc JOIN users u ON tc.user_id=u.id
        WHERE tc.task_id=? ORDER BY tc.created_at ASC
    ''', (task_id,)).fetchall())
    return jsonify({'task': task, 'comments': comments})

@app.route('/api/projects/<int:project_id>/tasks/<int:task_id>', methods=['PUT'])
@authenticate
@require_project_access
def update_task(project_id, task_id):
    db = get_db()
    task = row_to_dict(db.execute('SELECT * FROM tasks WHERE id=? AND project_id=?', (task_id, project_id)).fetchone())
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    is_proj_admin = g.user['role'] == 'admin' or g.project_role == 'admin'
    can_edit = is_proj_admin or task['creator_id'] == g.user['id'] or task['assignee_id'] == g.user['id']
    if not can_edit:
        return jsonify({'error': 'Cannot edit this task'}), 403

    data = request.json or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Task title is required'}), 400

    db.execute('''
        UPDATE tasks SET title=?,description=?,status=?,priority=?,assignee_id=?,due_date=?,
        updated_at=CURRENT_TIMESTAMP WHERE id=?
    ''', (title, data.get('description',''), data.get('status', task['status']),
          data.get('priority', task['priority']),
          data.get('assignee_id') or None,
          data.get('due_date') or None, task_id))
    db.commit()
    updated = row_to_dict(db.execute('''
        SELECT t.*, u.name as assignee_name, u.avatar as assignee_avatar, c.name as creator_name
        FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id JOIN users c ON t.creator_id=c.id
        WHERE t.id=?
    ''', (task_id,)).fetchone())
    return jsonify({'task': updated})

@app.route('/api/projects/<int:project_id>/tasks/<int:task_id>/status', methods=['PATCH'])
@authenticate
@require_project_access
def update_task_status(project_id, task_id):
    data = request.json or {}
    status = data.get('status')
    if status not in ('todo','in_progress','review','done'):
        return jsonify({'error': 'Invalid status'}), 400
    db = get_db()
    db.execute('UPDATE tasks SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=? AND project_id=?',
               (status, task_id, project_id))
    db.commit()
    return jsonify({'message': 'Status updated'})

@app.route('/api/projects/<int:project_id>/tasks/<int:task_id>', methods=['DELETE'])
@authenticate
@require_project_access
def delete_task(project_id, task_id):
    db = get_db()
    task = row_to_dict(db.execute('SELECT * FROM tasks WHERE id=? AND project_id=?', (task_id, project_id)).fetchone())
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    is_proj_admin = g.user['role'] == 'admin' or g.project_role == 'admin'
    if not is_proj_admin and task['creator_id'] != g.user['id']:
        return jsonify({'error': 'Cannot delete this task'}), 403
    db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    db.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/projects/<int:project_id>/tasks/<int:task_id>/comments', methods=['POST'])
@authenticate
@require_project_access
def add_comment(project_id, task_id):
    data = request.json or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400
    db = get_db()
    cursor = db.execute(
        'INSERT INTO task_comments (task_id,user_id,content) VALUES (?,?,?)',
        (task_id, g.user['id'], content)
    )
    db.commit()
    comment = row_to_dict(db.execute('''
        SELECT tc.*, u.name as user_name, u.avatar as user_avatar
        FROM task_comments tc JOIN users u ON tc.user_id=u.id WHERE tc.id=?
    ''', (cursor.lastrowid,)).fetchone())
    return jsonify({'comment': comment}), 201

# ─── DASHBOARD ─────────────────────────────────────────────────────────────
@app.route('/api/dashboard')
@authenticate
def dashboard():
    db = get_db()
    uid = g.user['id']
    is_admin = g.user['role'] == 'admin'

    if is_admin:
        proj_filter = ''
        proj_params = []
    else:
        proj_filter = 'AND p.id IN (SELECT project_id FROM project_members WHERE user_id=?)'
        proj_params = [uid]

    stats = row_to_dict(db.execute(f'''
        SELECT COUNT(*) as total,
          SUM(CASE WHEN status='todo' THEN 1 ELSE 0 END) as todo,
          SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) as in_progress,
          SUM(CASE WHEN status='review' THEN 1 ELSE 0 END) as review,
          SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) as done,
          SUM(CASE WHEN due_date < date('now') AND status!='done' THEN 1 ELSE 0 END) as overdue
        FROM tasks t JOIN projects p ON t.project_id=p.id WHERE 1=1 {proj_filter}
    ''', proj_params).fetchone())

    my_tasks = rows_to_list(db.execute('''
        SELECT t.*,p.name as project_name,p.color as project_color,
          CASE WHEN t.due_date < date('now') AND t.status!='done' THEN 1 ELSE 0 END as is_overdue
        FROM tasks t JOIN projects p ON t.project_id=p.id
        WHERE t.assignee_id=? AND t.status!='done'
        ORDER BY CASE t.priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END,
          t.due_date ASC NULLS LAST LIMIT 10
    ''', (uid,)).fetchall())

    recent_tasks = rows_to_list(db.execute(f'''
        SELECT t.*,p.name as project_name,p.color as project_color,u.name as assignee_name,
          CASE WHEN t.due_date < date('now') AND t.status!='done' THEN 1 ELSE 0 END as is_overdue
        FROM tasks t JOIN projects p ON t.project_id=p.id LEFT JOIN users u ON t.assignee_id=u.id
        WHERE 1=1 {proj_filter}
        ORDER BY t.updated_at DESC LIMIT 8
    ''', proj_params).fetchall())

    projects = rows_to_list(db.execute(f'''
        SELECT p.*,COUNT(t.id) as task_count,
          SUM(CASE WHEN t.status='done' THEN 1 ELSE 0 END) as done_count,
          SUM(CASE WHEN t.due_date < date('now') AND t.status!='done' THEN 1 ELSE 0 END) as overdue_count
        FROM projects p LEFT JOIN tasks t ON t.project_id=p.id
        WHERE 1=1 {proj_filter}
        GROUP BY p.id ORDER BY p.updated_at DESC LIMIT 6
    ''', proj_params).fetchall())

    overdue_proj_filter = proj_filter.replace('p.id IN', 't.project_id IN')
    overdue = rows_to_list(db.execute(f'''
        SELECT t.*,p.name as project_name,p.color as project_color,u.name as assignee_name
        FROM tasks t JOIN projects p ON t.project_id=p.id LEFT JOIN users u ON t.assignee_id=u.id
        WHERE t.due_date < date('now') AND t.status!='done' {overdue_proj_filter}
        ORDER BY t.due_date ASC LIMIT 5
    ''', proj_params).fetchall())

    return jsonify({'taskStats': stats, 'myTasks': my_tasks, 'recentTasks': recent_tasks,
                    'projects': projects, 'overdueTasks': overdue})

# ─── HEALTH ─────────────────────────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat()})

# ─── SPA FALLBACK ────────────────────────────────────────────────────────────
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def spa(path):
    return send_from_directory('static', 'index.html')

# ─── SEED ────────────────────────────────────────────────────────────────────
def seed_demo():
    with app.app_context():
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')

        count = db.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
        if count > 0:
            db.close()
            return

        print('🌱 Seeding demo data...')
        hash_pw = lambda p: bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

        users_data = [
            ('Alex Admin', 'admin@taskflow.com', hash_pw('password123'), 'admin', 'AA|#6366f1'),
            ('Sam Developer', 'sam@taskflow.com', hash_pw('password123'), 'member', 'SD|#10b981'),
            ('Jordan Designer', 'jordan@taskflow.com', hash_pw('password123'), 'member', 'JD|#ec4899'),
        ]
        for u in users_data:
            db.execute('INSERT OR IGNORE INTO users (name,email,password,role,avatar) VALUES (?,?,?,?,?)', u)
        db.commit()

        admin_id = db.execute("SELECT id FROM users WHERE email='admin@taskflow.com'").fetchone()['id']
        sam_id = db.execute("SELECT id FROM users WHERE email='sam@taskflow.com'").fetchone()['id']
        jordan_id = db.execute("SELECT id FROM users WHERE email='jordan@taskflow.com'").fetchone()['id']

        p1 = db.execute('INSERT INTO projects (name,description,color,owner_id) VALUES (?,?,?,?)',
            ('Website Redesign', 'Complete redesign of the company website with modern stack', '#6366f1', admin_id)
        ).lastrowid
        p2 = db.execute('INSERT INTO projects (name,description,color,owner_id) VALUES (?,?,?,?)',
            ('Mobile App v2.0', 'New version of the mobile app with improved UX', '#ec4899', admin_id)
        ).lastrowid
        db.commit()

        for pid, uid, role in [(p1,admin_id,'admin'),(p1,sam_id,'member'),(p1,jordan_id,'member'),
                                (p2,admin_id,'admin'),(p2,jordan_id,'admin')]:
            db.execute('INSERT OR IGNORE INTO project_members (project_id,user_id,role) VALUES (?,?,?)', (pid,uid,role))

        from datetime import date, timedelta
        today = date.today()
        tasks = [
            ('Design new homepage wireframes','Create wireframes for all key sections','done','high',p1,jordan_id,admin_id,str(today-timedelta(2))),
            ('Implement hero section','Build hero section with animations','in_progress','high',p1,sam_id,admin_id,str(today+timedelta(5))),
            ('Write API documentation','Document all REST endpoints','todo','medium',p1,sam_id,admin_id,str(today+timedelta(10))),
            ('Fix navigation bug on mobile','Hamburger menu broken on iOS Safari','review','urgent',p1,jordan_id,admin_id,str(today-timedelta(1))),
            ('SEO optimization','Add meta tags, sitemap, structured data','todo','low',p1,None,sam_id,str(today+timedelta(14))),
            ('User onboarding flow redesign','Redesign the 3-step onboarding','in_progress','high',p2,jordan_id,admin_id,str(today-timedelta(3))),
            ('Push notifications setup','Integrate Firebase for push notifications','todo','urgent',p2,None,admin_id,None),
            ('Dark mode implementation','Add system-level dark mode support','todo','medium',p2,sam_id,jordan_id,str(today+timedelta(7))),
        ]
        for t in tasks:
            db.execute('INSERT INTO tasks (title,description,status,priority,project_id,assignee_id,creator_id,due_date) VALUES (?,?,?,?,?,?,?,?)', t)

        db.commit()
        db.close()
        print('✅ Seed complete')

if __name__ == '__main__':
    init_db()
    seed_demo()
    port = int(os.environ.get('PORT', 3000))
    print(f'🚀 TaskFlow running on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=False)
