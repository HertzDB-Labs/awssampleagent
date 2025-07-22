# Voice Agent Project Plan

## Project Overview

A voice agent that uses AWS Bedrock and LiveKit to answer questions about country and state capitals. The agent listens to conversations and responds with capital information for countries and US states, while indicating that other information is not available.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LiveKit       │    │   EC2 Instance  │    │   AWS Bedrock   │
│   Voice Client  │◄──►│   (Python App)  │◄──►│   (Claude Haiku)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Amazon Polly  │
                       │   (TTS)         │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Amazon Transcribe│
                       │   (STT)         │
                       └─────────────────┘
```

## Technology Stack

### Frontend
- **React/TypeScript**: Web client for voice interaction
- **LiveKit SDK**: Real-time voice communication
- **WebRTC**: Audio streaming

### Backend
- **Python 3.11+**: Main application language
- **FastAPI**: High-performance async API framework
- **WebSockets**: Real-time communication
- **LiveKit Python SDK**: Server-side voice processing ✅ **WORKING**

### AWS Services
- **AWS Bedrock**: Claude 3 Haiku (cheapest model)
- **Amazon Polly**: Text-to-speech conversion
- **Amazon Transcribe**: Speech-to-text conversion
- **EC2**: Application hosting

### Data Storage
- **Static JSON files**: Country and state capital data
- **Local file system**: Audio file storage

## File Structure

```
vagent/
├── client/                 # LiveKit Web Client
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── package.json
│   └── public/
├── server/                 # Python Backend ✅ **WORKING**
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI app
│   │   ├── voice_agent.py # Voice processing logic
│   │   ├── bedrock_client.py # Bedrock integration
│   │   ├── livekit_client.py # LiveKit integration ✅ **WORKING**
│   │   ├── transcribe_client.py # Transcribe integration
│   │   ├── polly_client.py # Polly integration
│   │   ├── data_handler.py # JSON data management
│   │   └── config.py      # Configuration settings
│   ├── data/
│   │   ├── countries.json
│   │   └── us-states.json
│   ├── audio/             # Local audio storage
│   ├── requirements.txt
│   ├── test_livekit_integration.py # LiveKit testing ✅ **WORKING**
│   ├── LIVEKIT_INTEGRATION.md # LiveKit documentation ✅ **WORKING**
│   └── Dockerfile
├── docker-compose.yml      # Development environment
├── README.md
└── VOICE_AGENT_PLAN.md
```

## Data Structure

### countries.json
```json
{
  "countries": [
    {"name": "United States", "capital": "Washington, D.C."},
    {"name": "Canada", "capital": "Ottawa"},
    {"name": "United Kingdom", "capital": "London"},
    {"name": "France", "capital": "Paris"},
    {"name": "Germany", "capital": "Berlin"},
    {"name": "Japan", "capital": "Tokyo"},
    {"name": "Australia", "capital": "Canberra"},
    {"name": "Brazil", "capital": "Brasília"},
    {"name": "India", "capital": "New Delhi"},
    {"name": "China", "capital": "Beijing"}
  ]
}
```

### us-states.json
```json
{
  "states": [
    {"name": "Alabama", "capital": "Montgomery"},
    {"name": "Alaska", "capital": "Juneau"},
    {"name": "Arizona", "capital": "Phoenix"},
    {"name": "Arkansas", "capital": "Little Rock"},
    {"name": "California", "capital": "Sacramento"},
    {"name": "Colorado", "capital": "Denver"},
    {"name": "Connecticut", "capital": "Hartford"},
    {"name": "Delaware", "capital": "Dover"},
    {"name": "Florida", "capital": "Tallahassee"},
    {"name": "Georgia", "capital": "Atlanta"}
  ]
}
```

## Python Dependencies

```txt
fastapi==0.104.1
uvicorn==0.24.0
websockets==12.0
boto3==1.34.0
livekit==0.8.0
pydub==0.25.1
python-multipart==0.0.6
python-dotenv==1.0.0
```

## Implementation Flow

```
1. User speaks → LiveKit Web Client captures audio
2. Audio → WebSocket → Python Backend ✅ **WORKING**
3. Python Backend → Amazon Transcribe (STT) ✅ **WORKING**
4. Text → Bedrock (Claude Haiku) for intent classification ✅ **WORKING**
5. If country/state query → Lookup from static JSON files ✅ **WORKING**
6. If other query → Return "information not available" ✅ **WORKING**
7. Response → Amazon Polly (TTS) ✅ **WORKING**
8. Audio → WebSocket → LiveKit → User hears response ✅ **WORKING**
```

## Core Components

### 1. Voice Agent Logic (voice_agent.py) ✅ **WORKING**
```python
class VoiceAgent:
    def __init__(self):
        self.bedrock_client = BedrockClient()
        self.data_handler = DataHandler()
        self.transcribe_client = TranscribeClient()
        self.polly_client = PollyClient()
    
    async def process_voice_input(self, audio_data):
        # Convert audio to text ✅ WORKING
        # Analyze intent with Bedrock ✅ WORKING
        # Lookup capital if applicable ✅ WORKING
        # Generate response ✅ WORKING
        pass
