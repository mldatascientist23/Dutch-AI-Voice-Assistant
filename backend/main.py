from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import CallCreate, CallResponse, DashboardStatsResponse
from conversation_flows import ConversationFlowManager, VoiceProfile
import logging
import uuid
from datetime import datetime
from config import settings
from contextlib import asynccontextmanager

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

active_calls = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    try:
        init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    yield
    # Cleanup on shutdown
    logger.info("Application shutting down")

app = FastAPI(
    title="Dutch AI Voice Assistant",
    description="Real-time Dutch voice AI assistant with web dashboard",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Dutch AI Voice Assistant"}

@app.post("/calls", response_model=dict)
async def create_call(call_data: CallCreate, db: Session = Depends(get_db)):
    """Create a new call session"""
    try:
        call_id = str(uuid.uuid4())
        flow_manager = ConversationFlowManager(
            profile=VoiceProfile(call_data.voice_profile)
        )
        active_calls[call_id] = {
            "user_id": call_data.user_id,
            "voice_profile": call_data.voice_profile,
            "start_time": datetime.utcnow(),
            "flow_manager": flow_manager,
            "transcript": [],
            "status": "active"
        }
        logger.info(f"Call created: {call_id} for user {call_data.user_id}")
        return {
            "call_id": call_id,
            "status": "initiated",
            "voice_profile": call_data.voice_profile
        }
    except Exception as e:
        logger.error(f"Error creating call: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calls")
async def list_calls():
    """List all active calls"""
    return {
        "active_calls": len(active_calls),
        "calls": [
            {
                "call_id": call_id,
                "user_id": call["user_id"],
                "voice_profile": call["voice_profile"],
                "status": call["status"]
            }
            for call_id, call in active_calls.items()
        ]
    }

@app.get("/calls/{call_id}")
async def get_call(call_id: str):
    """Get specific call details"""
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = active_calls[call_id]
    return {
        "call_id": call_id,
        "user_id": call["user_id"],
        "voice_profile": call["voice_profile"],
        "status": call["status"],
        "start_time": call["start_time"],
        "transcript_turns": len(call["transcript"])
    }

@app.get("/calls/{call_id}/transcript")
async def get_transcript(call_id: str):
    """Get call transcript"""
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = active_calls[call_id]
    return {
        "call_id": call_id,
        "transcript": call["transcript"]
    }

@app.delete("/calls/{call_id}")
async def end_call(call_id: str):
    """End a call session"""
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = active_calls[call_id]
    duration = (datetime.utcnow() - call["start_time"]).total_seconds()
    call["status"] = "completed"
    call["duration"] = duration
    
    logger.info(f"Call ended: {call_id}, duration: {duration}s")
    
    return {
        "call_id": call_id,
        "status": "completed",
        "duration": duration
    }

@app.get("/stats", response_model=DashboardStatsResponse)
async def get_stats():
    """Get dashboard statistics"""
    total = len(active_calls)
    active = sum(1 for c in active_calls.values() if c["status"] == "active")
    completed = sum(1 for c in active_calls.values() if c["status"] == "completed")
    
    total_minutes = sum(
        c.get("duration", 0) / 60
        for c in active_calls.values()
        if "duration" in c
    )
    
    avg_duration = total_minutes / max(completed, 1) if completed > 0 else 0
    
    return DashboardStatsResponse(
        total_calls=total,
        active_calls=active,
        completed_calls=completed,
        average_duration=avg_duration,
        total_conversation_minutes=total_minutes
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
