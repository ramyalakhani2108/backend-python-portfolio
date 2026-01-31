#!/bin/bash

# Portfolio Backend - Deployment Setup Script

echo "🚀 Setting up deployment files..."

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Portfolio Backend API ready for deployment"
    echo "✅ Git repository initialized"
    echo ""
    echo "📝 Next steps:"
    echo "1. Create a new repository on GitHub"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/portfolio-backend.git"
    echo "3. Run: git branch -M main"
    echo "4. Run: git push -u origin main"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "📋 Deployment files created:"
echo "  ✅ Procfile (for Heroku-style platforms)"
echo "  ✅ runtime.txt (Python version)"
echo "  ✅ render.yaml (Render.com configuration)"
echo "  ✅ DEPLOYMENT.md (Full deployment guide)"
echo "  ✅ QUICK_DEPLOY.md (Quick start guide)"
echo ""
echo "🎯 Recommended deployment platform: Render.com"
echo "📖 Read QUICK_DEPLOY.md for 5-minute deployment instructions"
echo ""
echo "🔗 Quick links:"
echo "  • Render.com: https://render.com"
echo "  • Railway.app: https://railway.app"
echo "  • Fly.io: https://fly.io"
echo ""
echo "✨ Your backend is ready to deploy!"
