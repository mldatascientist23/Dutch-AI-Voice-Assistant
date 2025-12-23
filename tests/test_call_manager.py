"""Test Call Manager module"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from call_manager import CallManager, get_call_manager

def test_create_call():
    """Test call creation"""
    manager = CallManager()
    call_id = manager.create_call("user_123", "lifestyle")
    assert call_id is not None
    assert call_id in manager.active_calls
    assert manager.active_calls[call_id]["user_id"] == "user_123"

def test_add_conversation_turn():
    """Test adding conversation turn"""
    manager = CallManager()
    call_id = manager.create_call("user_123", "business")
    manager.add_conversation_turn(call_id, "user", "Hello")
    assert len(manager.active_calls[call_id]["turns"]) == 1
    manager.add_conversation_turn(call_id, "assistant", "Hi there!")
    assert len(manager.active_calls[call_id]["turns"]) == 2

def test_end_call():
    """Test ending call"""
    manager = CallManager()
    call_id = manager.create_call("user_123", "lifestyle")
    manager.add_conversation_turn(call_id, "user", "Test")
    summary = manager.end_call(call_id)
    assert summary["status"] == "completed"
    assert summary["turns"] == 1
    assert call_id not in manager.active_calls

def test_get_call_summary():
    """Test get call summary"""
    manager = CallManager()
    call_id = manager.create_call("user_456", "business")
    manager.add_conversation_turn(call_id, "user", "Help")
    summary = manager.get_call_summary(call_id)
    assert summary is not None
    assert summary["user_id"] == "user_456"
    assert summary["voice_profile"] == "business"

def test_get_all_active_calls():
    """Test get all active calls"""
    manager = CallManager()
    call1 = manager.create_call("user_1", "lifestyle")
    call2 = manager.create_call("user_2", "business")
    calls = manager.get_all_active_calls()
    assert len(calls) == 2
    assert any(c["call_id"] == call1 for c in calls)

def test_singleton():
    """Test CallManager singleton pattern"""
    manager1 = get_call_manager()
    manager2 = get_call_manager()
    assert manager1 is manager2

if __name__ == "__main__":
    test_create_call()
    test_add_conversation_turn()
    test_end_call()
    test_get_call_summary()
    test_get_all_active_calls()
    test_singleton()
    print("All call_manager tests passed!")
