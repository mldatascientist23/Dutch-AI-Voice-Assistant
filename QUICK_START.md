# 🚀 Quick Reference Guide

## Dutch AI Voice Assistant - Essential Commands

### 🏁 Getting Started (5 Minutes)

```bash
# 1. Clone
git clone https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant.git
cd Dutch-AI-Voice-Assistant

# 2. Install
cd backend
pip install -r requirements.txt

# 3. Run Backend
python main.py
# Backend runs on http://localhost:8000

# 4. Run Frontend (new terminal)
cd ../frontend
python -m http.server 3000
# Dashboard at http://localhost:3000
```

---

## 📡 API Quick Reference

### Base URL
```
http://localhost:8000
```

### Essential Endpoints

**Health Check**
```bash
curl http://localhost:8000/health
```

**Create Call**
```bash
curl -X POST http://localhost:8000/calls \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "voice_profile": "lifestyle"}'
```

**List Calls**
```bash
curl http://localhost:8000/calls
```

**Get Stats**
```bash
curl http://localhost:8000/stats
```

**Get Call Details**
```bash
curl http://localhost:8000/calls/{call_id}
```

**Get Transcript**
```bash
curl http://localhost:8000/calls/{call_id}/transcript
```

**End Call**
```bash
curl -X DELETE http://localhost:8000/calls/{call_id}
```

---

## 🧪 Testing Commands

**Run All Tests**
```bash
pytest tests/ -v
```

**Run Specific Test**
```bash
pytest tests/test_api.py -v
```

**With Coverage**
```bash
pytest tests/ --cov=backend --cov-report=html
```

---

## 🐳 Docker Commands

**Start All Services**
```bash
docker-compose up -d
```

**View Logs**
```bash
docker-compose logs -f
```

**Stop Services**
```bash
docker-compose down
```

**Rebuild**
```bash
docker-compose up --build
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Required
DATABASE_URL=sqlite:///./voice_assistant.db
API_HOST=0.0.0.0
API_PORT=8000

# Optional (for Google Cloud TTS/STT)
GOOGLE_CLOUD_CREDENTIALS=./credentials.json
SPEECH_LANGUAGE=nl-NL
```

---

## 🎤 Voice Profiles

### Lifestyle (Friendly)
```json
{
  "user_id": "user123",
  "voice_profile": "lifestyle"
}
```
**Use for:** Health coaching, wellness, casual conversations

### Business (Professional)
```json
{
  "user_id": "user456",
  "voice_profile": "business"
}
```
**Use for:** Customer service, appointments, professional calls

---

## 📊 Dashboard URLs

- **Main Dashboard:** http://localhost:3000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Interactive API:** http://localhost:8000/redoc

---

## 🔧 Troubleshooting

**Port Already in Use**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

**Module Not Found**
```bash
# Set Python path
export PYTHONPATH=/path/to/Dutch-AI-Voice-Assistant/backend:$PYTHONPATH
```

**Database Error**
```bash
# Remove and recreate
rm backend/voice_assistant.db
python backend/main.py
```

---

## 📁 Project Structure

```
Dutch-AI-Voice-Assistant/
├── backend/              # FastAPI application
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── voice_manager.py # TTS/STT
│   └── conversation_flows.py  # Dialog logic
├── frontend/            # Web dashboard
│   ├── index.html       # Main page
│   ├── style.css        # Styles
│   └── app.js           # Logic
├── tests/               # Test suite
├── DEPLOYMENT.md        # Full deployment guide
├── TEST_RESULTS.md      # Test verification
└── README.md            # Main documentation
```

---

## 🎯 Common Tasks

### Create and Test a Call

```bash
# 1. Create call
CALL_ID=$(curl -s -X POST http://localhost:8000/calls \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","voice_profile":"lifestyle"}' | jq -r '.call_id')

# 2. Get call details
curl http://localhost:8000/calls/$CALL_ID

# 3. End call
curl -X DELETE http://localhost:8000/calls/$CALL_ID
```

### Monitor System

```bash
# Watch stats (updates every 2 seconds)
watch -n 2 'curl -s http://localhost:8000/stats | jq .'
```

### Run Continuous Tests

```bash
# Watch mode (requires pytest-watch)
ptw tests/ -v
```

---

## 📚 Documentation Links

- **Full README:** [README.md](README.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Test Results:** [TEST_RESULTS.md](TEST_RESULTS.md)
- **Testing Guide:** [TESTING.md](TESTING.md)
- **Complete Summary:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## ✅ Verification Checklist

Before going live, verify:

- [ ] Backend starts: `curl http://localhost:8000/health`
- [ ] Frontend loads: Open http://localhost:3000
- [ ] Can create call via API
- [ ] Dashboard shows statistics
- [ ] Tests pass: `pytest tests/ -v`

---

## 🆘 Quick Help

**Problem:** Can't access dashboard  
**Solution:** Check both backend (8000) and frontend (3000) are running

**Problem:** Tests failing  
**Solution:** `pip install -r backend/requirements.txt`

**Problem:** Google Cloud errors  
**Solution:** App works in mock mode without credentials

---

## 🎉 Success Indicators

✅ Health endpoint returns `{"status": "healthy"}`  
✅ Dashboard loads at http://localhost:3000  
✅ Can create calls via UI  
✅ Statistics display correctly  
✅ All tests pass (28/28)

---

**🚀 You're ready to use the Dutch AI Voice Assistant!**

For detailed information, see [DEPLOYMENT.md](DEPLOYMENT.md)
