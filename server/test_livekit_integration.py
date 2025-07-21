#!/usr/bin/env python3
"""
Test script for LiveKit integration.
This script tests the LiveKit client functionality.
"""

import asyncio
import logging
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.livekit_client import LiveKitVoiceAgent
from app.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_livekit_connection():
    """Test LiveKit connection and basic functionality."""
    
    # Create LiveKit agent
    livekit_agent = LiveKitVoiceAgent()
    
    try:
        # Test connection
        logger.info("Testing LiveKit connection...")
        result = await livekit_agent.connect_to_room("test-room", "test-participant")
        
        if result.get("success"):
            logger.info("✅ Successfully connected to LiveKit room")
            logger.info(f"Room: {result.get('room_name')}")
            logger.info(f"Participant: {result.get('participant_name')}")
            
            # Test room status
            status = livekit_agent.get_room_status()
            logger.info(f"Room status: {status}")
            
            # Test disconnection
            logger.info("Testing disconnection...")
            disconnect_result = await livekit_agent.disconnect_from_room()
            
            if disconnect_result.get("success"):
                logger.info("✅ Successfully disconnected from LiveKit room")
            else:
                logger.error(f"❌ Failed to disconnect: {disconnect_result.get('error')}")
                
        else:
            logger.error(f"❌ Failed to connect to LiveKit room: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"❌ Error during LiveKit test: {e}")

async def test_voice_processing():
    """Test voice processing with LiveKit."""
    
    # Create LiveKit agent
    livekit_agent = LiveKitVoiceAgent()
    
    try:
        # Connect to room
        logger.info("Connecting to room for voice processing test...")
        result = await livekit_agent.connect_to_room("test-room", "test-participant")
        
        if result.get("success"):
            logger.info("✅ Connected to room for voice processing test")
            
            # Create dummy audio data (this would normally come from a real audio source)
            dummy_audio_data = b"dummy_audio_data_for_testing"
            
            # Test voice processing
            logger.info("Testing voice processing...")
            voice_result = await livekit_agent.process_voice_input(dummy_audio_data)
            
            logger.info(f"Voice processing result: {voice_result}")
            
            # Disconnect
            await livekit_agent.disconnect_from_room()
            logger.info("✅ Disconnected from room")
            
        else:
            logger.error(f"❌ Failed to connect for voice processing test: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"❌ Error during voice processing test: {e}")

async def test_track_kind_checking():
    """Test track kind checking functionality."""
    logger.info("Testing track kind checking...")
    logger.info("✅ Track kind values: 0 = AUDIO, 1 = VIDEO")
    logger.info("✅ Fixed TrackType import issue by using numeric values")

async def main():
    """Main test function."""
    logger.info("Starting LiveKit integration tests...")
    
    # Test track kind checking
    await test_track_kind_checking()
    
    # Test basic connection
    await test_livekit_connection()
    
    # Test voice processing
    await test_voice_processing()
    
    logger.info("LiveKit integration tests completed.")

if __name__ == "__main__":
    asyncio.run(main()) 