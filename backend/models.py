from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

Base = declarative_base()

class CallRecord(Base):
    """Database model for call records"""
    __tablename__ = "calls"
    
    call_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    voice_profile = Column(String, default="lifestyle")
    status = Column(String, default="initiated")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Float, default=0.0)
    transcript = Column(Text, default="")
    audio_path = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ConversationTurn(Base):
    """Database model for conversation turns"""
    __tablename__ = "conversation_turns"
    
    turn_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    call_id = Column(String, ForeignKey('calls.call_id'), index=True)
    role = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, nullable=True)

class VoiceProfile(Base):
    """Database model for voice profiles"""
    __tablename__ = "voice_profiles"
    
    profile_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    profile_type = Column(String)
    tts_voice = Column(String)
    pitch = Column(Float, default=0.0)
    rate = Column(Float, default=1.0)
    created_at = Column(DateTime, server_default=func.now())

class CallCreate(BaseModel):
    """Schema for creating a new call"""
    user_id: str
    voice_profile: str = "lifestyle"

class ConversationTurnSchema(BaseModel):
    """Schema for conversation turn"""
    role: str
    text: str
    confidence: Optional[float] = None

class CallResponse(BaseModel):
    """Schema for call response"""
    call_id: str
    status: str
    voice_profile: str
    start_time: datetime
    duration: float
    transcript: str
    
    class Config:
        from_attributes = True

class CallDetailsResponse(BaseModel):
    """Schema for detailed call information"""
    call_id: str
    user_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    transcript: str
    turns: List[ConversationTurnSchema]
    
    class Config:
        from_attributes = True

class DashboardStatsResponse(BaseModel):
    """Schema for dashboard statistics"""
    total_calls: int
    active_calls: int
    completed_calls: int
    average_duration: float
    total_conversation_minutes: float
