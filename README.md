# Voice Agent Project

A voice agent that uses AWS Bedrock and LiveKit to answer questions about country and state capitals. The agent listens to conversations and responds with capital information for countries and US states, while indicating that other information is not available.

## Project Status

**Current Phase: Phase 1 - Core Setup** ✅ **COMPLETED**

### Phase 1 Components:
- [x] Set up Python development environment
- [x] Create FastAPI application structure
- [x] Implement static JSON datasets
- [x] Basic Bedrock integration
- [x] Local development with virtual environment

## Architecture

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

- **Backend**: Python 3.10+, FastAPI
- **AWS Services**: Bedrock (Claude Haiku), Polly, Transcribe
- **Voice**: LiveKit
- **Data**: Static JSON files
- **Deployment**: Virtual Environment, EC2

## Quick Start

### Prerequisites

1. **Python 3.10+** installed on your system
2. **AWS Account** with access to:
   - AWS Bedrock (Claude Haiku model)
   - Amazon Polly
   - Amazon Transcribe

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vagent
   ```

2. **Run the setup script**
   ```bash
   cd server
   ./setup.sh
   ```

3. **Configure environment variables**
   ```bash
   # Edit the .env file with your AWS credentials
   nano .env
   ```

4. **Activate virtual environment and run**
   ```bash
   source venv/bin/activate
   python run.py
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Test Endpoint: http://localhost:8000/test

### Manual Setup (Alternative)

If you prefer to set up manually:

1. **Create virtual environment**
   ```bash
   cd server
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp ../env.example .env
   # Edit .env with your AWS credentials
   ```

4. **Run the application**
   ```bash
   python run.py
   # Or use uvicorn directly:
   # uvicorn app.main:app --reload
   ```

## Testing

### Local Testing

Run the comprehensive test suite:

```bash
cd server
source venv/bin/activate
python test_local.py
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8000/health

# System status
curl http://localhost:8000/status

# Process text
curl -X POST "http://localhost:8000/process-text" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the capital of France?"}'
```

Expected response:
```json
{
  "response": "The capital of France is Paris.",
  "success": true,
  "query_type": "COUNTRY",
  "entity": "France",
  "capital": "Paris"
}
```

## API Endpoints

### Core Endpoints

- `GET /` - Basic information
- `GET /health` - Health check
- `GET /status` - System status and AWS connection
- `GET /entities` - Available countries and states
- `POST /process-text` - Process text input
- `POST /process-voice` - Process voice input (Phase 2)

## Data Structure

The application uses static JSON files for country and state data:

- `server/data/countries.json` - 195 countries with capitals
- `server/data/us-states.json` - 50 US states with capitals

## Development Phases

### Phase 1: Core Setup ✅ COMPLETED
- [x] Python development environment
- [x] FastAPI application structure
- [x] Static JSON datasets
- [x] Basic Bedrock integration
- [x] Virtual environment setup

### Phase 2: Voice Integration (Next)
- [ ] Amazon Transcribe integration
- [ ] Amazon Polly integration
- [ ] WebSocket communication
- [ ] Basic voice processing pipeline

### Phase 3: LiveKit Integration
- [ ] LiveKit server setup
- [ ] Web client with LiveKit SDK
- [ ] Real-time audio streaming
- [ ] End-to-end voice communication

### Phase 4: Production Ready
- [ ] Error handling and logging
- [ ] Performance optimization
- [ ] Security hardening
- [ ] EC2 deployment setup

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `DEBUG` | Debug mode | `false` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### AWS Services Setup

1. **AWS Bedrock**
   - Enable Claude Haiku model access
   - Configure IAM permissions

2. **Amazon Polly** (Phase 2)
   - Enable text-to-speech service
   - Configure voice preferences

3. **Amazon Transcribe** (Phase 2)
   - Enable speech-to-text service
   - Configure language settings

## File Structure

```
vagent/
├── server/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── voice_agent.py
│   │   ├── bedrock_client.py
│   │   ├── data_handler.py
│   │   └── config.py
│   ├── data/
│   │   ├── countries.json
│   │   └── us-states.json
│   ├── audio/
│   ├── venv/              # Virtual environment
│   ├── requirements.txt
│   ├── run.py             # Run script
│   ├── setup.sh           # Setup script
│   ├── test_local.py      # Test script
│   └── .env               # Environment variables
├── env.example
├── README.md
└── VOICE_AGENT_PLAN.md
```

## Troubleshooting

### Common Issues

1. **Python Version**
   - Ensure Python 3.10+ is installed
   - Check with: `python3 --version`

2. **Virtual Environment**
   - Always activate: `source venv/bin/activate`
   - Reinstall if corrupted: `rm -rf venv && ./setup.sh`

3. **AWS Credentials**
   - Ensure AWS credentials are properly configured in `.env`
   - Check IAM permissions for Bedrock access

4. **Dependencies**
   - Reinstall if issues: `pip install -r requirements.txt`
   - Check for conflicts: `pip list`

### Logs

View application logs in the terminal where you run the server.

## Development Commands

```bash
# Setup (first time only)
cd server
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run server
python run.py

# Run tests
python test_local.py

# Install new dependencies
pip install package_name
pip freeze > requirements.txt
```

## Contributing

1. Follow the development phases outlined in the plan
2. Test thoroughly before submitting changes
3. Update documentation as needed

## License

[Add your license information here]

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository. # awssampleagent