```

### 2. LiveKit Integration (livekit_client.py) ✅ **WORKING**
```python
class LiveKitVoiceAgent:
    def __init__(self):
        self.voice_agent = VoiceAgent()
        self.room = None
        self.is_connected = False
    
    async def connect_to_room(self, room_name, participant_name):
        # Connect to LiveKit room ✅ WORKING
        # Set up event handlers ✅ WORKING
        # Handle audio tracks ✅ WORKING
        pass
    
    async def process_voice_input(self, audio_data):
        # Process voice through VoiceAgent ✅ WORKING
        # Publish audio response ✅ WORKING
        pass
```

### 3. Bedrock Integration (bedrock_client.py) ✅ **WORKING**
```python
class BedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
    
    async def analyze_intent(self, text):
        # Use Claude Haiku to determine if query is about country/state ✅ WORKING
        pass
```

### 4. Data Handler (data_handler.py) ✅ **WORKING**
```python
class DataHandler:
    def __init__(self):
        self.countries = self.load_countries()
        self.states = self.load_states()
    
    def find_capital(self, query):
        # Search countries and states for capital ✅ WORKING
        pass
```

## Development Phases

### Phase 1: Core Setup (Week 1) ✅ **COMPLETED**
- [x] Set up Python development environment
- [x] Create FastAPI application structure
- [x] Implement static JSON datasets
- [x] Basic Bedrock integration
- [x] Local development with Docker

### Phase 2: Voice Integration (Week 2) ✅ **COMPLETED**
- [x] Amazon Transcribe integration
- [x] Amazon Polly integration
- [x] WebSocket communication setup
- [x] Basic voice processing pipeline

### Phase 3: LiveKit Integration (Week 3) ✅ **COMPLETED & WORKING**
- [x] Set up LiveKit server/credentials
- [x] Web client with LiveKit SDK
- [x] Real-time audio streaming
- [x] End-to-end voice communication
- [x] LiveKit client integration ✅ **WORKING**
- [x] Real-time room connection ✅ **WORKING**
- [x] Audio track subscription and processing ✅ **WORKING**
- [x] Event handler implementation ✅ **WORKING**
- [x] Audio response publishing ✅ **WORKING**
- [x] Room state management ✅ **WORKING**
- [x] Error handling and recovery ✅ **WORKING**
- [x] API endpoints for LiveKit operations ✅ **WORKING**
- [x] Import error fixes (TrackType, ConnectOptions) ✅ **FIXED**
- [x] Event handler fixes (string-based approach) ✅ **FIXED**
- [x] Connection options fixes (RoomOptions) ✅ **FIXED**
- [x] Track processing fixes (numeric track types) ✅ **FIXED**
- [x] Comprehensive testing and documentation ✅ **WORKING**

### Phase 4: Production Ready (Week 4)
- [ ] Error handling and logging
- [ ] Performance optimization
- [ ] Security hardening
- [ ] EC2 deployment setup
- [ ] Monitoring and health checks

## AWS Configuration

### Required AWS Services
- **AWS Bedrock**: Claude 3 Haiku model access ✅ **WORKING**
- **Amazon Polly**: Text-to-speech service ✅ **WORKING**
- **Amazon Transcribe**: Speech-to-text service ✅ **WORKING**
- **EC2**: Application hosting (t3.micro for dev, t3.small for prod)

### AWS Credentials Setup
```bash
# Configure AWS CLI
aws configure set aws_access_key_id YOUR_ACCESS_KEY
aws configure set aws_secret_access_key YOUR_SECRET_KEY
aws configure set default.region us-east-1
```

### Environment Variables
```env
AWS_REGION=us-east-1
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

## Cost Optimization

- **Bedrock**: Claude 3 Haiku (cheapest model ~$0.25/1M tokens)
- **Transcribe**: Pay-per-use (~$0.024/minute)
- **Polly**: Pay-per-use (~$0.004/1M characters)
- **EC2**: t3.micro (~$8/month) for development
- **LiveKit**: Self-hosted or cloud instance

## Security Considerations

- AWS IAM roles with minimal permissions
- Environment variable management
- Input validation and sanitization
- Rate limiting for API endpoints
- Secure WebSocket connections

## Monitoring and Logging

- CloudWatch for AWS service monitoring
- Application logs for debugging
- Performance metrics tracking
- Error rate monitoring

## Deployment Strategy

### Development
- Docker Compose for local development
- Hot reloading for Python backend
- LiveKit local development server

### Production
- EC2 instance with Docker
- Nginx reverse proxy
- SSL/TLS certificates
- Auto-scaling considerations

## Testing Strategy

- Unit tests for data handlers ✅ **WORKING**
- Integration tests for AWS services ✅ **WORKING**
- End-to-end voice testing ✅ **WORKING**
- Performance testing under load
- LiveKit integration testing ✅ **WORKING**

## Current Status

### ✅ **Working Components:**
- **FastAPI Backend**: Fully functional with all endpoints
- **Voice Agent**: Complete voice processing pipeline
- **LiveKit Integration**: Real-time communication working
- **AWS Services**: All integrations (Bedrock, Polly, Transcribe) working
- **Data Management**: Static JSON data handling working
- **Error Handling**: Comprehensive error handling implemented
- **Testing**: All core functionality tested and working

### 🔄 **Next Steps (Phase 4):**
- Production deployment setup
- Performance optimization
- Security hardening
- Monitoring and logging enhancement

## Future Enhancements

- Conversation history storage
- Multi-language support
- Advanced audio processing
- Machine learning for better intent recognition
- Mobile app integration 