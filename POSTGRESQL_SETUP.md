# 🐘 PostgreSQL Setup Guide for Railway

## ✅ What We've Done

Your app now supports **both SQLite and PostgreSQL**:

- **Local development:** Uses SQLite (`taskflow.db`)
- **Railway production:** Uses PostgreSQL (persistent storage)

### Files Updated:

1. ✅ `requirements.txt` - Added `psycopg2-binary==2.9.9`
2. ✅ `app.py` - Updated to support both databases

---

## 🚀 Railway Deployment Steps

### **Step 1: Push Updated Code to GitHub**

```bash
# Make sure you're in the correct directory
cd taskflow-final

# Add all changes
git add .

# Commit
git commit -m "Add PostgreSQL support for production"

# Push to GitHub
git push origin main
```

---

### **Step 2: Add PostgreSQL Database on Railway**

1. **Go to Railway Dashboard:** https://railway.app

2. **Open your TaskFlow project**

3. **Add PostgreSQL:**
   - Click "**New**" button (top right)
   - Select "**Database**"
   - Choose "**PostgreSQL**"
   - Railway will create a PostgreSQL database

4. **Wait for provisioning** (takes ~30 seconds)

---

### **Step 3: Connect Database to Your App**

Railway automatically provides the `DATABASE_URL` environment variable!

**Verify the connection:**

1. Click on your **TaskFlow service** (not the database)
2. Go to "**Variables**" tab
3. You should see `DATABASE_URL` automatically added
4. It looks like: `postgresql://user:pass@host:port/dbname`

**If you don't see it:**
1. Click on the **PostgreSQL database**
2. Go to "**Variables**" tab
3. Copy the `DATABASE_URL` value
4. Go back to your **TaskFlow service**
5. Go to "**Variables**" tab
6. Click "**New Variable**"
7. Key: `DATABASE_URL`
8. Value: Paste the copied URL
9. Click "**Add**"

---

### **Step 4: Redeploy Your App**

Railway will automatically redeploy when you push to GitHub, but you can also:

1. Go to your TaskFlow service
2. Click "**Deploy**" button
3. Or go to "**Deployments**" tab → Click "**Redeploy**"

---

### **Step 5: Watch the Build Logs**

Click on the latest deployment to see logs:

```
✓ Detected Python application
✓ Installing dependencies...
✓ psycopg2-binary==2.9.9 installed
✓ Starting application...
🌱 Seeding demo data...
✅ Seed complete
🚀 TaskFlow running on http://0.0.0.0:3000
```

---

### **Step 6: Test Your App**

1. **Open your Railway URL**
2. **Login with demo account:**
   - Email: `admin@taskflow.com`
   - Password: `password123`

3. **Create a new user:**
   - Click "Sign Up"
   - Create account: `test@example.com` / `password123`

4. **Test persistence:**
   - Create a project
   - Create some tasks
   - **Redeploy the app** (Railway → Deployments → Redeploy)
   - **Login again** - Your data should still be there! 🎉

---

## 🔍 How It Works

### **Automatic Database Detection:**

```python
# In app.py
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    # Use PostgreSQL
    import psycopg2
else:
    # Use SQLite
    import sqlite3
```

### **Local Development (SQLite):**
```bash
# No DATABASE_URL environment variable
python app.py
# → Uses SQLite (taskflow.db)
```

### **Railway Production (PostgreSQL):**
```bash
# DATABASE_URL is set by Railway
# → Uses PostgreSQL (persistent)
```

---

## ✅ Benefits of PostgreSQL

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Persistence** | ❌ Resets on Railway | ✅ Permanent storage |
| **Concurrent Users** | ⚠️ Limited | ✅ Excellent |
| **Production Ready** | ❌ Not recommended | ✅ Industry standard |
| **Scalability** | ❌ Single file | ✅ Highly scalable |
| **Data Safety** | ⚠️ Can be lost | ✅ Backed up |

---

## 🧪 Testing Checklist

After deployment, test these:

- [ ] ✅ App loads successfully
- [ ] ✅ Demo accounts work (admin@taskflow.com)
- [ ] ✅ Can create new user account
- [ ] ✅ Can create projects
- [ ] ✅ Can create tasks
- [ ] ✅ **Redeploy app** (Railway dashboard)
- [ ] ✅ **Login again** - data still exists!
- [ ] ✅ New signups persist across restarts

---

## 🆘 Troubleshooting

### **Problem: "relation does not exist" error**

**Solution:** Database tables not created. Check logs for:
```
🌱 Seeding demo data...
✅ Seed complete
```

If missing, redeploy the app.

---

### **Problem: Can't connect to database**

**Solution:** Verify `DATABASE_URL` is set:

1. Railway → Your service → Variables
2. Check `DATABASE_URL` exists
3. Value should start with `postgresql://`

---

### **Problem: "psycopg2" import error**

**Solution:** Ensure `psycopg2-binary` is in requirements.txt:

```txt
psycopg2-binary==2.9.9
```

Then redeploy.

---

### **Problem: Data still resets on restart**

**Solution:** Verify PostgreSQL is being used:

1. Check Railway logs for: `Using PostgreSQL database`
2. Verify `DATABASE_URL` environment variable exists
3. Check that PostgreSQL service is running

---

## 📊 Database Management

### **View Database Contents:**

1. Railway → PostgreSQL service
2. Click "**Data**" tab
3. Browse tables: users, projects, tasks, etc.

### **Run SQL Queries:**

1. Railway → PostgreSQL service
2. Click "**Query**" tab
3. Run queries:

```sql
-- View all users
SELECT id, name, email, role FROM users;

-- View all projects
SELECT id, name, owner_id FROM projects;

-- Count tasks
SELECT COUNT(*) FROM tasks;
```

---

## 🎯 Success Indicators

You'll know PostgreSQL is working when:

✅ Railway logs show "Using PostgreSQL database"
✅ Can create new user accounts
✅ Data persists after redeployment
✅ Multiple users can use the app simultaneously
✅ No "database locked" errors

---

## 📝 Summary

**What changed:**

1. ✅ Added PostgreSQL support to `app.py`
2. ✅ Added `psycopg2-binary` to `requirements.txt`
3. ✅ App auto-detects database type
4. ✅ Local: SQLite, Production: PostgreSQL

**What to do:**

1. ✅ Push code to GitHub
2. ✅ Add PostgreSQL on Railway
3. ✅ Verify `DATABASE_URL` is set
4. ✅ Redeploy and test

**Result:**

🎉 **Permanent data storage on Railway!**

---

## 🚀 Next Steps

After PostgreSQL is working:

1. ✅ Update README with live URL
2. ✅ Record demo video
3. ✅ Submit assignment

**Your app is now production-ready!** 🎊
