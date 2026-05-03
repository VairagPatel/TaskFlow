# 🔧 Troubleshooting 500 Error on Signup

## ❌ Error You're Seeing

```
/api/auth/signup: 500 (Internal Server Error)
/api/auth/login: 401 (Unauthorized)
/api/auth/me: 401 (Unauthorized)
```

## 🔍 Root Cause

The 500 error on signup means the database isn't working. This could be:

1. **PostgreSQL not connected** - DATABASE_URL not set or incorrect
2. **Tables not created** - Database exists but tables missing
3. **psycopg2 not installed** - Missing PostgreSQL driver

---

## ✅ **Solution 1: Check Railway Logs**

### **Step 1: View Logs**

1. Go to Railway dashboard
2. Click your TaskFlow service
3. Click "**View Logs**" or "**Deployments**" → Latest deployment
4. Look for these messages:

**Good (PostgreSQL working):**
```
✓ Using PostgreSQL database
🌱 Seeding demo data...
✅ Seed complete
```

**Bad (PostgreSQL not working):**
```
✗ psycopg2 not installed, falling back to SQLite
✓ Using SQLite database
```

**Bad (Connection error):**
```
Error: could not connect to server
psycopg2.OperationalError
```

---

## ✅ **Solution 2: Verify PostgreSQL Setup**

### **Check 1: PostgreSQL Service Exists**

1. Railway dashboard
2. Your project should have **2 services**:
   - TaskFlow (your app)
   - PostgreSQL (database)

**If you only see TaskFlow:**
- Click "**New**" → "**Database**" → "**PostgreSQL**"
- Wait for provisioning

### **Check 2: DATABASE_URL Variable**

1. Click **TaskFlow service** (not PostgreSQL)
2. Go to "**Variables**" tab
3. Look for `DATABASE_URL`

**If missing:**
1. Click PostgreSQL service
2. Go to "**Variables**" tab
3. Copy the `DATABASE_URL` value
4. Go back to TaskFlow service
5. "**Variables**" → "**New Variable**"
6. Key: `DATABASE_URL`
7. Value: Paste the URL
8. Click "**Add**"

### **Check 3: DATABASE_URL Format**

The URL should look like:
```
postgresql://user:password@host:port/database
```

**If it starts with `postgres://`:**
- That's fine, the app auto-converts it

---

## ✅ **Solution 3: Force Redeploy**

Sometimes Railway needs a fresh deployment:

1. Railway → Your TaskFlow service
2. Go to "**Settings**" tab
3. Scroll to "**Danger Zone**"
4. Click "**Redeploy**"
5. Watch the logs

---

## ✅ **Solution 4: Use SQLite Temporarily**

If PostgreSQL is causing issues, you can use SQLite temporarily:

### **Remove DATABASE_URL:**

1. Railway → TaskFlow service
2. "**Variables**" tab
3. Find `DATABASE_URL`
4. Click "**...**" → "**Remove**"
5. App will redeploy and use SQLite

**Note:** Data will reset on restarts, but the app will work!

---

## ✅ **Solution 5: Check requirements.txt**

Ensure `psycopg2-binary` is in your requirements.txt:

```txt
flask==3.0.3
flask-cors==6.0.0
flask-jwt-extended==4.7.1
bcrypt==4.2.1
PyJWT==2.9.0
gunicorn==23.0.0
psycopg2-binary==2.9.9
```

**If missing:**

1. Add it to requirements.txt
2. Commit and push:
```bash
git add requirements.txt
git commit -m "Add psycopg2-binary"
git push
```

---

## 🧪 **Quick Test**

### **Test 1: Check if App is Running**

Open your Railway URL. You should see the login page.

**If you see "Application Error":**
- Check Railway logs for errors
- Database connection is failing

### **Test 2: Try Login with Demo Account**

Email: `admin@taskflow.com`
Password: `password123`

**If 401 error:**
- Database tables don't exist
- Seed function didn't run

### **Test 3: Try Signup**

Create a new account.

**If 500 error:**
- Database connection failed
- Check logs for specific error

---

## 🔍 **Common Error Messages**

### **Error: "relation 'users' does not exist"**

**Cause:** Tables not created

**Fix:**
1. Check logs for "🌱 Seeding demo data..."
2. If missing, redeploy the app
3. Ensure `init_db()` is called in app.py

### **Error: "psycopg2.OperationalError"**

**Cause:** Can't connect to PostgreSQL

**Fix:**
1. Verify DATABASE_URL is correct
2. Check PostgreSQL service is running
3. Try restarting PostgreSQL service

### **Error: "No module named 'psycopg2'"**

**Cause:** psycopg2-binary not installed

**Fix:**
1. Add to requirements.txt: `psycopg2-binary==2.9.9`
2. Push to GitHub
3. Railway will reinstall dependencies

---

## 📋 **Step-by-Step Fix**

### **Option A: Fresh PostgreSQL Setup**

```bash
# 1. Ensure code is up to date
git add .
git commit -m "Fix PostgreSQL setup"
git push

# 2. On Railway:
# - Delete PostgreSQL service (if exists)
# - Click "New" → "Database" → "PostgreSQL"
# - Wait for provisioning
# - Verify DATABASE_URL appears in TaskFlow variables
# - Redeploy TaskFlow service

# 3. Check logs for:
# ✓ Using PostgreSQL database
# 🌱 Seeding demo data...
# ✅ Seed complete
```

### **Option B: Use SQLite (Quick Fix)**

```bash
# 1. On Railway:
# - Go to TaskFlow service → Variables
# - Remove DATABASE_URL variable
# - App will redeploy with SQLite

# 2. Test the app
# - Should work immediately
# - Data will reset on restarts (that's okay for demo)
```

---

## 🎯 **Recommended Action**

**For immediate fix:**
1. Use **Option B** (SQLite) to get app working now
2. Submit assignment with working app
3. Add PostgreSQL later if needed

**For production setup:**
1. Use **Option A** (PostgreSQL) for persistent data
2. Takes 5-10 minutes to troubleshoot
3. Better for long-term use

---

## 📞 **Quick Commands**

```bash
# View Railway logs
railway logs --follow

# Redeploy
railway up

# Check environment variables
railway variables

# Link to project (if not linked)
railway link
```

---

## ✅ **Success Indicators**

You'll know it's fixed when:

✅ No 500 errors on signup
✅ Can create new account
✅ Can login with demo accounts
✅ Dashboard loads with data

---

## 🆘 **Still Not Working?**

### **Quick Diagnostic:**

1. **Check Railway logs** - What's the actual error?
2. **Check Variables tab** - Is DATABASE_URL set?
3. **Check PostgreSQL service** - Is it running?
4. **Try SQLite** - Remove DATABASE_URL temporarily

### **Share These Details:**

If you need more help, share:
- Railway logs (last 50 lines)
- Variables tab screenshot
- Specific error message from browser console

---

## 🎯 **Most Likely Fix**

**90% of the time, it's one of these:**

1. ✅ DATABASE_URL not set → Add it in Variables
2. ✅ PostgreSQL not created → Add PostgreSQL service
3. ✅ Tables not created → Redeploy to run init_db()
4. ✅ psycopg2 missing → Add to requirements.txt

**Try these in order!**

---

**Need immediate fix?** Remove DATABASE_URL and use SQLite! 🚀
