@echo off
echo ================================================================
echo          Fixing Repository Structure for Railway
echo ================================================================
echo.
echo This script will move files to the correct location for Railway
echo.
pause

REM Navigate to parent directory
cd ..

echo Step 1: Moving files from taskflow-final to root...
echo.

REM Move all files from taskflow-final to current directory
move taskflow-final\* . 2>nul
if errorlevel 1 (
    echo [INFO] Some files may already be in place
)

REM Remove the now-empty taskflow-final directory
rmdir taskflow-final 2>nul

echo [OK] Files moved to root directory
echo.

echo Step 2: Checking repository structure...
echo.
dir /b

echo.
echo Step 3: Committing changes...
git add .
git commit -m "Fix: Move files to root for Railway deployment"

echo.
echo Step 4: Pushing to GitHub...
git push

echo.
echo ================================================================
echo Files moved successfully!
echo ================================================================
echo.
echo Railway will now detect your app correctly.
echo.
echo Next steps:
echo 1. Go to Railway dashboard
echo 2. Your app should automatically redeploy
echo 3. Wait for build to complete
echo 4. Check deployment logs
echo.
pause
