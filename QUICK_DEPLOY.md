# Quick Deploy to Render.com

## 🚀 5-Minute Deployment

### 1. Push to GitHub (if not already):
```bash
cd D:\portfolio-application\backend
git init
git add .
git commit -m "Ready for deployment"
```

Create repo on GitHub, then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/portfolio-backend.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render:
1. Go to https://render.com and sign up (free, no credit card)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Render will auto-detect settings from `render.yaml`
5. Add these environment variables:

```
DATABASE_URL = postgresql+asyncpg://postgres:techby@rp21@db.fwgjnitsshrszhkdzase.supabase.co:5432/postgres
GEMINI_API_KEY = AIzaSyDumR56I5D6REsd2YyjFdx-9PQzfrLN9xc
ADMIN_PASSWORD = adminn@gmail12312
ADMIN_SECRET_KEY = your-super-secret-admin-key-change-this-in-production
SECRET_KEY = your-super-secret-jwt-key-change-this-in-production
```

6. Click "Create Web Service"

### 3. Get Your URL:
After deployment completes (~3 min), you'll get:
```
https://portfolio-backend.onrender.com
```

### 4. Update Flutter App:
```dart
static const String baseUrl = 'https://portfolio-backend.onrender.com';
```

### 5. Test:
- Health: https://your-app.onrender.com/health
- Docs: https://your-app.onrender.com/docs
- Admin: https://your-app.onrender.com/admin/login

✅ Done! Your API is live!

**Note**: Free tier sleeps after 15 min inactivity (first request takes ~30s to wake up)

---

## Keep It Awake (Optional):
Use https://cron-job.org to ping every 14 min:
```
GET https://your-app.onrender.com/health
```
