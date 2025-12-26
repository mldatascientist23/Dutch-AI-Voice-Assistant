# Netlify Deployment Guide

## 🚀 Deploying Dutch AI Voice Assistant on Netlify

This guide explains how to deploy the frontend of the Dutch AI Voice Assistant on Netlify.

### ⚠️ Important Note

The Dutch AI Voice Assistant consists of **two parts**:

1. **Frontend** (HTML/CSS/JS) - Can be deployed on Netlify ✅
2. **Backend** (FastAPI/Python) - Must be deployed separately ⚠️

Netlify is excellent for hosting the frontend, but the backend needs to be deployed on a platform that supports Python applications (like Render, Railway, or your own server).

---

## 📋 Prerequisites

- GitHub account
- Netlify account (free tier is sufficient)
- Backend deployed somewhere (see Backend Deployment Options below)

---

## 🎯 Quick Deployment Steps

### Step 1: Deploy Frontend to Netlify

1. **Fork or clone this repository to your GitHub account**

2. **Sign in to [Netlify](https://netlify.com)**

3. **Import your repository**:
   - Click "Add new site" → "Import an existing project"
   - Select GitHub and authorize Netlify
   - Select your repository

4. **Configure build settings** (should be auto-detected from `netlify.toml`):
   - Build command: `node build.js`
   - Publish directory: `frontend`

5. **Set Environment Variables** (IMPORTANT):
   - Go to "Site settings" → "Environment variables"
   - Add variable:
     - Key: `BACKEND_API_URL`
     - Value: Your backend URL (e.g., `https://your-backend.onrender.com`)

6. **Deploy**:
   - Click "Deploy site"
   - Wait for deployment to complete
   - Your frontend will be available at `https://your-site-name.netlify.app`

### Step 2: Verify Deployment

1. Visit your Netlify URL
2. Open browser console (F12)
3. Check for "API Base URL" log message
4. Try creating a test call
5. If backend is properly configured, the dashboard should work!

---

## 🔧 Backend Deployment Options

The backend needs to be hosted separately. Here are recommended platforms:

### Option 1: Render.com (Recommended - Free Tier)

1. Sign up at [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `DATABASE_URL`: `sqlite:///./voice_assistant.db`
   - `API_HOST`: `0.0.0.0`
   - `API_PORT`: Use Render's `$PORT` variable
   - Add Google Cloud credentials if using real TTS/STT
6. Deploy and copy your backend URL
7. Update Netlify environment variable with this URL

### Option 2: Railway.app

1. Sign up at [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Configure:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables
5. Deploy and get your URL
6. Update Netlify with backend URL

### Option 3: Google Cloud Run

```bash
# From project root
cd backend
gcloud run deploy dutch-ai-voice-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 4: Your Own Server

```bash
# On your server
git clone <your-repo>
cd Dutch-AI-Voice-Assistant/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Use nginx as a reverse proxy to expose it securely.

---

## 🔧 Configuration

### Setting Backend URL in Netlify

**Option A: Environment Variable (Recommended)**

1. Go to Netlify Site Settings
2. Navigate to Environment Variables
3. Add `BACKEND_API_URL` with your backend URL
4. Trigger a redeploy

**Option B: Manual Configuration**

Edit `frontend/env-config.js`:
```javascript
window.BACKEND_API_URL = 'https://your-backend.onrender.com';
```

Commit and push changes.

---

## 🧪 Testing Your Deployment

### Test Frontend

1. Visit your Netlify URL
2. Page should load without 404 errors
3. Console should show API Base URL

### Test Backend Connection

1. Click "New Call" tab
2. Enter a test user ID
3. Click "Start Call"
4. Should see success message with call ID
5. Check "Active Calls" - should show the new call
6. Click "Overview" and "Refresh Stats" - should show statistics

### Common Issues

**404 Error**: 
- Ensure `netlify.toml` is present in the repository root
- Check that the publish directory is set to `frontend`
- Verify the build completed successfully in Netlify dashboard

**API Connection Failed**:
- Verify backend is running
- Check `BACKEND_API_URL` environment variable is set correctly
- Verify CORS is enabled on backend (should be by default)
- Check browser console for actual API URL being used

**Backend Not Found**:
- Backend must be deployed separately
- Backend URL must be accessible from the internet
- Check backend health: `curl https://your-backend-url/health`

---

## 📁 Repository Structure

```
Dutch-AI-Voice-Assistant/
├── frontend/           # Static files (deployed to Netlify)
│   ├── index.html
│   ├── app.js
│   ├── config.js
│   ├── env-config.js
│   ├── style.css
│   └── setup.html     # Setup instructions page
├── backend/           # FastAPI app (deploy separately)
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── netlify.toml       # Netlify configuration
├── build.js           # Build script to inject env vars
└── README.md
```

---

## 🔄 Updating Your Deployment

### Update Frontend

1. Make changes to frontend files
2. Commit and push to GitHub
3. Netlify auto-deploys on push to main branch

### Update Backend

1. Make changes to backend files
2. Commit and push to GitHub
3. Backend platform (Render/Railway) auto-deploys

---

## 🌍 Custom Domain

### Add Custom Domain to Netlify

1. Go to Site Settings
2. Navigate to Domain Management
3. Add your custom domain
4. Follow DNS configuration instructions

### Update Backend URL

If using custom domain for backend:
1. Update `BACKEND_API_URL` in Netlify
2. Trigger a redeploy

---

## 🔒 Security Considerations

- Never commit credentials or API keys
- Use environment variables for sensitive data
- Enable HTTPS on both frontend and backend
- Configure CORS properly on backend
- Use strong authentication if deploying to production

---

## 📊 Monitoring

### Netlify Dashboard

- View deployment logs
- Monitor performance
- Check analytics

### Backend Monitoring

- Check backend platform logs
- Monitor API response times
- Set up alerts for downtime

---

## 🆘 Troubleshooting

### Frontend Shows 404

1. Check `netlify.toml` exists in repository root
2. Verify publish directory is set to `frontend`
3. Check build logs in Netlify dashboard
4. Ensure `frontend/` directory exists with files

### Backend Connection Issues

1. Verify backend is running:
   ```bash
   curl https://your-backend-url/health
   ```
2. Check backend logs for errors
3. Verify CORS settings allow your Netlify domain
4. Test backend independently before connecting frontend

### Build Fails

1. Check `build.js` syntax
2. Ensure Node.js is available (Netlify default)
3. Review build logs in Netlify dashboard

---

## 💡 Tips

- Use Netlify Preview Deployments for testing changes
- Set up different backend URLs for production vs preview using branch-specific environment variables
- Monitor usage on free tiers (both Netlify and backend platform)
- Consider using Netlify Analytics for insights

---

## 📚 Additional Resources

- [Netlify Documentation](https://docs.netlify.com)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Project README](./README.md)
- [Full Deployment Guide](./DEPLOYMENT.md)
- [Vercel Deployment Guide](./VERCEL_DEPLOYMENT.md)

---

## ✅ Deployment Checklist

- [ ] Repository forked/cloned to GitHub
- [ ] Backend deployed to hosting platform
- [ ] Backend health endpoint accessible
- [ ] Netlify account created
- [ ] Project imported to Netlify
- [ ] `BACKEND_API_URL` environment variable set
- [ ] Frontend deployed successfully
- [ ] Visited Netlify URL - no 404 error
- [ ] Tested creating a call
- [ ] Dashboard shows statistics
- [ ] All features working correctly

---

**🎉 Congratulations! Your Dutch AI Voice Assistant is now live on Netlify!**

For issues or questions, please open an issue on GitHub.
