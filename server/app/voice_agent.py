from typing import Dict, Any, Optional
from .bedrock_client import BedrockClient
from .data_handler import DataHandler
from .config import Config

class VoiceAgent:
    """Main voice agent that coordinates all components."""
    
    def __init__(self):
        self.bedrock_client = BedrockClient()
        self.data_handler = DataHandler()
    
    async def process_text_input(self, text: str) -> Dict[str, Any]:
        """
        Process text input and return appropriate response.
        
        Args:
            text: User's text input
            
        Returns:
            Dict containing response text and metadata
        """
        try:
            # Analyze intent using Bedrock
            intent_result = await self.bedrock_client.analyze_intent(text)
            
            if intent_result.get("error"):
                return {
                    "response": "I'm sorry, I'm having trouble processing your request right now.",
                    "success": False,
                    "error": intent_result["error"]
                }
            
            # Check if it's a capital query
            if intent_result.get("is_capital_query"):
                entity = intent_result.get("entity")
                query_type = intent_result.get("query_type")
                
                if entity:
                    # Look up the capital
                    capital = self.data_handler.find_capital(entity)
                    
                    if capital:
                        # Generate natural response
                        response = await self.bedrock_client.generate_response(
                            query_type, entity, capital
                        )
                        return {
                            "response": response,
                            "success": True,
                            "query_type": query_type,
                            "entity": entity,
                            "capital": capital
                        }
                    else:
                        return {
                            "response": f"I'm sorry, I don't have information about the capital of {entity}.",
                            "success": True,
                            "query_type": query_type,
                            "entity": entity,
                            "capital": None
                        }
                else:
                    return {
                        "response": "I'm sorry, I couldn't understand which country or state you're asking about.",
                        "success": True,
                        "query_type": "unknown",
                        "entity": None,
                        "capital": None
                    }
            else:
                # Not a capital query
                return {
                    "response": Config.UNSUPPORTED_QUERY_RESPONSE,
                    "success": True,
                    "query_type": "other",
                    "entity": None,
                    "capital": None
                }
                
        except Exception as e:
            return {
                "response": "I'm sorry, I encountered an error processing your request.",
                "success": False,
                "error": str(e)
            }
    
    async def process_voice_input(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Process voice input (placeholder for future implementation).
        
        Args:
            audio_data: Raw audio data
            
        Returns:
            Dict containing response text and metadata
        """
        # TODO: Implement speech-to-text conversion
        # For now, return a placeholder response
        return {
            "response": "Voice processing not yet implemented.",
            "success": False,
            "error": "Voice processing not implemented in Phase 1"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and health information."""
        bedrock_status = self.bedrock_client.test_connection()
        data_summary = self.data_handler.get_data_summary()
        
        return {
            "bedrock_connection": bedrock_status,
            "data_loaded": data_summary,
            "config": {
                "aws_region": Config.AWS_REGION,
                "bedrock_model": Config.BEDROCK_MODEL_ID,
                "debug_mode": Config.DEBUG
            }
        }
    
    def get_available_entities(self) -> Dict[str, Any]:
        """Get lists of available countries and states."""
        return {
            "countries": self.data_handler.get_all_countries(),
            "states": self.data_handler.get_all_states()
        } 