# Dutch AI Voice Assistant - Deployment Guide

## 🚀 Complete Deployment Instructions

This guide provides step-by-step instructions to deploy the Dutch AI Voice Assistant on any system.

---

## 📋 Prerequisites

Before deploying, ensure you have:

- **Python 3.9+** installed
- **pip** package manager
- **Google Cloud Account** (for TTS/STT services)
- **Git** installed
- **Port 8000** (backend) and **Port 3000** (frontend) available

---

## 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant.git
cd Dutch-AI-Voice-Assistant
```

---

## 🔑 Step 2: Google Cloud Setup (Optional for Testing)

### For Production Use:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API
4. Create a service account:
   - Navigate to **IAM & Admin** → **Service Accounts**
   - Click **Create Service Account**
   - Grant roles: **Cloud Speech Client** and **Cloud Text to Speech Client**
5. Download the JSON credentials file
6. Save it as `credentials.json` in the `backend/` directory

### For Testing (Mock Mode):

The application includes mock credentials for testing without Google Cloud. You can skip the Google Cloud setup and the app will run in mock mode.

---

## 🐍 Step 3: Backend Setup

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure Environment

```bash
# Copy the example environment file
cp ../.env.example .env

# Edit .env file (optional - defaults work for testing)
nano .env
```

### Key Environment Variables:

```env
DATABASE_URL=sqlite:///./voice_assistant.db
API_HOST=0.0.0.0
API_PORT=8000
GOOGLE_CLOUD_CREDENTIALS=./credentials.json
SPEECH_LANGUAGE=nl-NL
SAMPLE_RATE=16000
```

### Initialize Database

The database will be created automatically on first run.

---

## ▶️ Step 4: Start the Backend Server

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Verify Backend is Running

Open a new terminal and test:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"Dutch AI Voice Assistant"}
```

---

## 🌐 Step 5: Start the Frontend Dashboard

Open a new terminal:

```bash
cd frontend
python -m http.server 3000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

---

## 🎉 Step 6: Access the Dashboard

Open your web browser and navigate to:

```
http://localhost:3000
```

You should see the **Dutch AI Voice Assistant Dashboard**!

---

## 🧪 Step 7: Test the Application

### Test 1: Create a Lifestyle Coach Call

1. Click on **"New Call"** tab
2. Enter User ID: `test_user_1`
3. Select Voice Profile: **"Lifestyle Coach (Friendly)"**
4. Click **"Start Call"**
5. You should see: `Call created! ID: [unique-id]`

### Test 2: Create a Business Service Call

1. Stay on **"New Call"** tab
2. Enter User ID: `business_user_1`
3. Select Voice Profile: **"Business Service (Professional)"**
4. Click **"Start Call"**

### Test 3: View Active Calls

1. Click on **"Active Calls"** tab
2. Click **"Refresh Calls"**
3. You should see all created calls with their status

### Test 4: Check Dashboard Statistics

1. Click on **"Overview"** tab
2. Click **"Refresh Stats"**
3. View real-time statistics:
   - Total Calls
   - Active Calls
   - Completed Calls
   - Average Duration
   - Total Minutes

---

## 🐳 Docker Deployment (Alternative)

### Option A: Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Option B: Manual Docker Build

```bash
# Build backend image
docker build -t dutch-ai-voice-backend .

# Run backend container
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./voice_assistant.db \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=8000 \
  dutch-ai-voice-backend

# Serve frontend (use nginx or any web server)
docker run -p 3000:80 \
  -v $(pwd)/frontend:/usr/share/nginx/html:ro \
  nginx:alpine
```

---

## 🔍 Testing API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Create a Call
```bash
curl -X POST http://localhost:8000/calls \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "voice_profile": "lifestyle"}'
```

### List All Calls
```bash
curl http://localhost:8000/calls
```

### Get Dashboard Stats
```bash
curl http://localhost:8000/stats
```

### Get Call Details
```bash
curl http://localhost:8000/calls/{call_id}
```

### Get Call Transcript
```bash
curl http://localhost:8000/calls/{call_id}/transcript
```

### End a Call
```bash
curl -X DELETE http://localhost:8000/calls/{call_id}
```

---

## 🧪 Running Tests

### Run All Tests
```bash
cd /path/to/Dutch-AI-Voice-Assistant
pytest tests/ -v
```

### Run Specific Test Modules
```bash
# API tests
pytest tests/test_api.py -v

# Conversation flow tests
pytest tests/test_flows.py -v

# Call manager tests
pytest tests/test_call_manager.py -v

# TTS/STT tests
pytest tests/test_tts.py -v
pytest tests/test_stt.py -v
```

### Test with Coverage
```bash
pytest tests/ -v --cov=backend --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

---

## 🔒 Production Deployment

### Security Checklist

- [ ] Use HTTPS/SSL certificates
- [ ] Secure API endpoints with authentication
- [ ] Use environment variables for sensitive data
- [ ] Enable CORS only for trusted domains
- [ ] Use a production WSGI server (e.g., Gunicorn)
- [ ] Set up proper logging and monitoring
- [ ] Use PostgreSQL instead of SQLite
- [ ] Implement rate limiting
- [ ] Enable request validation
- [ ] Regular security updates

### Production Environment Variables

```env
# Production settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@localhost:5432/voice_assistant

# Google Cloud credentials
GOOGLE_CLOUD_CREDENTIALS=/path/to/production/credentials.json

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/voice_assistant/app.log
```

### Using Gunicorn (Production Server)

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/voice_assistant/access.log \
  --error-logfile /var/log/voice_assistant/error.log
```

### Nginx Configuration (Frontend)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/Dutch-AI-Voice-Assistant/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Issue: Google Cloud Authentication Error

```bash
# Set credentials path explicitly
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### Issue: Module Not Found

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/Dutch-AI-Voice-Assistant/backend:$PYTHONPATH
```

### Issue: Database Connection Error

```bash
# Check if database file exists and has write permissions
ls -la backend/voice_assistant.db
chmod 644 backend/voice_assistant.db
```

### Issue: Frontend Not Loading

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Ensure allow_origins includes your frontend URL
```

---

## 📊 Performance Tuning

### Backend Optimization

1. **Use connection pooling** for database
2. **Enable response compression**
3. **Implement caching** for frequent queries
4. **Use async operations** throughout
5. **Monitor with tools** like Prometheus

### Database Optimization

```python
# For PostgreSQL in production
DATABASE_URL=postgresql://user:password@localhost:5432/voice_assistant?pool_size=20&max_overflow=0
```

---

## 🔄 Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Server
        run: |
          ssh user@server "cd /app && git pull && docker-compose up -d --build"
```

---

## 📱 Mobile Access

The dashboard is fully responsive and works on mobile devices. Simply access:

```
http://your-server-ip:3000
```

from any mobile browser.

---

## 🆘 Support

For issues or questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [README.md](README.md)
3. Open an issue on [GitHub](https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant/issues)

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## ✅ Deployment Checklist

- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Configure environment variables
- [ ] Set up Google Cloud credentials (or use mock mode)
- [ ] Start backend server
- [ ] Start frontend server
- [ ] Access dashboard at http://localhost:3000
- [ ] Test API endpoints
- [ ] Run test suite
- [ ] Verify all features work
- [ ] (Optional) Configure production deployment
- [ ] (Optional) Set up monitoring and logging

---

**🎉 Congratulations! Your Dutch AI Voice Assistant is now deployed and ready to use!**
