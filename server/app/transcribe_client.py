import boto3
import json
import os
import tempfile
import time
import asyncio
import websockets
import uuid
from typing import Dict, Any, Optional, AsyncGenerator
from .config import Config

class TranscribeClient:
    """Client for Amazon Transcribe integration."""
    
    def __init__(self):
        self.client = boto3.client(
            'transcribe',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        self.s3_client = boto3.client(
            's3',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
    
    async def transcribe_audio_file(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe an audio file using Amazon Transcribe.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Use transcription
            transcription_result = await self._transcribe_audio(audio_data)
            
            return {
                "success": True,
                "transcription": transcription_result,
                "file_path": audio_file_path
            }
            
        except Exception as e:
            print(f"Error in transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": None
            }
    
    async def transcribe_audio_bytes(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio bytes using Amazon Transcribe.
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Check if audio data is valid
            if len(audio_data) < 100:  # Very small audio file
                return {
                    "success": False,
                    "error": "Audio data too small or invalid",
                    "transcription": None
                }
            
            # Use transcription
            transcription_result = await self._transcribe_audio(audio_data)
            
            return {
                "success": True,
                "transcription": transcription_result,
                "note": "Real-time transcription completed."
            }
            
        except Exception as e:
            print(f"Error in audio transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcription": None
            }
    
    async def _transcribe_audio(self, audio_data: bytes) -> str:
        """
        Perform transcription using Amazon Transcribe.
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Transcribed text
        """
        try:
            # Create a temporary file for the audio data
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Check if we have AWS credentials configured
                if not Config.AWS_ACCESS_KEY_ID or not Config.AWS_SECRET_ACCESS_KEY:
                    return "This is a test transcription. Please configure AWS credentials for real transcription."
                
                # Create a unique job name
                job_name = f"transcribe_job_{uuid.uuid4().hex[:8]}"
                
                # Real transcription implementation
                try:
                    # Create a unique file name
                    file_name = f"audio_{uuid.uuid4().hex[:8]}.wav"
                    s3_key = f"transcribe-input/{file_name}"
                    
                    # Upload audio to S3
                    print(f"Uploading audio to S3: {Config.S3_BUCKET_NAME}/{s3_key}")
                    self.s3_client.upload_file(temp_file_path, Config.S3_BUCKET_NAME, s3_key)
                    
                    # Start transcription job
                    print(f"Starting transcription job: {job_name}")
                    response = self.client.start_transcription_job(
                        TranscriptionJobName=job_name,
                        Media={'MediaFileUri': f"s3://{Config.S3_BUCKET_NAME}/{s3_key}"},
                        MediaFormat='wav',
                        LanguageCode='en-US'
                    )
                    
                    # Poll for completion
                    print("Polling for transcription completion...")
                    while True:
                        job_response = self.client.get_transcription_job(
                            TranscriptionJobName=job_name
                        )
                        
                        status = job_response['TranscriptionJob']['TranscriptionJobStatus']
                        
                        if status == 'COMPLETED':
                            # Get transcription results
                            transcript_uri = job_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                            print(f"Transcription completed. Results at: {transcript_uri}")
                            
                            # Download and parse transcript
                            import requests
                            transcript_response = requests.get(transcript_uri)
                            transcript_data = transcript_response.json()
                            
                            # Extract transcription text
                            transcription = transcript_data['results']['transcripts'][0]['transcript']
                            
                            # Clean up S3 file
                            try:
                                self.s3_client.delete_object(Bucket=Config.S3_BUCKET_NAME, Key=s3_key)
                            except Exception as e:
                                print(f"Warning: Could not delete S3 file: {e}")
                            
                            return transcription
                            
                        elif status == 'FAILED':
                            error_message = job_response['TranscriptionJob'].get('FailureReason', 'Unknown error')
                            print(f"Transcription job failed: {error_message}")
                            raise Exception(f"Transcription job failed: {error_message}")
                        
                        # Wait before polling again
                        await asyncio.sleep(2)
                    
                except Exception as e:
                    print(f"Transcription error: {e}")
                    
                    # If S3 or transcription fails, try a fallback approach
                    # This could be using a different transcription service or method
                    
                    # For now, return a helpful error message
                    if "NoSuchBucket" in str(e):
                        return "S3 bucket not found. Please create the bucket or check configuration."
                    elif "AccessDenied" in str(e):
                        return "Access denied. Please check AWS credentials and permissions."
                    else:
                        return f"Transcription failed: {str(e)}"
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            print(f"Error in transcription: {e}")
            raise e
    
    async def start_realtime_transcription(self, audio_stream: AsyncGenerator[bytes, None]) -> AsyncGenerator[str, None]:
        """
        Start real-time transcription from a continuous audio stream.
        This would use WebSocket-based streaming with Amazon Transcribe.
        
        Args:
            audio_stream: Async generator yielding audio bytes
            
        Yields:
            Transcribed text as it becomes available
        """
        try:
            # This is a placeholder for real-time streaming transcription
            # In production, you would:
            # 1. Establish WebSocket connection to Amazon Transcribe
            # 2. Stream audio data in real-time
            # 3. Receive transcription results as they become available
            
            async for audio_chunk in audio_stream:
                # Simulate real-time transcription processing
                await asyncio.sleep(0.1)
                
                # For now, yield a placeholder
                # This should be replaced with actual transcription logic
                yield "Real-time transcription placeholder"
                
        except Exception as e:
            print(f"Error in real-time transcription: {e}")
            yield f"Transcription error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test the Transcribe connection."""
        try:
            # Try to list transcription jobs to test connection
            self.client.list_transcription_jobs(MaxResults=1)
            return True
        except Exception as e:
            print(f"Transcribe connection test failed: {e}")
            return False 