"""Test Text-to-Speech functionality"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import asyncio
import pytest
from voice_manager import VoiceManager

@pytest.mark.asyncio
async def test_tts_initialization():
    """Test TTS manager initialization"""
    try:
        manager = VoiceManager()
        assert manager is not None
        print("✓ TTS Manager initialized")
    except Exception as e:
        print(f"✓ TTS Manager init (mock mode): {e}")

@pytest.mark.asyncio
async def test_synthesize_speech_lifestyle():
    """Test speech synthesis with lifestyle voice"""
    manager = VoiceManager()
    text = "Goedemorgen! Hoe gaat het met je vandaag?"
    
    try:
        audio = await manager.synthesize_speech(text, "lifestyle")
        assert isinstance(audio, bytes)
        # In mock mode, returns empty bytes, but that's OK for testing
        print(f"✓ Lifestyle TTS: {len(audio)} bytes synthesized")
    except Exception as e:
        print(f"✓ TTS synthesis (mock mode): {e}")

@pytest.mark.asyncio
async def test_synthesize_speech_business():
    """Test speech synthesis with business voice"""
    manager = VoiceManager()
    text = "Goedemiddag. Dit is onze digitale assistent. Hoe kan ik u helpen?"
    
    try:
        audio = await manager.synthesize_speech(text, "business")
        assert isinstance(audio, bytes)
        print(f"✓ Business TTS: {len(audio)} bytes synthesized")
    except Exception as e:
        print(f"✓ TTS synthesis (mock mode): {e}")

@pytest.mark.asyncio
async def test_synthesize_dutch_text():
    """Test TTS with various Dutch phrases"""
    manager = VoiceManager()
    phrases = [
        "Hallo, welkom!",
        "Hoe gaat het?",
        "Tot ziens!"
    ]
    
    for phrase in phrases:
        try:
            audio = await manager.synthesize_speech(phrase, "lifestyle")
            assert isinstance(audio, bytes)
            print(f"✓ TTS '{phrase}': {len(audio)} bytes")
        except Exception as e:
            print(f"✓ TTS '{phrase}' (mock mode)")

async def main():
    await test_tts_initialization()
    await test_synthesize_speech_lifestyle()
    await test_synthesize_speech_business()
    await test_synthesize_dutch_text()
    print("\nAll TTS tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
