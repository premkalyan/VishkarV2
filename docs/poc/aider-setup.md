# Aider Setup Guide

**Story:** [V2-3](https://bounteous.jira.com/browse/V2-3) - Set up Aider execution engine locally
**Status:** To Do

## Overview

Aider is an AI pair programming tool with best-in-class Git integration. It creates clean, atomic commits and handles multi-file changes seamlessly.

**Source:** [aider.chat](https://aider.chat/), [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider)

## Prerequisites

- Python 3.9+
- Git
- Claude API key (recommended) or OpenAI API key

## Installation

### pip (Recommended)

```bash
pip install aider-chat
```

### pipx (Isolated)

```bash
pipx install aider-chat
```

### Homebrew

```bash
brew install aider
```

## Configuration

### API Keys

Add to `.env`:

```bash
# Already configured
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
```

### Aider Config File

Create `~/.aider.conf.yml`:

```yaml
# Default model
model: claude-3-5-sonnet-20241022

# Git settings
auto-commits: true
dirty-commits: false
attribute-author: true
attribute-committer: true

# Code style
edit-format: diff
stream: true

# Architecture mode for complex tasks
architect: false
```

### Project-Specific Config

Create `.aider.conf.yml` in VishkarV2 root:

```yaml
# VishkarV2 Aider Config
model: claude-3-5-sonnet-20241022

# Project context
read:
  - docs/ARCHITECTURE_PLAN.md
  - docs/research/execution-engines.md

# Ignore patterns
ignore:
  - .env
  - "*.pyc"
  - __pycache__
  - .git
```

## Usage

### Basic Commands

```bash
# Start interactive session
cd /Users/premkalyan/code/VishkarV2
aider

# Start with specific model
aider --model claude-3-5-sonnet-20241022

# Start with specific files
aider src/main.py src/api/routes.py

# Architect mode for planning
aider --architect
```

### In-Session Commands

```
/add <file>       - Add file to context
/drop <file>      - Remove file from context
/clear            - Clear conversation
/tokens           - Show token usage
/diff             - Show pending changes
/undo             - Undo last commit
/run <command>    - Run shell command
```

### Example Session

```
$ aider

aider> Add a health check endpoint at /api/health that returns {"status": "ok"}

I'll create a health check endpoint. Let me add the necessary files.

src/api/health.py
<<<<<<< SEARCH
=======
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}
>>>>>>> REPLACE

src/main.py
<<<<<<< SEARCH
app = FastAPI()
=======
from src.api.health import router as health_router

app = FastAPI()
app.include_router(health_router, prefix="/api")
>>>>>>> REPLACE

Commit: feat: add health check endpoint
```

## Verification

### Test Installation

```bash
aider --version
```

### Test Basic Operation

```bash
cd /Users/premkalyan/code/VishkarV2
aider --message "Create a file called test.txt with 'Hello from Aider'"
```

### Test Git Integration

```bash
aider --message "Add a TODO comment to README.md"
git log -1  # Should show Aider's commit
```

## Acceptance Criteria

- [ ] Aider installed and running
- [ ] Can execute code edits with git commits
- [ ] Multi-file changes work
- [ ] Claude API integration verified
- [ ] Architect mode tested

## Features for VishkarV2

### Strengths

1. **Git Awareness** - Clean, atomic commits
2. **Architect Mode** - Separate planning from coding
3. **Multi-file** - Coordinated changes across files
4. **Context Management** - `/add` and `/drop` commands

### Limitations

1. **CLI-only** - No GUI/API
2. **Less autonomous** - Requires human guidance
3. **No MCP** - Can't integrate with VISHKAR MCPs directly

## Troubleshooting

### API Key Issues

```bash
# Verify key
echo $ANTHROPIC_API_KEY

# Test with explicit key
aider --anthropic-api-key $ANTHROPIC_API_KEY
```

### Git Issues

```bash
# Aider needs a git repo
git status

# Ensure clean state
git stash
```

### Token Limits

```bash
# Use map for large repos
aider --map-tokens 2048

# Check token usage
aider
aider> /tokens
```

## Related

- [Execution Engines Research](../research/execution-engines.md)
- [POC Overview](./README.md)
