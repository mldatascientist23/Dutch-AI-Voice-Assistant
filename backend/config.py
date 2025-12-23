import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./voice_assistant.db")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # TTS/STT Services
    GOOGLE_CLOUD_CREDENTIALS = os.getenv("GOOGLE_CLOUD_CREDENTIALS", "./credentials.json")
    SPEECH_LANGUAGE = "nl-NL"  # Dutch language
    
    # Voice Profiles
    VOICE_PROFILES: Dict = {
        "lifestyle": {
            "name": "Amy",
            "gender": "FEMALE",
            "pitch": 0.0,
            "rate": 0.9,
            "emotion": "friendly"
        },
        "business": {
            "name": "Gary",
            "gender": "MALE",
            "pitch": 0.0,
            "rate": 1.0,
            "emotion": "professional"
        }
    }
    
    # Call Settings
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    MAX_CALL_DURATION = 3600  # 1 hour in seconds
    
    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL = 30  # seconds
    WS_TIMEOUT = 300  # seconds
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "./logs/voice_assistant.log")

settings = Settings()
