"""Dutch AI Voice Assistant Backend Package"""

from config import settings
from database import get_db, init_db
from models import (
    CallRecord,
    ConversationTurn,
    VoiceProfile,
    CallCreate,
    CallResponse,
    DashboardStatsResponse
)
from conversation_flows import ConversationFlowManager, VoiceProfile as VoiceProfileEnum

__version__ = "1.0.0"
__author__ = "Dutch AI Voice Assistant Team"

__all__ = [
    "settings",
    "get_db",
    "init_db",
    "CallRecord",
    "ConversationTurn",
    "VoiceProfile",
    "CallCreate",
    "CallResponse",
    "DashboardStatsResponse",
    "ConversationFlowManager",
    "VoiceProfileEnum",
]
