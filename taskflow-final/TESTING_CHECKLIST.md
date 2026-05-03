# 🧪 TaskFlow Testing Checklist

## 📋 Pre-Testing Setup

### ✅ Prerequisites Check
- [ ] Python 3.8+ installed (`python --version` or `py --version`)
- [ ] pip installed (`pip --version`)
- [ ] Virtual environment created (optional but recommended)

### ✅ Installation Steps
```bash
# Navigate to project folder
cd taskflow-final

# Create virtual environment (optional)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Expected Output:**
```
🌱 Seeding demo data...
✅ Seed complete
🚀 TaskFlow running on http://localhost:3000
```

---

## 🔍 TESTING CHECKLIST

### 1️⃣ **SERVER STARTUP** ✅

**Test:** Application starts successfully

- [ ] Server starts without errors
- [ ] Port 3000 is accessible
- [ ] Database file `taskflow.db` is created
- [ ] Console shows "TaskFlow running on http://localhost:3000"
- [ ] No Python errors in terminal

**How to Test:**
1. Run `python app.py`
2. Check terminal output
3. Verify `taskflow.db` file exists in project folder

---

### 2️⃣ **HEALTH CHECK** ✅

**Test:** Health endpoint responds

- [ ] Open browser: `http://localhost:3000/api/health`
- [ ] Returns JSON: `{"status": "ok", "time": "..."}`
- [ ] HTTP status code: 200

---

### 3️⃣ **AUTHENTICATION - SIGNUP** ✅

**Test:** New user registration

#### Test Case 1: Valid Signup
- [ ] Open `http://localhost:3000`
- [ ] Click "Sign Up" tab
- [ ] Fill form:
  - Name: `Test User`
  - Email: `test@example.com`
  - Password: `password123`
  - Role: `Member`
- [ ] Click "Create Account →"
- [ ] ✅ Success: Redirects to dashboard
- [ ] ✅ Toast notification: "Account created"
- [ ] ✅ User avatar appears in sidebar

#### Test Case 2: Invalid Signup (Validation)
- [ ] Try empty name → Error: "Name, email and password are required"
- [ ] Try invalid email (no @) → Error: "Invalid email format"
- [ ] Try short password (< 6 chars) → Error: "Password must be at least 6 characters"
- [ ] Try duplicate email → Error: "Email already registered"

**Expected Results:**
- ✅ Valid signup creates account and logs in
- ✅ Invalid inputs show error messages
- ✅ No page refresh (SPA behavior)

---

### 4️⃣ **AUTHENTICATION - LOGIN** ✅

**Test:** User login with existing accounts

#### Test Case 1: Admin Login
- [ ] Logout if logged in
- [ ] Click "Sign In" tab
- [ ] Email: `admin@taskflow.com`
- [ ] Password: `password123`
- [ ] Click "Sign In →"
- [ ] ✅ Redirects to dashboard
- [ ] ✅ Sidebar shows "Alex Admin" with role "admin"
- [ ] ✅ Can see all projects

#### Test Case 2: Member Login
- [ ] Logout
- [ ] Email: `sam@taskflow.com`
- [ ] Password: `password123`
- [ ] ✅ Logs in successfully
- [ ] ✅ Sidebar shows "Sam Developer" with role "member"
- [ ] ✅ Can only see assigned projects

#### Test Case 3: Invalid Login
- [ ] Try wrong password → Error: "Invalid credentials"
- [ ] Try non-existent email → Error: "Invalid credentials"
- [ ] Try empty fields → Error: "Email and password are required"

**Expected Results:**
- ✅ Correct credentials log in successfully
- ✅ Wrong credentials show error
- ✅ Token stored in localStorage

---

### 5️⃣ **DASHBOARD** ✅

**Test:** Dashboard displays correct data

**Login as:** `admin@taskflow.com` / `password123`

#### Statistics Cards
- [ ] Total Tasks shows correct count
- [ ] In Progress count is accurate
- [ ] In Review count is accurate
- [ ] Done count is accurate
- [ ] Overdue count shows tasks past due date

#### My Tasks Section
- [ ] Shows tasks assigned to current user
- [ ] Sorted by priority (urgent → high → medium → low)
- [ ] Shows project name and color
- [ ] Overdue tasks highlighted in red

#### Overdue Tasks Panel
- [ ] Shows all overdue tasks
- [ ] Shows due date
- [ ] Shows assignee name
- [ ] Empty state if no overdue tasks

#### Recent Activity
- [ ] Shows recently updated tasks
- [ ] Shows project name
- [ ] Shows assignee
- [ ] Shows status badge

