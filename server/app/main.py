from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

from .voice_agent import VoiceAgent
from .config import Config

# Initialize FastAPI app
app = FastAPI(
    title="Voice Agent API",
    description="A voice agent that answers questions about country and state capitals",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize voice agent
voice_agent = VoiceAgent()

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str

class VoiceRequest(BaseModel):
    audio_data: str  # Base64 encoded audio

class Response(BaseModel):
    response: str
    success: bool
    query_type: str = None
    entity: str = None
    capital: str = None
    error: str = None

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Voice Agent API",
        "version": "1.0.0",
        "description": "A voice agent that answers questions about country and state capitals"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "voice-agent"}

@app.get("/status")
async def get_status():
    """Get system status and health information."""
    return voice_agent.get_system_status()

@app.get("/entities")
async def get_entities():
    """Get available countries and states."""
    return voice_agent.get_available_entities()

@app.post("/process-text", response_model=Response)
async def process_text(request: TextRequest):
    """
    Process text input and return response.
    
    This endpoint analyzes the text to determine if it's asking about a country or state capital,
    and returns the appropriate response.
    """
    try:
        result = await voice_agent.process_text_input(request.text)
        return Response(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.post("/process-voice", response_model=Response)
async def process_voice(request: VoiceRequest):
    """
    Process voice input (placeholder for Phase 2).
    
    This endpoint will be implemented in Phase 2 with speech-to-text conversion.
    """
    try:
        # For now, return a placeholder response
        result = await voice_agent.process_voice_input(request.audio_data.encode())
        return Response(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint for development."""
    return {
        "message": "Voice Agent API is running",
        "phase": "Phase 1 - Core Setup",
        "features": [
            "FastAPI application",
            "Bedrock integration",
            "Static data loading",
            "Text processing",
            "Health checks"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    ) 