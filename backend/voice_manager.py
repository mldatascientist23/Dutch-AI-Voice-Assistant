"""Voice Manager Module - Handles Dutch TTS/STT using Google Cloud"""
import logging
import json
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class VoiceManager:
    """Manager for Text-to-Speech and Speech-to-Text operations"""
    
    def __init__(self):
        """Initialize Voice Manager"""
        try:
            # Import Google Cloud clients
            from google.cloud import texttospeech, speech_v1
            from config import settings
            import os
            
            # Set credentials from environment
            if os.path.exists(settings.GOOGLE_CLOUD_CREDENTIALS):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_CLOUD_CREDENTIALS
            
            self.tts_client = texttospeech.TextToSpeechClient()
            self.stt_client = speech_v1.SpeechClient()
            self.settings = settings
            logger.info("Voice Manager initialized successfully")
        except ImportError:
            logger.warning("Google Cloud libraries not installed. Using mock mode for testing.")
            self.tts_client = None
            self.stt_client = None
            self.settings = None
        except Exception as e:
            logger.error(f"Failed to initialize Voice Manager: {e}")
            raise
    
    async def synthesize_speech(self, text: str, voice_profile: str = "lifestyle") -> bytes:
        """Convert text to speech in Dutch"""
        try:
            if not self.tts_client or not self.settings:
                logger.warning("TTS client not available, returning empty bytes")
                return b''
            
            profile = self.settings.VOICE_PROFILES.get(voice_profile, self.settings.VOICE_PROFILES["lifestyle"])
            
            from google.cloud import texttospeech
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.settings.SPEECH_LANGUAGE,
                name=f"{self.settings.SPEECH_LANGUAGE}-Neural2-{'F' if profile['gender'] == 'FEMALE' else 'M'}",
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=profile["pitch"],
                speaking_rate=profile["rate"],
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            logger.info(f"Speech synthesized: {len(response.audio_content)} bytes")
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            raise
    
    async def transcribe_audio(self, audio_data: bytes) -> Tuple[str, float]:
        """Convert audio to text using Dutch STT"""
        try:
            if not self.stt_client or not self.settings:
                logger.warning("STT client not available")
                return "Simulated transcription", 0.95
            
            from google.cloud import speech_v1
            
            audio = speech_v1.RecognitionAudio(content=audio_data)
            
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.settings.SAMPLE_RATE,
                language_code=self.settings.SPEECH_LANGUAGE,
                enable_automatic_punctuation=True,
            )
            
            response = self.stt_client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    confidence = result.alternatives[0].confidence
                    logger.info(f"Audio transcribed: '{transcript}' (confidence: {confidence})")
                    return transcript, float(confidence)
            
            return "", 0.0
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise

voice_manager: Optional[VoiceManager] = None

def get_voice_manager() -> VoiceManager:
    """Get or create voice manager instance"""
    global voice_manager
    if voice_manager is None:
        voice_manager = VoiceManager()
    return voice_manager
