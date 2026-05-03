# TaskFlow — Team Task Manager

A full-stack team task management web app with role-based access control, built with **Python Flask + SQLite + Vanilla JS**.

---

## 🚀 Live Demo

> Deploy to Railway and paste your URL here.

**Demo credentials:**
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@taskflow.com | password123 |
| Member | sam@taskflow.com | password123 |
| Member | jordan@taskflow.com | password123 |

---

## ✨ Features

### Authentication
- JWT-based signup/login with 7-day tokens
- Password hashing with bcrypt
- Auto-assign admin role to the first registered user

### Role-Based Access Control (RBAC)
| Action | System Admin | Project Admin | Member |
|--------|-------------|---------------|--------|
| View all projects | ✅ | ❌ | ❌ |
| Create projects | ✅ | ✅ | ✅ |
| Edit/Delete project | ✅ | ✅ (own) | ❌ |
| Manage members | ✅ | ✅ | ❌ |
| Create tasks | ✅ | ✅ | ✅ |
| Edit any task | ✅ | ✅ | Own/Assigned only |
| Delete any task | ✅ | ✅ | Own only |

### Projects
- Create projects with name, description, color
- Add/remove team members with per-project roles (admin/member)
- Progress tracking (% completed)
- Overdue task count per project

### Tasks
- Create, update, delete tasks
- Statuses: `todo` → `in_progress` → `review` → `done`
- Priorities: `low`, `medium`, `high`, `urgent`
- Assign to project members
- Due dates with overdue detection
- Comments on tasks
- Board view (Kanban) and List view
- Filter by status and priority
- Quick status update from list view

### Dashboard
- Task stats: Total, In Progress, In Review, Done, Overdue
- My Tasks (assigned to me, sorted by priority)
- Overdue Tasks alert panel
- Recent Activity feed

---

## 🏗️ Architecture

```
taskflow/
├── app.py              # Flask app — all routes & DB logic
├── static/
│   └── index.html      # Single-page frontend (HTML + CSS + JS)
├── requirements.txt
├── Procfile
├── railway.toml
└── README.md
```

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask |
| Database | SQLite (via stdlib `sqlite3`) |
| Auth | JWT (PyJWT) + bcrypt |
| Frontend | Vanilla JS SPA (no framework) |
| Deployment | Railway |

### Database Schema
```sql
users            -- id, name, email, password, role, avatar
projects         -- id, name, description, color, owner_id
project_members  -- project_id, user_id, role (admin/member)
tasks            -- id, title, description, status, priority,
                 --   project_id, assignee_id, creator_id, due_date
task_comments    -- task_id, user_id, content
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd taskflow

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
# → http://localhost:3000
```

The app auto-creates the SQLite database and seeds demo data on first run.

---

## 🌐 Deploy to Railway

### Method 1: GitHub (Recommended)
1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select your repo → Railway auto-detects Python
4. Set environment variables (optional):
   ```
   JWT_SECRET=your-secure-random-string
   DB_PATH=/data/taskflow.db
   ```
5. Done! Railway gives you a live URL.

### Method 2: Railway CLI
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Server port (Railway sets this automatically) |
| `JWT_SECRET` | `taskflow-secret-2024` | Secret for JWT signing — **change in production!** |
| `DB_PATH` | `taskflow.db` | SQLite database path |

> **Note on SQLite in Railway:** Railway's filesystem is ephemeral. For production persistence, either use Railway's Volume feature (mount at `/data`) and set `DB_PATH=/data/taskflow.db`, or swap SQLite for PostgreSQL using `psycopg2`.

---

## 🔌 REST API Reference

### Auth
```
POST /api/auth/signup    Body: {name, email, password, role}
POST /api/auth/login     Body: {email, password}
GET  /api/auth/me        → current user
GET  /api/auth/users     → all users list
```

### Projects
```
GET    /api/projects               → list (filtered by access)
POST   /api/projects               Body: {name, description, color}
GET    /api/projects/:id
PUT    /api/projects/:id           Body: {name, description, color}
DELETE /api/projects/:id
POST   /api/projects/:id/members   Body: {user_id, role}
DELETE /api/projects/:id/members/:userId
```

### Tasks
```
GET    /api/projects/:pid/tasks           ?status=&priority=&assignee_id=
POST   /api/projects/:pid/tasks           Body: {title, description, status, priority, assignee_id, due_date}
GET    /api/projects/:pid/tasks/:id
PUT    /api/projects/:pid/tasks/:id
PATCH  /api/projects/:pid/tasks/:id/status   Body: {status}
DELETE /api/projects/:pid/tasks/:id
POST   /api/projects/:pid/tasks/:id/comments  Body: {content}
```

### Dashboard
```
GET /api/dashboard    → stats, myTasks, recentTasks, projects, overdueTasks
```

---

## 🎨 UI Highlights

- **Dark industrial aesthetic** with Space Mono + DM Sans typography
- **Kanban board** view with 4 columns (Todo / In Progress / Review / Done)
- **List view** with inline status updates
- **Overdue indicators** — red dots on task cards, highlighted rows
- **Progress bars** on project cards
- **Toast notifications** for all actions
- **Modal forms** for create/edit with validation
- **Task detail panel** with comments thread
- **Responsive sidebar** with project navigator

---

## 📁 Project Structure Details

```
app.py
├── init_db()        — creates all tables
├── seed_demo()      — seeds 3 users, 2 projects, 8 tasks
├── Auth middleware  — @authenticate, @require_project_access, @require_project_admin
├── /api/auth/*      — signup, login, me, users
├── /api/projects/*  — CRUD + member management
├── /api/projects/:id/tasks/*  — CRUD + comments + status patch
└── /api/dashboard   — aggregated stats

static/index.html
├── CSS variables    — design tokens, dark theme
├── Auth page        — login/signup with tab switch
├── Sidebar          — nav + project list + user profile
├── Dashboard page   — stats cards, my tasks, overdue, recent
├── Projects page    — project cards grid
├── Project detail   — Kanban board + list view + filters
├── My Tasks page    — cross-project task list
└── Modals           — create/edit project, create/edit task, members
```
