# OpenHands Setup Guide

**Story:** [V2-4](https://bounteous.jira.com/browse/V2-4) - Set up OpenHands execution engine locally
**Status:** To Do

## Overview

OpenHands (formerly OpenDevin) is a fully autonomous AI coding agent that runs in a sandboxed Docker environment. It can browse the web, run shell commands, and write code.

**Source:** [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)

## Prerequisites

- Docker Desktop
- 16GB+ RAM recommended
- Anthropic or OpenAI API key

## Installation

### Docker (Recommended)

```bash
# Pull the image
docker pull ghcr.io/all-hands-ai/openhands:latest

# Verify
docker images | grep openhands
```

### From Source

```bash
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands
make build
```

## Configuration

### Environment Variables

Create `.openhands.env`:

```bash
# LLM Configuration
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_API_KEY=${ANTHROPIC_API_KEY}

# Workspace (mounted volume)
WORKSPACE_BASE=/Users/premkalyan/code/VishkarV2

# Sandbox settings
SANDBOX_TYPE=local
```

## Usage

### Start OpenHands

```bash
# Run with Docker
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /Users/premkalyan/code/VishkarV2:/workspace \
  -p 3000:3000 \
  -e LLM_MODEL=claude-3-5-sonnet-20241022 \
  -e LLM_API_KEY=$ANTHROPIC_API_KEY \
  ghcr.io/all-hands-ai/openhands:latest
```

### Access Web UI

Open http://localhost:3000

### Docker Compose

Create `docker-compose.openhands.yml`:

```yaml
version: '3.8'
services:
  openhands:
    image: ghcr.io/all-hands-ai/openhands:latest
    ports:
      - "3000:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./:/workspace
    environment:
      - LLM_MODEL=claude-3-5-sonnet-20241022
      - LLM_API_KEY=${ANTHROPIC_API_KEY}
      - SANDBOX_TYPE=local
    restart: unless-stopped
```

Run:

```bash
docker-compose -f docker-compose.openhands.yml up
```

### Python SDK

```bash
pip install openhands
```

```python
from openhands import OpenHands

agent = OpenHands(
    model="claude-3-5-sonnet-20241022",
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

result = agent.run("Create a FastAPI health check endpoint")
print(result.code_changes)
```

## Verification

### Test Docker Setup

```bash
docker run --rm ghcr.io/all-hands-ai/openhands:latest --version
```

### Test Basic Operation

1. Start OpenHands (Web UI)
2. Enter task: "Create a file called test.txt with 'Hello from OpenHands'"
3. Verify file created in workspace

### Test Sandbox

1. Start OpenHands
2. Enter task: "Run `python --version` and tell me the result"
3. Verify command executed in sandbox

## Acceptance Criteria

- [ ] OpenHands running in Docker
- [ ] Can execute code in sandbox
- [ ] Full autonomy features verified
- [ ] Web UI accessible
- [ ] Claude API integration working

## Features for VishkarV2

### Strengths

1. **Full Autonomy** - Shell, browser, file operations
2. **Sandboxed** - Docker isolation for safety
3. **Web UI** - Visual debugging
4. **Jupyter Support** - Notebook execution

### Limitations

1. **Resource Heavy** - Docker containers
2. **Complex Setup** - More infrastructure
3. **No MCP** - Would need adapter

## Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| CPU | 2 cores | 4+ cores |
| Disk | 10GB | 20GB+ |
| Docker | Yes | Yes |

## Troubleshooting

### Docker Socket Issues

```bash
# Ensure Docker is running
docker info

# Check socket permissions
ls -la /var/run/docker.sock
```

### Memory Issues

```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory
```

### API Issues

```bash
# Test API key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
```

### Container Logs

```bash
docker logs -f $(docker ps -q --filter ancestor=ghcr.io/all-hands-ai/openhands:latest)
```

## Related

- [Execution Engines Research](../research/execution-engines.md)
- [POC Overview](./README.md)
