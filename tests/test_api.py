"""Test FastAPI endpoints"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data

def test_create_call():
    """Test creating a call"""
    response = client.post(
        "/calls",
        json={"user_id": "test_user", "voice_profile": "lifestyle"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "call_id" in data
    assert data["status"] == "initiated"
    assert data["voice_profile"] == "lifestyle"

def test_list_calls():
    """Test listing calls"""
    # Create a call first
    client.post("/calls", json={"user_id": "user1", "voice_profile": "business"})
    
    response = client.get("/calls")
    assert response.status_code == 200
    data = response.json()
    assert "active_calls" in data
    assert "calls" in data

def test_get_stats():
    """Test statistics endpoint"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_calls" in data
    assert "active_calls" in data
    assert "completed_calls" in data
    assert "average_duration" in data

def test_invalid_call_id():
    """Test error handling for invalid call ID"""
    response = client.get("/calls/invalid_id")
    assert response.status_code == 404

if __name__ == "__main__":
    test_health_check()
    test_create_call()
    test_list_calls()
    test_get_stats()
    test_invalid_call_id()
    print("All API tests passed!")
