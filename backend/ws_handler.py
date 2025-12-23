"""WebSocket Handler - Real-time audio streaming and conversation"""
import logging
import json
import asyncio
from typing import Set, Dict
from fastapi import WebSocket, WebSocketDisconnect
from conversation_flows import ConversationFlowManager, VoiceProfile

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.call_flows: Dict[str, ConversationFlowManager] = {}
    
    async def connect(self, websocket: WebSocket, call_id: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[call_id] = websocket
        logger.info(f"WebSocket connected: {call_id}")
    
    def disconnect(self, call_id: str):
        """Remove WebSocket connection"""
        if call_id in self.active_connections:
            del self.active_connections[call_id]
        if call_id in self.call_flows:
            del self.call_flows[call_id]
        logger.info(f"WebSocket disconnected: {call_id}")
    
    async def send_message(self, call_id: str, message: dict):
        """Send JSON message to client"""
        if call_id in self.active_connections:
            try:
                await self.active_connections[call_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {call_id}: {e}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connections"""
        for call_id in self.active_connections.copy():
            await self.send_message(call_id, message)
    
    async def receive_text(self, call_id: str) -> str:
        """Receive text message from client"""
        if call_id in self.active_connections:
            try:
                return await self.active_connections[call_id].receive_text()
            except WebSocketDisconnect:
                self.disconnect(call_id)
                return ""
        return ""

manager = ConnectionManager()

async def handle_websocket_call(websocket: WebSocket, call_id: str, voice_profile: str):
    """
    Handle WebSocket connection for a call
    """
    try:
        await manager.connect(websocket, call_id)
        
        # Initialize conversation flow
        flow = ConversationFlowManager(profile=VoiceProfile(voice_profile))
        manager.call_flows[call_id] = flow
        
        # Send greeting
        greeting = await flow.start_conversation()
        await manager.send_message(call_id, {
            "type": "greeting",
            "message": greeting,
            "call_id": call_id
        })
        
        # Handle incoming messages
        while call_id in manager.active_connections:
            try:
                # Receive message with timeout
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                
                if not data:
                    continue
                
                # Parse JSON message
                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    message = {"text": data}
                
                user_input = message.get("text", "")
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    closing = await flow.close_conversation()
                    await manager.send_message(call_id, {
                        "type": "closing",
                        "message": closing,
                        "call_id": call_id
                    })
                    break
                
                # Generate response
                response = await flow.respond(user_input)
                
                await manager.send_message(call_id, {
                    "type": "response",
                    "message": response,
                    "user_input": user_input,
                    "call_id": call_id
                })
                
            except asyncio.TimeoutError:
                await manager.send_message(call_id, {
                    "type": "timeout",
                    "message": "No response received. Connection timeout."
                })
                break
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error in WebSocket handler: {e}")
                await manager.send_message(call_id, {
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
                break
    
    except Exception as e:
        logger.error(f"WebSocket connection error for {call_id}: {e}")
    
    finally:
        manager.disconnect(call_id)
        logger.info(f"WebSocket handler finished for {call_id}")

async def handle_audio_stream(websocket: WebSocket, call_id: str):
    """
    Handle audio streaming for real-time transcription
    """
    try:
        await manager.connect(websocket, call_id)
        
        await manager.send_message(call_id, {
            "type": "audio_stream_ready",
            "message": "Audio stream handler ready",
            "call_id": call_id
        })
        
        audio_buffer = b""
        
        while call_id in manager.active_connections:
            try:
                # Receive audio data
                data = await asyncio.wait_for(
                    websocket.receive_bytes(),
                    timeout=30.0
                )
                
                if not data:
                    continue
                
                audio_buffer += data
                
                # Send acknowledgment
                await manager.send_message(call_id, {
                    "type": "audio_received",
                    "bytes_received": len(data),
                    "buffer_size": len(audio_buffer)
                })
                
            except asyncio.TimeoutError:
                break
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error in audio stream: {e}")
                break
    
    except Exception as e:
        logger.error(f"Audio stream error for {call_id}: {e}")
    
    finally:
        manager.disconnect(call_id)
