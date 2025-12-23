"""Test Conversation Flows"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import asyncio
from conversation_flows import LifestyleCoachFlow, BusinessCallFlow, ConversationFlowManager, VoiceProfile

async def test_lifestyle_greeting():
    """Test lifestyle coach greeting"""
    flow = LifestyleCoachFlow()
    greeting = await flow.get_greeting()
    assert greeting is not None
    assert len(greeting) > 0
    assert "Hallo" in greeting or "Hey" in greeting or "Welkom" in greeting

async def test_lifestyle_response():
    """Test lifestyle coach response"""
    flow = LifestyleCoachFlow()
    response = await flow.get_response("Ik ben gestrest")
    assert response is not None
    assert len(response) > 0

async def test_lifestyle_closing():
    """Test lifestyle coach closing"""
    flow = LifestyleCoachFlow()
    closing = await flow.get_closing()
    assert closing is not None
    assert len(closing) > 0

async def test_business_greeting():
    """Test business call greeting"""
    flow = BusinessCallFlow()
    greeting = await flow.get_greeting()
    assert greeting is not None
    assert len(greeting) > 0
    assert "Goedemorgen" in greeting or "Hallo" in greeting

async def test_business_response():
    """Test business call response"""
    flow = BusinessCallFlow()
    response = await flow.get_response("Ik ben hier voor diensten")
    assert response is not None
    assert len(response) > 0

async def test_business_closing():
    """Test business call closing"""
    flow = BusinessCallFlow()
    closing = await flow.get_closing()
    assert closing is not None
    assert len(closing) > 0

async def test_flow_manager_lifestyle():
    """Test flow manager with lifestyle profile"""
    manager = ConversationFlowManager(profile=VoiceProfile.LIFESTYLE)
    greeting = await manager.start_conversation()
    assert greeting is not None
    response = await manager.respond("Hoe gaat het?")
    assert response is not None
    closing = await manager.close_conversation()
    assert closing is not None

async def test_flow_manager_business():
    """Test flow manager with business profile"""
    manager = ConversationFlowManager(profile=VoiceProfile.BUSINESS)
    greeting = await manager.start_conversation()
    assert greeting is not None
    response = await manager.respond("Help nodig")
    assert response is not None
    closing = await manager.close_conversation()
    assert closing is not None

async def main():
    await test_lifestyle_greeting()
    await test_lifestyle_response()
    await test_lifestyle_closing()
    await test_business_greeting()
    await test_business_response()
    await test_business_closing()
    await test_flow_manager_lifestyle()
    await test_flow_manager_business()
    print("All conversation flow tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
