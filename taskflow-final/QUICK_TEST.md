# ⚡ Quick Test Guide (5 Minutes)

## 🎯 Fast Testing Checklist

Use this for a quick smoke test before deployment.

---

## ✅ 1. START SERVER (30 seconds)

```bash
cd taskflow-final
python app.py
```

**Check:**
- [ ] ✅ No errors in terminal
- [ ] ✅ Shows "TaskFlow running on http://localhost:3000"
- [ ] ✅ `taskflow.db` file created

---

## ✅ 2. TEST LOGIN (1 minute)

**Open:** http://localhost:3000

**Test Admin Login:**
- [ ] Email: `admin@taskflow.com`
- [ ] Password: `password123`
- [ ] ✅ Logs in successfully
- [ ] ✅ Shows dashboard with stats

**Test Member Login:**
- [ ] Logout
- [ ] Email: `sam@taskflow.com`
- [ ] Password: `password123`
- [ ] ✅ Logs in successfully

---

## ✅ 3. TEST DASHBOARD (30 seconds)

**Check:**
- [ ] ✅ Stats cards show numbers
- [ ] ✅ "My Tasks" section loads
- [ ] ✅ "Recent Activity" shows tasks
- [ ] ✅ No errors in browser console (F12)

---

## ✅ 4. TEST PROJECTS (1 minute)

**Click "Projects" in sidebar:**
- [ ] ✅ Shows 2 demo projects
- [ ] ✅ Click "Website Redesign"
- [ ] ✅ Opens project detail page
- [ ] ✅ Shows task board with 4 columns

**Create New Project:**
- [ ] ✅ Click "+ New Project"
- [ ] ✅ Fill: Name = "Test", Description = "Test"
- [ ] ✅ Click "Create Project"
- [ ] ✅ New project appears

---

## ✅ 5. TEST TASKS (1 minute)

**In any project:**
- [ ] ✅ Click "+ New Task"
- [ ] ✅ Fill: Title = "Test Task"
- [ ] ✅ Select status, priority, assignee
- [ ] ✅ Click "Create Task"
- [ ] ✅ Task appears in correct column

**Edit Task:**
- [ ] ✅ Click on task card
- [ ] ✅ Task detail modal opens
- [ ] ✅ Click "Edit Task"
- [ ] ✅ Change status to "In Progress"
- [ ] ✅ Save
- [ ] ✅ Task moves to "In Progress" column

---

## ✅ 6. TEST PERMISSIONS (1 minute)

**As Admin (admin@taskflow.com):**
- [ ] ✅ Can see "Edit Project" button
- [ ] ✅ Can see "Manage Members" button
- [ ] ✅ Can delete tasks

**As Member (sam@taskflow.com):**
- [ ] ✅ Cannot see "Edit Project" button
- [ ] ✅ Cannot see "Manage Members" button
- [ ] ✅ Can only edit own/assigned tasks

---

## ✅ 7. TEST FILTERS (30 seconds)

**In project detail:**
- [ ] ✅ Click "In Progress" status filter
- [ ] ✅ Only in-progress tasks show
- [ ] ✅ Click "All" to reset
- [ ] ✅ All tasks show again

---

## ✅ 8. TEST VIEWS (30 seconds)

**Switch views:**
- [ ] ✅ Click "List" view button
- [ ] ✅ Shows table view
- [ ] ✅ Click "Board" view button
- [ ] ✅ Shows Kanban board

---

## 🎯 PASS/FAIL CRITERIA

### ✅ PASS - Ready to Deploy
- All 8 sections work
- No critical errors
- Demo accounts login
- Can create/edit projects and tasks

### ⚠️ NEEDS WORK
- 1-2 sections fail
- Minor bugs present
- Some features not working

### ❌ FAIL - Not Ready
- 3+ sections fail
- Server crashes
- Cannot login
- Major features broken

---

## 📊 Your Results

**Date:** _______________

| Test | Status | Notes |
|------|--------|-------|
| 1. Server Start | ⬜ | |
| 2. Login | ⬜ | |
| 3. Dashboard | ⬜ | |
| 4. Projects | ⬜ | |
| 5. Tasks | ⬜ | |
| 6. Permissions | ⬜ | |
| 7. Filters | ⬜ | |
| 8. Views | ⬜ | |

**Overall:** ⬜ PASS / ⬜ NEEDS WORK / ⬜ FAIL

---

## 🚀 Next Steps

### If PASS:
1. ✅ Deploy to Railway
2. ✅ Push to GitHub
3. ✅ Record demo video
4. ✅ Submit assignment

### If NEEDS WORK:
1. ⚠️ Use full TESTING_CHECKLIST.md
2. ⚠️ Fix identified bugs
3. ⚠️ Re-test
4. ⚠️ Then deploy

### If FAIL:
1. ❌ Check SETUP_GUIDE.md
2. ❌ Verify Python installation
3. ❌ Check dependencies installed
4. ❌ Review error messages
5. ❌ Use full TESTING_CHECKLIST.md

---

**Good luck! 🎉**