**Expected Results:**
- ✅ All sections load without errors
- ✅ Data is accurate and up-to-date
- ✅ Empty states show when no data

---

### 6️⃣ **PROJECT MANAGEMENT** ✅

**Test:** Create, view, edit, delete projects

#### Test Case 1: Create Project
- [ ] Click "Projects" in sidebar
- [ ] Click "+ New Project" button (top right)
- [ ] Fill form:
  - Name: `Test Project`
  - Description: `Testing project creation`
  - Color: Select any color
- [ ] Click "Create Project"
- [ ] ✅ Modal closes
- [ ] ✅ Toast: "Project created"
- [ ] ✅ New project appears in grid
- [ ] ✅ Project appears in sidebar

#### Test Case 2: View Project Details
- [ ] Click on "Website Redesign" project card
- [ ] ✅ Opens project detail page
- [ ] ✅ Shows project name in topbar
- [ ] ✅ Shows task board (4 columns)
- [ ] ✅ Shows tasks in correct columns
- [ ] ✅ "Edit Project" and "Manage Members" buttons visible (if admin)

#### Test Case 3: Edit Project
- [ ] Open any project
- [ ] Click "Edit Project" button
- [ ] Change name to `Updated Project Name`
- [ ] Change description
- [ ] Change color
- [ ] Click "Update Project"
- [ ] ✅ Modal closes
- [ ] ✅ Toast: "Project updated"
- [ ] ✅ Changes reflected immediately

#### Test Case 4: Delete Project
- [ ] Create a test project
- [ ] Open the project
- [ ] Click "Edit Project"
- [ ] Click "Delete Project" button
- [ ] Confirm deletion
- [ ] ✅ Redirects to projects page
- [ ] ✅ Toast: "Project deleted"
- [ ] ✅ Project removed from list

#### Test Case 5: Manage Members
- [ ] Open any project
- [ ] Click "Manage Members" button
- [ ] ✅ Shows current members list
- [ ] ✅ Shows "Add Member" button
- [ ] Click "Add Member"
- [ ] Select user from dropdown
- [ ] Select role (Admin/Member)
- [ ] Click "Add"
- [ ] ✅ Member added to list
- [ ] Click "Remove" on a member
- [ ] ✅ Member removed

**Expected Results:**
- ✅ All CRUD operations work
- ✅ Only admins can edit/delete
- ✅ Changes reflect immediately
- ✅ Proper error handling

---

### 7️⃣ **TASK MANAGEMENT** ✅

**Test:** Create, view, edit, delete tasks

#### Test Case 1: Create Task
- [ ] Open "Website Redesign" project
- [ ] Click "+ New Task" button
- [ ] Fill form:
  - Title: `Test Task`
  - Description: `Testing task creation`
  - Status: `To Do`
  - Priority: `High`
  - Assignee: Select a user
  - Due Date: Select future date
- [ ] Click "Create Task"
- [ ] ✅ Modal closes
- [ ] ✅ Toast: "Task created"
- [ ] ✅ Task appears in correct column
- [ ] ✅ Shows priority badge
- [ ] ✅ Shows assignee avatar

#### Test Case 2: View Task Details
- [ ] Click on any task card
- [ ] ✅ Opens task detail modal
- [ ] ✅ Shows full description
- [ ] ✅ Shows all metadata (status, priority, assignee, due date)
- [ ] ✅ Shows comments section
- [ ] ✅ Shows "Edit" and "Delete" buttons (if permitted)

#### Test Case 3: Edit Task
- [ ] Open task detail
- [ ] Click "Edit Task" button
- [ ] Change title, description, status, priority
- [ ] Change assignee
- [ ] Change due date
- [ ] Click "Update Task"
- [ ] ✅ Modal closes
- [ ] ✅ Toast: "Task updated"
- [ ] ✅ Task moves to correct column (if status changed)
- [ ] ✅ Changes reflected immediately

#### Test Case 4: Quick Status Update (List View)
- [ ] Switch to "List" view
- [ ] Click status dropdown on any task
- [ ] Select different status
- [ ] ✅ Status updates immediately
- [ ] ✅ No page reload

#### Test Case 5: Add Comment
- [ ] Open task detail
- [ ] Scroll to comments section
- [ ] Type comment: `This is a test comment`
- [ ] Click "Add Comment"
- [ ] ✅ Comment appears immediately
- [ ] ✅ Shows your name and avatar
- [ ] ✅ Shows timestamp

