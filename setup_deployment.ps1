# Portfolio Backend - Deployment Setup Script for Windows

Write-Host "🚀 Setting up deployment files..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - Portfolio Backend API ready for deployment"
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Create a new repository on GitHub"
    Write-Host "2. Run: git remote add origin https://github.com/YOUR_USERNAME/portfolio-backend.git"
    Write-Host "3. Run: git branch -M main"
    Write-Host "4. Run: git push -u origin main"
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Deployment files created:" -ForegroundColor Cyan
Write-Host "  ✅ Procfile (for Heroku-style platforms)"
Write-Host "  ✅ runtime.txt (Python version)"
Write-Host "  ✅ render.yaml (Render.com configuration)"
Write-Host "  ✅ DEPLOYMENT.md (Full deployment guide)"
Write-Host "  ✅ QUICK_DEPLOY.md (Quick start guide)"
Write-Host ""
Write-Host "🎯 Recommended deployment platform: Render.com" -ForegroundColor Yellow
Write-Host "📖 Read QUICK_DEPLOY.md for 5-minute deployment instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔗 Quick links:" -ForegroundColor Cyan
Write-Host "  • Render.com: https://render.com"
Write-Host "  • Railway.app: https://railway.app"
Write-Host "  • Fly.io: https://fly.io"
Write-Host ""
Write-Host "✨ Your backend is ready to deploy!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
