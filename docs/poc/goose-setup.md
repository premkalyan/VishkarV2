# Goose Setup Guide

**Story:** [V2-2](https://bounteous.jira.com/browse/V2-2) - Set up Goose execution engine locally
**Status:** Complete
**Verified:** 2025-12-25

## Overview

Goose is an AI-powered development agent from Block (formerly Square). It's MCP-native and used by 5,000+ Block employees.

**Source:** [github.com/block/goose](https://github.com/block/goose)

## Prerequisites

- macOS or Linux
- Python 3.10+
- OpenRouter API key (or other LLM provider)

## Installation

### Option 1: Homebrew (macOS)

```bash
brew install goose
```

### Option 2: pip

```bash
pip install goose-ai
```

### Option 3: From source

```bash
git clone https://github.com/block/goose.git
cd goose
pip install -e .
```

## Configuration

### Create VishkarV2 Profile

```bash
mkdir -p ~/.config/goose/profiles
```

Create `~/.config/goose/profiles/vishkar.yaml`:

```yaml
# VishkarV2 Goose Profile
provider: openrouter
model: x-ai/grok-4-fast:free

# MCP Extensions
extensions:
  - name: enhanced-context
    type: mcp
    server_url: https://enhanced-context-mcp.vercel.app/api/mcp
    headers:
      X-API-Key: ${PROJECT_REGISTRY_TOKEN}

  - name: jira
    type: mcp
    server_url: https://jira-mcp-pi.vercel.app/api/mcp
    headers:
      Authorization: Bearer ${PROJECT_REGISTRY_TOKEN}

# Working directory
workspace: /Users/premkalyan/code/VishkarV2
```

### Environment Variables

Add to `.env`:

```bash
# Already configured
GOOSE_PROVIDER=openrouter
GOOSE_MODEL=x-ai/grok-4-fast:free
GOOSE_API_KEY=${OPENROUTER_API_KEY}
```

## Usage

### Basic Commands

```bash
# Start interactive session
goose

# Start with VishkarV2 profile
goose --profile vishkar

# Run a recipe
goose run recipe.yaml

# One-shot command
goose "Add a health check endpoint to the API"
```

### Example Recipe

```yaml
# recipes/add-endpoint.yaml
name: Add API Endpoint
description: Creates a new FastAPI endpoint with model and service

steps:
  - name: Create model
    prompt: |
      Create a Pydantic model for the endpoint in src/models/

  - name: Create service
    prompt: |
      Create a service module in src/services/ that uses the model

  - name: Create route
    prompt: |
      Create a FastAPI route in src/api/routes/ that uses the service

  - name: Add tests
    prompt: |
      Create unit tests for the service in tests/
```

## Verification

### Test Installation

```bash
goose --version
```

### Test Basic Operation

```bash
cd /Users/premkalyan/code/VishkarV2
goose "Create a file called test.txt with 'Hello from Goose'"
```

### Test MCP Integration

```bash
goose --profile vishkar "What SDLC steps are available?"
```

## Acceptance Criteria

- [x] Goose installed and running (v1.6.0)
- [x] Can execute simple file operations
- [x] VishkarV2 profile configured (using existing OpenRouter config)
- [ ] MCP integration verified (Enhanced Context) - deferred to POC tests
- [x] OpenRouter API working (grok-4-fast:free)

## Verification Results

**Date:** 2025-12-25

```
$ goose info
Goose Version:
  Version:          1.6.0
Config file:      /Users/premkalyan/.config/goose/config.yaml
Sessions dir:     /Users/premkalyan/.local/share/goose/sessions
Logs dir:         /Users/premkalyan/.local/state/goose/logs
```

**Configuration:**
- Provider: OpenRouter
- Model: x-ai/grok-4-fast:free
- Extensions: developer, memory, computercontroller, autovisualiser

## Notes

- Goose sessions persist state; use `goose clear` to reset
- Logs are in `~/.goose/logs/`
- Recipe files can be version controlled

## Troubleshooting

### API Key Issues

```bash
# Verify API key
echo $OPENROUTER_API_KEY

# Test directly
curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### MCP Connection Issues

```bash
# Test MCP directly
curl -X POST https://enhanced-context-mcp.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PROJECT_REGISTRY_TOKEN" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Related

- [Execution Engines Research](../research/execution-engines.md)
- [POC Overview](./README.md)
