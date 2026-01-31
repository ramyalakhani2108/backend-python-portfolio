# Free Hosting Deployment Guide

## 🚀 Recommended: Deploy to Render.com (Best Free Option)

Render.com offers the best free tier for Python applications with no credit card required.

### Prerequisites:
1. GitHub account
2. Your code pushed to a GitHub repository

### Step-by-Step Deployment:

#### 1. **Push Your Code to GitHub**

```bash
cd D:\portfolio-application\backend

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Portfolio Backend API"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/portfolio-backend.git
git branch -M main
git push -u origin main
```

#### 2. **Sign Up on Render.com**
- Go to https://render.com
- Sign up with your GitHub account (free, no credit card needed)

#### 3. **Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository: `portfolio-backend`
- Configure:
  - **Name**: `portfolio-backend` (or any name you prefer)
  - **Runtime**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - **Plan**: Free

#### 4. **Set Environment Variables**

In Render dashboard, go to "Environment" and add:

```
DATABASE_URL = postgresql+asyncpg://postgres:techby@rp21@db.fwgjnitsshrszhkdzase.supabase.co:5432/postgres
GEMINI_API_KEY = AIzaSyDumR56I5D6REsd2YyjFdx-9PQzfrLN9xc
ADMIN_USERNAME = admin
ADMIN_PASSWORD = adminn@gmail12312
ADMIN_SECRET_KEY = your-super-secret-admin-key-change-this-in-production
SECRET_KEY = your-super-secret-jwt-key-change-this-in-production
CORS_ORIGINS = ["*"]
DEBUG = false
GEMINI_MODEL = gemini-2.5-flash
PROJECT_NAME = Portfolio API
```

#### 5. **Deploy**
- Click "Create Web Service"
- Render will automatically build and deploy your app
- You'll get a URL like: `https://portfolio-backend.onrender.com`

#### 6. **Update Flutter App**
Update your Flutter app's API base URL to:
```dart
static const String baseUrl = 'https://portfolio-backend.onrender.com';
```

### ⚠️ Free Tier Limitations:
- **Spin down after 15 minutes of inactivity** (first request after inactivity takes ~30 seconds)
- 750 hours/month (enough for 24/7 with one service)
- Automatic HTTPS included
- Custom domains supported (optional)

---

## Alternative Free Hosting Options:

### Option 2: Railway.app

**Pros**: 
- Easy deployment
- $5 free credit monthly (500 hours)
- Fast cold starts

**Steps**:
1. Go to https://railway.app
2. Sign in with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables
6. Railway auto-detects Python and deploys

**Command**: 
```bash
railway login
railway init
railway up
```

### Option 3: Fly.io

**Pros**:
- Good free tier
- Multiple regions
- Fast performance

**Steps**:
1. Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Run:
```bash
cd D:\portfolio-application\backend
fly auth signup
fly launch --name portfolio-backend
fly secrets set DATABASE_URL="your-database-url"
fly secrets set GEMINI_API_KEY="your-api-key"
# ... set other secrets
fly deploy
```

### Option 4: PythonAnywhere

**Pros**:
- Specifically for Python apps
- Always-on free tier (limited)

**Cons**:
- More manual setup
- Limited outbound HTTPS on free tier

### Option 5: Google Cloud Run

**Pros**:
- Generous free tier (2 million requests/month)
- Scales to zero

**Requires**:
- Credit card for verification (won't be charged on free tier)
- Docker knowledge

---

## 📝 Important Post-Deployment Steps:

### 1. Update CORS Settings (Production)
After deployment, update `.env` or Render environment variables:
```
CORS_ORIGINS = ["https://your-flutter-web-app.com", "https://your-admin-domain.com"]
```

### 2. Secure Your Secrets
Change these in production:
- `ADMIN_PASSWORD`
- `SECRET_KEY`
- `ADMIN_SECRET_KEY`

### 3. Test Your Deployment
```bash
# Health check
curl https://your-app.onrender.com/health

# API docs
https://your-app.onrender.com/docs

# Admin panel
https://your-app.onrender.com/admin/login
```

### 4. Monitor Your App
- Render Dashboard: View logs and metrics
- Set up uptime monitoring: https://uptimerobot.com (free)

---

## 🔥 Keeping Your Free App Awake

Render free tier spins down after 15 minutes of inactivity. Options:

### Option A: Cron Job (External Ping)
Use https://cron-job.org (free) to ping your health endpoint every 14 minutes:
```
GET https://your-app.onrender.com/health
```

### Option B: UptimeRobot
https://uptimerobot.com
- Add your app URL
- Set check interval to 5 minutes
- Free plan includes 50 monitors

### Option C: Accept the Spin-Down
- First request takes ~30 seconds to wake up
- Subsequent requests are instant
- Good enough for personal projects

---

## 📊 Comparison Table:

| Platform | Free Hours | Cold Start | Build Time | Ease of Use | Best For |
|----------|-----------|------------|------------|-------------|----------|
| **Render** | 750/month | ~30s | ~2 min | ⭐⭐⭐⭐⭐ | **Best Overall** |
| Railway | 500/month ($5 credit) | ~10s | ~2 min | ⭐⭐⭐⭐⭐ | Fast deployment |
| Fly.io | Always-on (limited) | ~5s | ~3 min | ⭐⭐⭐⭐ | Global apps |
| PythonAnywhere | Always-on | N/A | Manual | ⭐⭐⭐ | Python-specific |

---

## 🎯 Recommended Workflow:

1. **Development**: `localhost:8000`
2. **Staging**: Deploy to Render (free tier)
3. **Production**: Upgrade Render or use Railway

---

## Need Help?

- Render Docs: https://render.com/docs/deploy-fastapi
- Railway Docs: https://docs.railway.app/getting-started
- Fly.io Docs: https://fly.io/docs/languages-and-frameworks/python/

Your app is ready to deploy! 🚀