#### Test Case 6: Delete Task
- [ ] Open task detail
- [ ] Click "Delete Task" button
- [ ] Confirm deletion
- [ ] ✅ Modal closes
- [ ] ✅ Toast: "Task deleted"
- [ ] ✅ Task removed from board

#### Test Case 7: Filter Tasks
- [ ] Click "In Progress" status filter
- [ ] ✅ Only in-progress tasks shown
- [ ] Click "Urgent" priority filter
- [ ] ✅ Only urgent tasks shown
- [ ] Click "All" to reset
- [ ] ✅ All tasks shown again

#### Test Case 8: Board vs List View
- [ ] Click "Board" view button
- [ ] ✅ Shows Kanban board (4 columns)
- [ ] Click "List" view button
- [ ] ✅ Shows table with all tasks
- [ ] ✅ Both views show same data

**Expected Results:**
- ✅ All CRUD operations work
- ✅ Filters work correctly
- ✅ View switching works
- ✅ Comments save and display
- ✅ Overdue tasks highlighted

---

### 8️⃣ **ROLE-BASED ACCESS CONTROL** ✅

**Test:** Permissions work correctly

#### Test Case 1: System Admin (admin@taskflow.com)
- [ ] Login as admin
- [ ] ✅ Can see ALL projects
- [ ] ✅ Can create projects
- [ ] ✅ Can edit ANY project
- [ ] ✅ Can delete ANY project
- [ ] ✅ Can manage members in ANY project
- [ ] ✅ Can edit/delete ANY task

#### Test Case 2: Project Admin (jordan@taskflow.com)
- [ ] Login as Jordan (project admin for Mobile App v2.0)
- [ ] ✅ Can see only assigned projects
- [ ] ✅ Can edit projects where admin
- [ ] ✅ Can manage members in admin projects
- [ ] ✅ Can edit/delete tasks in admin projects
- [ ] ❌ Cannot edit other projects

#### Test Case 3: Project Member (sam@taskflow.com)
- [ ] Login as Sam (member)
- [ ] ✅ Can see assigned projects
- [ ] ✅ Can create tasks
- [ ] ✅ Can edit own tasks
- [ ] ✅ Can edit assigned tasks
- [ ] ❌ Cannot edit project settings
- [ ] ❌ Cannot manage members
- [ ] ❌ Cannot delete others' tasks

**Expected Results:**
- ✅ Admins have full access
- ✅ Members have limited access
- ✅ Proper error messages for unauthorized actions
- ✅ UI hides unavailable actions

---

### 9️⃣ **MY TASKS PAGE** ✅

**Test:** Personal task view

- [ ] Click "My Tasks" in sidebar
- [ ] ✅ Shows all tasks assigned to you
- [ ] ✅ Shows across all projects
- [ ] ✅ Shows project name for each task
- [ ] ✅ Shows status, priority, due date
- [ ] ✅ Click task to open details
- [ ] ✅ Sorted by priority and due date

**Expected Results:**
- ✅ Only shows your assigned tasks
- ✅ Cross-project view works
- ✅ All task data visible

---

### 🔟 **PROFILE PAGE** ✅

**Test:** User profile view

- [ ] Click on user card in sidebar (bottom)
- [ ] ✅ Opens profile page
- [ ] ✅ Shows user name
- [ ] ✅ Shows email
- [ ] ✅ Shows role badge
- [ ] ✅ Shows avatar
- [ ] ✅ Shows account creation date

**Expected Results:**
- ✅ All user info displayed correctly
- ✅ Avatar matches sidebar

---

### 1️⃣1️⃣ **UI/UX FEATURES** ✅

**Test:** User interface elements

#### Navigation
- [ ] Sidebar navigation works
- [ ] Active page highlighted
- [ ] Project list in sidebar clickable
- [ ] Topbar shows current page title

#### Modals
- [ ] Modals open smoothly
- [ ] Click outside to close works
- [ ] X button closes modal
- [ ] Form validation shows errors

#### Toast Notifications
- [ ] Success toasts appear (green)
- [ ] Error toasts appear (red)
- [ ] Toasts auto-dismiss after 3.5s
- [ ] Multiple toasts stack properly

#### Responsive Design
- [ ] Works on desktop (1920x1080)
- [ ] Works on laptop (1366x768)
- [ ] Sidebar scrolls if needed
- [ ] Tables scroll horizontally if needed

#### Visual Elements
- [ ] Avatars show initials
- [ ] Project colors display correctly
- [ ] Status badges color-coded
- [ ] Priority badges color-coded
- [ ] Overdue indicators (red dots) show
- [ ] Progress bars animate
- [ ] Hover effects work

