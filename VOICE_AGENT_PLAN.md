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
- **LiveKit Python SDK**: Server-side voice processing

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
├── server/                 # Python Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI app
│   │   ├── voice_agent.py # Voice processing logic
│   │   ├── bedrock_client.py # Bedrock integration
│   │   ├── data_handler.py # JSON data management
│   │   └── config.py      # Configuration settings
│   ├── data/
│   │   ├── countries.json
│   │   └── us-states.json
│   ├── audio/             # Local audio storage
│   ├── requirements.txt
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
2. Audio → WebSocket → Python Backend
3. Python Backend → Amazon Transcribe (STT)
4. Text → Bedrock (Claude Haiku) for intent classification
5. If country/state query → Lookup from static JSON files
6. If other query → Return "information not available"
7. Response → Amazon Polly (TTS)
8. Audio → WebSocket → LiveKit → User hears response
```

## Core Components

### 1. Voice Agent Logic (voice_agent.py)
```python
class VoiceAgent:
    def __init__(self):
        self.bedrock_client = BedrockClient()
        self.data_handler = DataHandler()
    
    async def process_voice_input(self, audio_data):
        # Convert audio to text
        # Analyze intent with Bedrock
        # Lookup capital if applicable
        # Generate response
        pass
```

### 2. Bedrock Integration (bedrock_client.py)
```python
class BedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
    
    async def analyze_intent(self, text):
        # Use Claude Haiku to determine if query is about country/state
        pass
```

### 3. Data Handler (data_handler.py)
```python
class DataHandler:
    def __init__(self):
        self.countries = self.load_countries()
        self.states = self.load_states()
    
    def find_capital(self, query):
        # Search countries and states for capital
        pass
```

## Development Phases

### Phase 1: Core Setup (Week 1) ✅ COMPLETED
- [x] Set up Python development environment
- [x] Create FastAPI application structure
- [x] Implement static JSON datasets
- [x] Basic Bedrock integration
- [x] Local development with Docker

### Phase 2: Voice Integration (Week 2) ✅ COMPLETED
- [x] Amazon Transcribe integration
- [x] Amazon Polly integration
- [x] WebSocket communication setup
- [x] Basic voice processing pipeline

### Phase 3: LiveKit Integration (Week 3)
- [ ] Set up LiveKit server/credentials
- [ ] Web client with LiveKit SDK
- [ ] Real-time audio streaming
- [ ] End-to-end voice communication

### Phase 4: Production Ready (Week 4)
- [ ] Error handling and logging
- [ ] Performance optimization
- [ ] Security hardening
- [ ] EC2 deployment setup
- [ ] Monitoring and health checks

## AWS Configuration

### Required AWS Services
- **AWS Bedrock**: Claude 3 Haiku model access
- **Amazon Polly**: Text-to-speech service
- **Amazon Transcribe**: Speech-to-text service
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

- Unit tests for data handlers
- Integration tests for AWS services
- End-to-end voice testing
- Performance testing under load

## Future Enhancements

- Conversation history storage
- Multi-language support
- Advanced audio processing
- Machine learning for better intent recognition
- Mobile app integration 