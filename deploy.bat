@echo off
REM TaskFlow Railway Deployment Script for Windows
REM This script automates the deployment process

echo ================================================================
echo          TaskFlow Railway Deployment Script
echo ================================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Step 1: Initialize Git Repository
echo ================================================================
echo Step 1: Initializing Git repository...
echo ================================================================
if exist .git (
    echo [OK] Git repository already initialized
) else (
    git init
    echo [OK] Git repository initialized
)
echo.

REM Step 2: Add all files
echo ================================================================
echo Step 2: Adding files to Git...
echo ================================================================
git add .
echo [OK] Files added
echo.

REM Step 3: Create commit
echo ================================================================
echo Step 3: Creating commit...
echo ================================================================
git commit -m "Initial commit: TaskFlow Team Task Manager"
if errorlevel 1 (
    echo [INFO] Already committed or no changes
)
echo.

REM Step 4: GitHub repository
echo ================================================================
echo Step 4: GitHub Repository Setup
echo ================================================================
echo.
echo Please create a GitHub repository manually:
echo 1. Go to: https://github.com/new
echo 2. Repository name: taskflow-team-manager
echo 3. Make it PUBLIC
echo 4. DO NOT initialize with README
echo 5. Click 'Create repository'
echo.
pause
echo.

REM Step 5: Add remote
echo ================================================================
echo Step 5: Adding GitHub remote...
echo ================================================================
set /p github_username="Enter your GitHub username: "
git remote remove origin 2>nul
git remote add origin "https://github.com/%github_username%/taskflow-team-manager.git"
echo [OK] Remote added
echo.

REM Step 6: Push to GitHub
echo ================================================================
echo Step 6: Pushing to GitHub...
echo ================================================================
git branch -M main
git push -u origin main
echo [OK] Code pushed to GitHub
echo.

REM Step 7: Railway deployment instructions
echo ================================================================
echo          Railway Deployment Instructions
echo ================================================================
echo.
echo Now deploy to Railway:
echo.
echo 1. Go to: https://railway.app
echo 2. Click 'Login' - Sign in with GitHub
echo 3. Click 'New Project'
echo 4. Select 'Deploy from GitHub repo'
echo 5. Choose 'taskflow-team-manager'
echo 6. Click 'Deploy Now'
echo 7. Wait for build to complete (2-3 minutes)
echo 8. Go to Settings - Generate Domain
echo 9. Copy your live URL
echo.
echo [OK] Your app will be live at: https://[your-app].up.railway.app
echo.
echo ================================================================
echo Deployment process complete!
echo ================================================================
echo.
echo Next steps:
echo    1. Test your live app
echo    2. Update README.md with live URL
echo    3. Record demo video (2-5 min)
echo    4. Submit assignment
echo.
pause