**Expected Results:**
- ✅ Smooth animations
- ✅ No visual glitches
- ✅ Consistent styling
- ✅ Professional appearance

---

### 1️⃣2️⃣ **DATA PERSISTENCE** ✅

**Test:** Data saves correctly

- [ ] Create a project
- [ ] Create tasks
- [ ] Add comments
- [ ] Logout
- [ ] Login again
- [ ] ✅ All data still present
- [ ] ✅ Projects exist
- [ ] ✅ Tasks exist
- [ ] ✅ Comments exist

**Expected Results:**
- ✅ Data persists in SQLite database
- ✅ No data loss on logout/login

---

### 1️⃣3️⃣ **ERROR HANDLING** ✅

**Test:** Application handles errors gracefully

#### Network Errors
- [ ] Stop server while logged in
- [ ] Try to create project
- [ ] ✅ Shows error toast
- [ ] ✅ Doesn't crash

#### Invalid Data
- [ ] Try to submit empty forms
- [ ] ✅ Shows validation errors
- [ ] Try invalid date formats
- [ ] ✅ Handles gracefully

#### 404 Errors
- [ ] Try to access non-existent project
- [ ] ✅ Shows error or redirects

**Expected Results:**
- ✅ No crashes
- ✅ User-friendly error messages
- ✅ Application remains functional

---

### 1️⃣4️⃣ **PERFORMANCE** ✅

**Test:** Application performance

- [ ] Dashboard loads in < 2 seconds
- [ ] Project list loads quickly
- [ ] Task board renders smoothly
- [ ] No lag when switching views
- [ ] Filters apply instantly
- [ ] Modals open/close smoothly

**Expected Results:**
- ✅ Fast load times
- ✅ Smooth interactions
- ✅ No freezing or lag

---

### 1️⃣5️⃣ **BROWSER COMPATIBILITY** ✅

**Test:** Works in different browsers

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)

**Expected Results:**
- ✅ Works in all modern browsers
- ✅ Consistent appearance
- ✅ All features functional

---

## 🎯 CRITICAL BUGS TO CHECK

### High Priority Issues
- [ ] ❌ Server crashes on startup
- [ ] ❌ Cannot login with demo credentials
- [ ] ❌ Database not created
- [ ] ❌ Tasks don't save
- [ ] ❌ Projects don't appear
- [ ] ❌ Permissions not enforced

### Medium Priority Issues
- [ ] ⚠️ Toast notifications don't show
- [ ] ⚠️ Modals don't close
- [ ] ⚠️ Filters don't work
- [ ] ⚠️ Comments don't save

### Low Priority Issues
- [ ] 🔸 Styling inconsistencies
- [ ] 🔸 Slow load times
- [ ] 🔸 Minor UI glitches

---

## ✅ FINAL CHECKLIST

### Before Deployment
- [ ] All critical features work
- [ ] No server crashes
- [ ] Demo accounts work
- [ ] Database creates successfully
- [ ] All CRUD operations functional
- [ ] RBAC enforced correctly
- [ ] UI looks professional
- [ ] No console errors

### Ready to Deploy When:
- [ ] ✅ 90%+ of tests pass
- [ ] ✅ No critical bugs
- [ ] ✅ Demo accounts work
- [ ] ✅ All core features functional

---

## 📊 TEST RESULTS SUMMARY

**Date:** _______________  
**Tester:** _______________

| Category | Tests Passed | Tests Failed | Status |
|----------|--------------|--------------|--------|
| Server Startup | __ / 5 | __ | ⬜ |
| Authentication | __ / 10 | __ | ⬜ |
| Dashboard | __ / 5 | __ | ⬜ |
| Projects | __ / 8 | __ | ⬜ |
| Tasks | __ / 12 | __ | ⬜ |
| RBAC | __ / 8 | __ | ⬜ |
| UI/UX | __ / 10 | __ | ⬜ |
| **TOTAL** | **__ / 58** | **__** | **⬜** |

**Overall Status:** 
- ✅ PASS (90%+ tests passed)
- ⚠️ NEEDS WORK (70-89% tests passed)
- ❌ FAIL (< 70% tests passed)

---

## 🐛 BUGS FOUND

| # | Description | Severity | Status |
|---|-------------|----------|--------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 📝 NOTES

_Add any additional observations or comments here:_

---

**Testing Complete!** 🎉

If 90%+ tests pass, you're ready to deploy to Railway!
