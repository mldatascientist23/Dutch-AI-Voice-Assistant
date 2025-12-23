"""Call Manager - Manages call lifecycle and state"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

class CallManager:
    """Manages call state and lifecycle"""
    
    def __init__(self):
        self.active_calls: Dict[str, dict] = {}
    
    def create_call(self, user_id: str, voice_profile: str) -> str:
        """Create a new call record"""
        try:
            call_id = str(uuid.uuid4())
            
            self.active_calls[call_id] = {
                "user_id": user_id,
                "voice_profile": voice_profile,
                "status": "active",
                "start_time": datetime.utcnow(),
                "turns": [],
                "transcript": []
            }
            
            logger.info(f"Call created: {call_id} for user {user_id}")
            return call_id
            
        except Exception as e:
            logger.error(f"Error creating call: {e}")
            raise
    
    def add_conversation_turn(self, call_id: str, role: str, text: str, confidence: float = 1.0):
        """Add a conversation turn to a call"""
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            turn_id = str(uuid.uuid4())
            
            turn_data = {
                "turn_id": turn_id,
                "role": role,
                "text": text,
                "confidence": confidence if role == "user" else 1.0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.active_calls[call_id]["turns"].append(turn_data)
            self.active_calls[call_id]["transcript"].append(f"{role}: {text}")
            self.active_calls[call_id]["status"] = "active"
            
            logger.info(f"Turn added to call {call_id}: {role}")
            
        except Exception as e:
            logger.error(f"Error adding conversation turn: {e}")
            raise
    
    def end_call(self, call_id: str) -> dict:
        """End a call and save final data"""
        try:
            if call_id not in self.active_calls:
                raise ValueError(f"Call {call_id} not found")
            
            call_info = self.active_calls[call_id]
            end_time = datetime.utcnow()
            start_time = call_info["start_time"]
            duration = (end_time - start_time).total_seconds()
            
            summary = {
                "call_id": call_id,
                "status": "completed",
                "duration": duration,
                "turns": len(call_info["turns"]),
                "user_id": call_info["user_id"],
                "voice_profile": call_info["voice_profile"],
                "end_time": end_time.isoformat()
            }
            
            del self.active_calls[call_id]
            logger.info(f"Call ended: {call_id}, duration: {duration}s")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error ending call: {e}")
            raise
    
    def get_call_summary(self, call_id: str) -> Optional[dict]:
        """Get summary of a call"""
        try:
            if call_id not in self.active_calls:
                return None
            
            call_info = self.active_calls[call_id]
            
            return {
                "call_id": call_id,
                "user_id": call_info["user_id"],
                "voice_profile": call_info["voice_profile"],
                "status": call_info["status"],
                "start_time": call_info["start_time"].isoformat(),
                "turns_count": len(call_info["turns"]),
                "transcript": "\\n".join(call_info["transcript"])
            }
        except Exception as e:
            logger.error(f"Error getting call summary: {e}")
            return None
    
    def get_all_active_calls(self) -> List[dict]:
        """Get list of all active calls"""
        return [
            {
                "call_id": call_id,
                "user_id": info["user_id"],
                "voice_profile": info["voice_profile"],
                "status": info["status"]
            }
            for call_id, info in self.active_calls.items()
        ]

_call_manager: Optional[CallManager] = None

def get_call_manager() -> CallManager:
    """Get or create call manager instance"""
    global _call_manager
    if _call_manager is None:
        _call_manager = CallManager()
    return _call_manager
