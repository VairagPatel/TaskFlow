#!/bin/bash

# TaskFlow Railway Deployment Script
# This script automates the deployment process

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🚀 TaskFlow Railway Deployment Script               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Step 1: Initialize Git Repository
echo "📦 Step 1: Initializing Git repository..."
if [ -d .git ]; then
    echo "✅ Git repository already initialized"
else
    git init
    echo "✅ Git repository initialized"
fi
echo ""

# Step 2: Add all files
echo "📝 Step 2: Adding files to Git..."
git add .
echo "✅ Files added"
echo ""

# Step 3: Create commit
echo "💾 Step 3: Creating commit..."
git commit -m "Initial commit: TaskFlow Team Task Manager" || echo "✅ Already committed"
echo ""

# Step 4: GitHub repository
echo "🌐 Step 4: GitHub Repository Setup"
echo ""
echo "Please create a GitHub repository manually:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: taskflow-team-manager"
echo "3. Make it PUBLIC"
echo "4. DO NOT initialize with README"
echo "5. Click 'Create repository'"
echo ""
read -p "Press Enter after creating the repository..."
echo ""

# Step 5: Add remote
echo "🔗 Step 5: Adding GitHub remote..."
read -p "Enter your GitHub username: " github_username
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$github_username/taskflow-team-manager.git"
echo "✅ Remote added"
echo ""

# Step 6: Push to GitHub
echo "⬆️  Step 6: Pushing to GitHub..."
git branch -M main
git push -u origin main
echo "✅ Code pushed to GitHub"
echo ""

# Step 7: Railway deployment instructions
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              🚂 Railway Deployment Instructions              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Now deploy to Railway:"
echo ""
echo "1. Go to: https://railway.app"
echo "2. Click 'Login' → Sign in with GitHub"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose 'taskflow-team-manager'"
echo "6. Click 'Deploy Now'"
echo "7. Wait for build to complete (2-3 minutes)"
echo "8. Go to Settings → Generate Domain"
echo "9. Copy your live URL"
echo ""
echo "✅ Your app will be live at: https://[your-app].up.railway.app"
echo ""
echo "🎉 Deployment process complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Test your live app"
echo "   2. Update README.md with live URL"
echo "   3. Record demo video (2-5 min)"
echo "   4. Submit assignment"
echo ""
