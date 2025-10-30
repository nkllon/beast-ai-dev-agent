# Beast AI Development Agent

> Platform-agnostic AI development agents for cloud platforms (GKE, Cloud Run, Cloud Functions)

[![PyPI version](https://img.shields.io/pypi/v/beast-ai-dev-agent)](https://pypi.org/project/beast-ai-dev-agent/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 **Platform Agnostic**: Same agent code runs on GKE, Cloud Run, or Cloud Functions
- 🤖 **Beast Mode Integration**: Optional multi-agent coordination via Redis pub/sub
- 📊 **Built-in Observability**: Health checks, metrics, and structured logging
- ⚡ **Fast**: Optimized for low latency and minimal cold starts
- 🔒 **Secure**: Best practices for authentication and error handling
- 📦 **Easy to Use**: Simple API, comprehensive examples

## Quick Start

### Installation

```bash
# Basic installation
uv add beast-ai-dev-agent

# With Beast Mode support
uv add beast-ai-dev-agent[beast-mode]

# With all optional features
uv add beast-ai-dev-agent[all]
```

### Cloud Run Example

```python
from beast_ai_dev_agent import CloudRunKiroAgent

# Create and run agent
agent = CloudRunKiroAgent()
agent.run()  # Starts on port 8080
```

### GKE Example

```python
from beast_ai_dev_agent import GKEKiroAgent

# Create GKE-optimized agent
agent = GKEKiroAgent()
agent.run(host="0.0.0.0", port=8080)
```

### Cloud Functions Example

```python
from beast_ai_dev_agent import CloudFunctionsKiroAgent, create_kiro_request_from_flask

agent = CloudFunctionsKiroAgent()

def kiro_agent_http(request):
    """Cloud Function entry point"""
    kiro_request = create_kiro_request_from_flask(request)
    kiro_response = agent.process_request(kiro_request)
    return kiro_response.data, kiro_response.status_code
```

## API Endpoints

### Cloud Run / GKE

- `GET /` - Service information
- `GET /health` - Health check
- `POST /analyze` - Data analysis endpoint
- `GET /metrics` - Performance metrics

### Example Request

```bash
curl -X POST https://your-service.run.app/analyze \
  -H "Content-Type: application/json" \
  -d '{"data": "your analysis data"}'
```

## Configuration

### Environment Variables

```bash
# Port configuration
PORT=8080

# Beast Mode (optional)
BEAST_MODE_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379

# Platform detection (auto-detected)
PLATFORM=cloudrun  # or gke, cloud_functions
```

## Platform Support

| Platform | Status | Features |
|----------|--------|----------|
| **Cloud Run** | ✅ Full | HTTP endpoints, auto-scaling, health checks |
| **GKE** | ✅ Full | Kubernetes-aware, service mesh ready |
| **Cloud Functions** | ✅ Full | Serverless, optimized cold starts |

## Beast Mode Integration

Enable multi-agent coordination:

```python
import os
from beast_ai_dev_agent import CloudRunKiroAgent

# Enable Beast Mode
os.environ["BEAST_MODE_ENABLED"] = "true"
os.environ["REDIS_HOST"] = "your-redis-host"

agent = CloudRunKiroAgent()
agent.run()
```

## Development

```bash
# Clone repository
git clone https://github.com/nkllon/beast-ai-dev-agent.git
cd beast-ai-dev-agent

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Format code
uv run black src/ tests/

# Type check
uv run mypy src/
```

## Architecture

```
beast_ai_dev_agent/
├── common/          # Shared interfaces and models
├── cloudrun/        # Cloud Run implementation
├── gke/             # GKE implementation  
├── cloud_functions/ # Cloud Functions implementation
├── beast_mode/      # Multi-agent coordination
└── utils/           # Logging, metrics, helpers
```

## Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Cloud Run Deployment](docs/platforms/cloudrun.md)
- [GKE Deployment](docs/platforms/gke.md)
- [Cloud Functions Deployment](docs/platforms/cloud_functions.md)
- [Beast Mode Guide](docs/beast_mode.md)

## Requirements

- Python 3.10+
- FastAPI / Uvicorn (for Cloud Run/GKE)
- Redis (optional, for Beast Mode)

## Use Cases

- **AI Development Agents**: Hackathon submissions for Kiro, TiDB, GKE hackathons
- **Multi-Agent Systems**: Coordinate multiple AI agents via Beast Mode
- **Microservices**: Deploy as cloud-native microservices
- **Serverless Functions**: Low-latency serverless AI agents

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details

## Attribution

Created for the OpenFlow Playground project and hackathon submissions.

- [OpenFlow Playground](https://github.com/louspringer/OpenFlow-Playground)
- Part of the Beast Mode multi-agent framework

## Links

- **GitHub**: https://github.com/nkllon/beast-ai-dev-agent
- **PyPI**: https://pypi.org/project/beast-ai-dev-agent/
- **Issues**: https://github.com/nkllon/beast-ai-dev-agent/issues
- **OpenFlow Playground**: https://github.com/louspringer/OpenFlow-Playground

---

**Status**: Alpha Release (v0.1.0)  
**Maintainer**: Lou Springer  
**Last Updated**: 2025-01-30

