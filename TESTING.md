# Testing Guide - Dutch AI Voice Assistant

Comprehensive testing documentation for the Dutch AI Voice Assistant project.

## Quick Start

### Prerequisites
```bash
cd backend
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Modules
```bash
# Test Call Manager
pytest tests/test_call_manager.py -v

# Test Conversation Flows
pytest tests/test_flows.py -v
```

### Run Individual Test
```bash
pytest tests/test_call_manager.py::test_create_call -v
```

## Test Coverage

### 1. Call Manager Tests (`test_call_manager.py`)
- **test_create_call**: Verifies call creation and initialization
- **test_add_conversation_turn**: Tests adding user/assistant turns
- **test_end_call**: Validates call termination and summary
- **test_get_call_summary**: Checks call summary retrieval
- **test_get_all_active_calls**: Tests listing active calls
- **test_singleton**: Verifies singleton pattern implementation

### 2. Conversation Flows Tests (`test_flows.py`)
- **Lifestyle Coach Flow**: Tests friendly, casual voice interactions
  - Greetings in Dutch
  - Context-aware responses (stress, exercise, sleep)
  - Natural closings
- **Business Call Flow**: Tests professional voice interactions
  - Professional greetings
  - Call routing and data collection
  - Business-appropriate closings

## Running Tests Locally

### Setup Environment
```bash
# Clone repository
git clone https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant.git
cd Dutch-AI-Voice-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

### Configure Environment
```bash
# Copy and configure .env file
cp .env.example .env

# Edit .env with your Google Cloud credentials
echo "GOOGLE_CLOUD_CREDENTIALS=path/to/credentials.json" >> .env
echo "DATABASE_URL=sqlite:///./test.db" >> .env
```

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=backend --cov-report=html

# Async tests only
pytest tests/test_flows.py -v -s
```

## Test Results

Expected output:
```
tests/test_call_manager.py::test_create_call PASSED
tests/test_call_manager.py::test_add_conversation_turn PASSED
tests/test_call_manager.py::test_end_call PASSED
tests/test_call_manager.py::test_get_call_summary PASSED
tests/test_call_manager.py::test_get_all_active_calls PASSED
tests/test_call_manager.py::test_singleton PASSED
tests/test_flows.py::test_lifestyle_greeting PASSED
tests/test_flows.py::test_business_greeting PASSED
...

====== 8 passed in 0.45s ======
```

## Integration Testing

### Manual API Testing
```bash
# Start backend
cd backend
python main.py

# In another terminal, test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/calls -H "Content-Type: application/json" -d '{"user_id": "test_user", "voice_profile": "lifestyle"}'
curl http://localhost:8000/stats
```

### WebSocket Testing
Use a WebSocket client to connect to:
```
ws://localhost:8000/ws/call/{call_id}
```

Send messages:
```json
{"text": "Hallo, hoe gaat het?"}
```

## Dashboard Testing

### Start Frontend
```bash
cd frontend
# Serve the HTML file using a simple server
python -m http.server 3000
```

Access at: `http://localhost:3000`

### Test Flows
1. **Overview Tab**: Check stats display
2. **Active Calls**: Create a call and verify it appears
3. **Transcripts**: Search for call ID and view transcript
4. **New Call**: Create calls with different voice profiles

## Docker Testing

### Build and Run
```bash
docker-compose up --build
```

### Run Tests in Container
```bash
docker-compose exec backend pytest tests/ -v
```

## Continuous Integration

Add to GitHub Actions (`.github/workflows/tests.yml`):
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install pytest pytest-asyncio
      - run: cd backend && pip install -r requirements.txt
      - run: pytest tests/ -v
```

## Troubleshooting

### Import Errors
- Ensure `PYTHONPATH` includes backend directory
- Check that `__init__.py` exists in test and backend directories

### Async Test Failures
- Install `pytest-asyncio`: `pip install pytest-asyncio`
- Use `asyncio.run()` for main entry points

### Google Cloud Errors
- Verify credentials file path in `.env`
- Check that credentials have proper permissions
- In test mode, mock clients are available

## Performance Benchmarks

- Call creation: < 10ms
- Conversation turn: < 50ms
- Call ending: < 20ms
- WebSocket message: < 100ms

## Next Steps

- Add voice quality tests
- Implement load testing for concurrent calls
- Add user acceptance testing scenarios
- Create performance profiling suite
