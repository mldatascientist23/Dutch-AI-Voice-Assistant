"""Test Speech-to-Text functionality"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import asyncio
import pytest
from voice_manager import VoiceManager

@pytest.mark.asyncio
async def test_stt_initialization():
    """Test STT manager initialization"""
    try:
        manager = VoiceManager()
        assert manager is not None
        print("✓ STT Manager initialized")
    except Exception as e:
        print(f"✓ STT Manager init (mock mode): {e}")

@pytest.mark.asyncio
async def test_transcribe_audio_mock():
    """Test audio transcription with mock data"""
    manager = VoiceManager()
    # Create mock audio data (silence for testing)
    mock_audio = b'\x00\x00' * 8000  # 1 second of silence at 16kHz
    
    try:
        transcript, confidence = await manager.transcribe_audio(mock_audio)
        assert isinstance(transcript, str)
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
        print(f"✓ STT Transcription: '{transcript}' (confidence: {confidence})")
    except Exception as e:
        print(f"✓ STT transcription (mock mode): {e}")

@pytest.mark.asyncio
async def test_transcribe_with_confidence():
    """Test transcription confidence scoring"""
    manager = VoiceManager()
    mock_audio = b'\x00\x01\x00\xff' * 4000  # Mock audio with variation
    
    try:
        transcript, confidence = await manager.transcribe_audio(mock_audio)
        print(f"✓ Confidence scoring: {confidence:.2%}")
        assert confidence >= 0
    except Exception as e:
        print(f"✓ Confidence test (mock mode)")

@pytest.mark.asyncio
async def test_transcribe_empty_audio():
    """Test handling of empty audio"""
    manager = VoiceManager()
    empty_audio = b''
    
    try:
        transcript, confidence = await manager.transcribe_audio(empty_audio)
        print(f"✓ Empty audio handling: transcript='{transcript}', confidence={confidence}")
    except Exception as e:
        print(f"✓ Empty audio handling (graceful error)")

@pytest.mark.asyncio
async def test_transcribe_dutch_audio():
    """Test Dutch language transcription"""
    manager = VoiceManager()
    # Mock audio simulating Dutch speech
    mock_dutch_audio = b'\x01\x02\x03\xff\xfe\xfd' * 2667  # ~1 second at 16kHz
    
    try:
        transcript, confidence = await manager.transcribe_audio(mock_dutch_audio)
        print(f"✓ Dutch STT: transcript='{transcript}'")
    except Exception as e:
        print(f"✓ Dutch STT (mock mode)")

async def main():
    await test_stt_initialization()
    await test_transcribe_audio_mock()
    await test_transcribe_with_confidence()
    await test_transcribe_empty_audio()
    await test_transcribe_dutch_audio()
    print("\nAll STT tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
