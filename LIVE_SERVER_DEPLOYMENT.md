# Live Server Deployment Guide

## 🚀 Complete Guide for Production Deployment

This guide provides instructions to deploy the Dutch AI Voice Assistant on a live server (VPS, cloud instance, or dedicated server).

---

## ✅ What's New - Production Ready

The application has been updated to work seamlessly on live servers:

- **✅ Dynamic API Configuration**: Frontend automatically detects and connects to backend
- **✅ Nginx Reverse Proxy**: Professional routing and API proxying
- **✅ Docker Support**: One-command deployment with docker-compose
- **✅ WebSocket Support**: Real-time communication properly configured
- **✅ Production Security**: Proper headers and CORS configuration

---

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed on your server
- **Open Ports**: 80 (HTTP) or 443 (HTTPS), and optionally 3000 for testing
- **Domain Name** (optional, but recommended for production)
- **Google Cloud Credentials** (optional for production TTS/STT)

---

## 🔧 Quick Deployment with Docker

### Option 1: Standard Deployment (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant.git
cd Dutch-AI-Voice-Assistant

# 2. (Optional) Add Google Cloud credentials
# Copy your credentials.json to the project root
cp /path/to/your/credentials.json ./credentials.json

# 3. Start all services
docker-compose up -d --build

# 4. Check if services are running
docker-compose ps

# 5. Access the application
# Open http://your-server-ip:3000 in your browser
```

That's it! The application is now running on your server.

### Option 2: Production Port 80

To run on standard HTTP port 80:

```bash
# Edit docker-compose.yml and change frontend port
# Change "3000:80" to "80:80"

# Then start services
docker-compose up -d --build
```

Access at: `http://your-server-ip` or `http://yourdomain.com`

---

## 🔍 Verify Deployment

### 1. Check Backend Health

```bash
curl http://your-server-ip:3000/health
```

Expected response:
```json
{"status":"healthy","service":"Dutch AI Voice Assistant"}
```

### 2. Check Frontend

Open your browser to:
```
http://your-server-ip:3000
```

You should see the **Dutch AI Voice Assistant Dashboard**.

### 3. Test API Through Nginx

```bash
curl http://your-server-ip:3000/api/health
```

This tests the nginx proxy configuration.

---

## 🌐 How It Works

### Architecture

```
[Browser] → [Nginx :80] → [Frontend Static Files]
                ↓
            [/api/*] → [Backend :8000]
                ↓
            [/ws/*]  → [WebSocket Backend]
```

### Dynamic API Configuration

The frontend automatically detects the environment:

- **Port 80/443**: Uses `/api/` prefix (nginx proxy)
- **Port 3000+**: Uses `/api/` prefix (nginx proxy)
- **localhost with custom port**: Direct connection to `http://localhost:8000`

This allows seamless deployment without hardcoded URLs!

---

## 📝 Configuration Options

### Environment Variables

Create a `.env` file in the project root:

```env
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./voice_assistant.db

# Google Cloud (Optional)
GOOGLE_CLOUD_CREDENTIALS=./credentials.json

# Logging
LOG_LEVEL=INFO
```

### Update docker-compose.yml

```yaml
services:
  backend:
    environment:
      - DATABASE_URL=sqlite:///./voice_assistant.db
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - LOG_LEVEL=INFO
```

---

## 🔒 Production Security

### Enable HTTPS with Let's Encrypt

1. Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. Get SSL Certificate:
```bash
sudo certbot --nginx -d yourdomain.com
```

3. Update nginx.conf to redirect HTTP to HTTPS:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of nginx configuration
}
```

### Update CORS for Production

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Issue: Can't connect to backend

**Solution**: Check if backend is running:
```bash
docker-compose logs backend
```

### Issue: Frontend shows but API calls fail

**Solution**: Check nginx logs:
```bash
docker-compose logs frontend
```

Verify nginx proxy is working:
```bash
curl http://localhost:3000/api/health
```

### Issue: Port already in use

**Solution**: Stop existing services:
```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :8000

# Stop docker-compose services
docker-compose down

# Or change ports in docker-compose.yml
```

### Issue: Database errors

**Solution**: Reset the database:
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d --build
```

---

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Check Resource Usage

```bash
docker stats
```

---

## 🔄 Updates and Maintenance

### Update to Latest Version

```bash
cd Dutch-AI-Voice-Assistant
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Backup Database

```bash
docker exec dutch-voice-backend cp /app/voice_assistant.db /app/backup.db
docker cp dutch-voice-backend:/app/backup.db ./voice_assistant_backup.db
```

### Restore Database

```bash
docker cp ./voice_assistant_backup.db dutch-voice-backend:/app/voice_assistant.db
docker-compose restart backend
```

---

## 🎯 Testing the Live Deployment

### Test 1: Create a Call

```bash
curl -X POST http://your-server-ip:3000/api/calls \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "voice_profile": "lifestyle"}'
```

### Test 2: Get Statistics

```bash
curl http://your-server-ip:3000/api/stats
```

### Test 3: List Calls

```bash
curl http://your-server-ip:3000/api/calls
```

### Test 4: Use the Dashboard

1. Open `http://your-server-ip:3000`
2. Go to "New Call" tab
3. Enter a User ID
4. Select a voice profile
5. Click "Start Call"
6. Check "Overview" tab for updated statistics

---

## 📱 Mobile Access

The dashboard is fully responsive. Access from any device:

```
http://your-server-ip:3000
```

Or with domain:

```
https://yourdomain.com
```

---

## 🚦 Health Checks

Monitor your deployment:

```bash
# Backend health
curl http://your-server-ip:3000/health

# Get stats
curl http://your-server-ip:3000/api/stats

# Check Docker status
docker-compose ps
```

---

## 📧 Support

For issues:

1. Check logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Test API endpoints with curl
4. Open an issue on [GitHub](https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant/issues)

---

## ✅ Deployment Checklist

- [ ] Server has Docker and Docker Compose installed
- [ ] Ports 80 or 3000 are open and available
- [ ] Repository cloned to server
- [ ] (Optional) Google Cloud credentials added
- [ ] `docker-compose up -d --build` executed successfully
- [ ] All services showing as "Up" in `docker-compose ps`
- [ ] Backend health check passing
- [ ] Frontend accessible in browser
- [ ] API calls working through nginx proxy
- [ ] Dashboard functioning properly
- [ ] (Production) HTTPS configured
- [ ] (Production) Domain name configured
- [ ] (Production) CORS updated for specific domain
- [ ] (Production) Monitoring and logging set up

---

## 🎉 Success!

Your Dutch AI Voice Assistant is now live and fully functional on your server!

**Access Points:**
- Dashboard: `http://your-server-ip:3000` (or `http://yourdomain.com`)
- API Docs: `http://your-server-ip:3000/api/docs`
- Health: `http://your-server-ip:3000/health`

**Next Steps:**
1. Configure your domain name
2. Enable HTTPS with Let's Encrypt
3. Set up monitoring and backups
4. Customize voice profiles
5. Add Google Cloud credentials for production TTS/STT
