# 🚀 Railway Deployment Guide

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Git installed (you have: git version 2.49.0)
- ✅ GitHub account
- ✅ Railway account (sign up at https://railway.app)

---

## 🎯 Deployment Steps

### Step 1: Initialize Git Repository (2 minutes)

```bash
# Navigate to project folder
cd taskflow-final

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: TaskFlow Team Task Manager"
```

---

### Step 2: Create GitHub Repository (3 minutes)

#### Option A: Using GitHub Website (Easier)

1. Go to https://github.com/new
2. Repository name: `taskflow-team-manager`
3. Description: `Full-stack team task management app with role-based access control`
4. Keep it **Public** (required for free Railway deployment)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

7. Copy the commands shown and run them:
```bash
git remote add origin https://github.com/YOUR_USERNAME/taskflow-team-manager.git
git branch -M main
git push -u origin main
```

#### Option B: Using GitHub CLI (if installed)

```bash
gh repo create taskflow-team-manager --public --source=. --remote=origin
git push -u origin main
```

---

### Step 3: Deploy to Railway (5 minutes)

#### Method 1: Deploy from GitHub (Recommended)

1. **Sign up/Login to Railway:**
   - Go to https://railway.app
   - Click "Login" → Sign in with GitHub
   - Authorize Railway to access your GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `taskflow-team-manager` repository
   - Click "Deploy Now"

3. **Railway Auto-Detection:**
   - Railway will automatically detect Python
   - It will use your `railway.toml` configuration
   - Build will start automatically

4. **Wait for Deployment:**
   - Watch the build logs
   - Wait for "Success" status (2-3 minutes)

5. **Generate Domain:**
   - Click on your deployment
   - Go to "Settings" tab
   - Scroll to "Networking" section
   - Click "Generate Domain"
   - Copy your live URL (e.g., `taskflow-production.up.railway.app`)

6. **Test Your App:**
   - Open the generated URL
   - Login with: `admin@taskflow.com` / `password123`
   - Test all features

---

#### Method 2: Deploy with Railway CLI (Alternative)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up

# Generate domain
railway domain
```

---

### Step 4: Configure Environment Variables (Optional)

For better security in production:

1. In Railway dashboard, go to your project
2. Click "Variables" tab
3. Add these variables:

```
JWT_SECRET=your-super-secret-random-string-change-this-in-production
PORT=3000
```

**Generate a secure JWT_SECRET:**
```bash
# On Windows PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# Or use any random string generator
```

4. Click "Deploy" to restart with new variables

---

## ⚠️ Important Notes

### Database Persistence

**Current Setup (SQLite):**
- Database resets on every deployment/restart
- Demo data auto-regenerates via seed function
- Perfect for demo/evaluation purposes

**For Production (Optional):**

If you want persistent data, you have 2 options:

#### Option 1: Add Railway Volume
1. In Railway dashboard → "Settings"
2. Scroll to "Volumes"
3. Click "Add Volume"
4. Mount path: `/data`
5. Add environment variable: `DB_PATH=/data/taskflow.db`
6. Redeploy

#### Option 2: Switch to PostgreSQL
1. In Railway dashboard → "New" → "Database" → "PostgreSQL"
2. Railway will provide `DATABASE_URL`
3. Update `app.py` to use PostgreSQL instead of SQLite
4. Install `psycopg2` in requirements.txt

**For this assignment, SQLite is fine!** The evaluators just need to see a working app.

---

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] All files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project deployed on Railway
- [ ] Domain generated
- [ ] App accessible via URL
- [ ] Login works with demo accounts
- [ ] All features functional

---

## 🧪 Test Your Deployment

After deployment, test these critical features:

1. **Authentication:**
   - [ ] Login with `admin@taskflow.com` / `password123`
   - [ ] Signup with new account

2. **Dashboard:**
   - [ ] Stats cards display correctly
   - [ ] My Tasks section loads
   - [ ] Recent activity shows

3. **Projects:**
   - [ ] Can view demo projects
   - [ ] Can create new project
   - [ ] Can edit project (as admin)

4. **Tasks:**
   - [ ] Can create tasks
   - [ ] Can edit tasks
   - [ ] Can change status
   - [ ] Board view works
   - [ ] List view works

5. **Permissions:**
   - [ ] Admin has full access
   - [ ] Member has limited access

**If all tests pass → Deployment successful! 🎉**

---

## 📝 Update README with Live URL

After deployment, update your README.md:

```markdown
## 🚀 Live Demo

**Live URL:** https://your-app-name.up.railway.app

**Demo credentials:**
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@taskflow.com | password123 |
| Member | sam@taskflow.com | password123 |
```

Commit and push the change:
```bash
git add README.md
git commit -m "Add live deployment URL"
git push
```

---

## 🆘 Troubleshooting

### Build Fails

**Problem:** Railway build fails with Python errors
**Solution:** 
- Check build logs for specific error
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### App Crashes on Start

**Problem:** App starts but crashes immediately
**Solution:**
- Check Railway logs (click "View Logs")
- Ensure all dependencies installed
- Check for missing environment variables

### Database Not Found

**Problem:** "No such table" errors
**Solution:**
- Database should auto-create on first run
- Check that `init_db()` is called in `app.py`
- Redeploy to trigger fresh database creation

### 502 Bad Gateway

**Problem:** URL shows 502 error
**Solution:**
- Wait 2-3 minutes for deployment to complete
- Check Railway logs for errors
- Ensure app binds to `0.0.0.0:$PORT`

### Demo Data Missing

**Problem:** No projects or users after deployment
**Solution:**
- Check that `seed_demo()` is called in `app.py`
- Redeploy to trigger seed function
- Check logs for seed completion message

---

## 📊 Deployment Status

**Date:** _______________

| Step | Status | Notes |
|------|--------|-------|
| Git initialized | ⬜ | |
| GitHub repo created | ⬜ | |
| Code pushed | ⬜ | |
| Railway account | ⬜ | |
| App deployed | ⬜ | |
| Domain generated | ⬜ | |
| App tested | ⬜ | |
| README updated | ⬜ | |

**Live URL:** _________________________________

**Deployment Status:** ⬜ SUCCESS / ⬜ IN PROGRESS / ⬜ FAILED

---

## 🎥 Next Steps: Demo Video

After successful deployment:

1. **Record 2-5 minute demo video showing:**
   - Live URL in browser
   - Login with demo account
   - Dashboard overview
   - Create a project
   - Create and assign tasks
   - Show different user roles
   - Demonstrate key features

2. **Tools for recording:**
   - OBS Studio (free)
   - Loom (easy, free tier)
   - Windows Game Bar (Win + G)
   - QuickTime (Mac)

3. **Upload to:**
   - YouTube (unlisted)
   - Google Drive
   - Loom

---

## 📦 Final Submission Checklist

- [ ] ✅ Live URL working
- [ ] ✅ GitHub repository public
- [ ] ✅ README.md updated with live URL
- [ ] ✅ Demo video recorded (2-5 min)
- [ ] ✅ All features functional
- [ ] ✅ Demo accounts work

**You're ready to submit! 🎉**

---

## 📞 Quick Commands Reference

```bash
# Git commands
git status                    # Check status
git add .                     # Stage all files
git commit -m "message"       # Commit changes
git push                      # Push to GitHub

# Railway CLI commands
railway login                 # Login to Railway
railway status                # Check deployment status
railway logs                  # View logs
railway open                  # Open app in browser
railway domain                # Manage domains

# View logs
railway logs --follow         # Live logs
```

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ App is accessible via Railway URL
✅ No errors in Railway logs
✅ Demo accounts login successfully
✅ All CRUD operations work
✅ Database persists during session
✅ UI loads correctly
✅ API endpoints respond

---

**Need help?** Check Railway documentation: https://docs.railway.app

**Good luck with your deployment! 🚀**
