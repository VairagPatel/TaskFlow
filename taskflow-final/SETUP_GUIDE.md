# 🚀 Quick Setup Guide

## ⚠️ Python Not Found!

You need to install Python before running this project.

---

## 📥 Install Python on Windows

### Option 1: Official Python Installer (Recommended)

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11" (or latest version)

2. **Install Python:**
   - Run the downloaded installer
   - ✅ **IMPORTANT:** Check "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   ```bash
   python --version
   # Should show: Python 3.11.x
   
   pip --version
   # Should show: pip 23.x.x
   ```

### Option 2: Microsoft Store (Easier)

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click "Get" or "Install"
4. Wait for installation
5. Verify in terminal: `python --version`

---

## 🏃 Run the Project

Once Python is installed:

```bash
# 1. Navigate to project folder
cd taskflow-final

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

**Expected Output:**
```
🌱 Seeding demo data...
✅ Seed complete
🚀 TaskFlow running on http://localhost:3000
```

---

## 🌐 Access the Application

1. Open your browser
2. Go to: **http://localhost:3000**
3. Login with demo account:
   - Email: `admin@taskflow.com`
   - Password: `password123`

---

## 📋 Next Steps

After the app is running:

1. ✅ Use **TESTING_CHECKLIST.md** to test all features
2. ✅ Check each section systematically
3. ✅ Mark items as you test them
4. ✅ Note any bugs found

---

## 🆘 Troubleshooting

### Issue: "python: command not found"
**Solution:** Python not in PATH. Reinstall and check "Add to PATH"

### Issue: "pip: command not found"
**Solution:** Run: `python -m pip install -r requirements.txt`

### Issue: "Port 3000 already in use"
**Solution:** 
- Close other apps using port 3000
- Or change port in app.py: `port = 3001`

### Issue: "Module not found" errors
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: Database errors
**Solution:** Delete `taskflow.db` file and restart app

---

## 📞 Need Help?

If you encounter issues:
1. Check error messages carefully
2. Google the specific error
3. Check Python version (needs 3.8+)
4. Ensure all dependencies installed

---

**Ready to test?** Follow the **TESTING_CHECKLIST.md** file! 🎯
