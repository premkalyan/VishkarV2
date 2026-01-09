# VishkarV2

17-Step SDLC Automation Platform with AI-powered development workflows using Temporal.io.

## Overview

VishkarV2 orchestrates AI coding tools (Aider, Goose) through a 17-step SDLC pipeline, ensuring consistent quality through automated reviews, JIRA integration, and documentation generation.

### Key Features

- **Pluggable Tool Adapters**: Unified interface for Aider, Goose, and local LLMs
- **17-Step SDLC Pipeline**: Automated workflow with quality gates
- **4-Angle Reviews**: Architecture, Security, Code Quality, Tech-Stack
- **MCP Integration**: JIRA ticket management, Confluence documentation
- **Cost Tracking**: Monitor and optimize AI tool spending

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Local LLM (optional): [LMStudio](https://lmstudio.ai/) with Qwen model

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/VishkarV2.git
cd VishkarV2

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create a `.env` file with:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...

# JIRA Configuration
JIRA_HOST=https://your-instance.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-token
JIRA_PROJECT_KEY=V2

# Confluence Configuration
CONFLUENCE_URL=https://your-instance.atlassian.net/wiki
CONFLUENCE_SPACE_KEY=V2

# Local LLM (optional)
LOCAL_LLM_URL=http://127.0.0.1:1234
LOCAL_LLM_MODEL=qwen/qwen3-30b-a3b-2507
```

### Running

```bash
# Run a simple task with Aider
python -m src.cli execute "Fix the bug in utils.py" src/utils.py

# Run with tool selection
python -m src.cli execute "Refactor authentication" --complexity complex
```

## Project Structure

```
VishkarV2/
├── src/
│   ├── adapters/           # Tool adapters (Aider, Goose)
│   │   ├── base/           # Abstract interface
│   │   ├── aider/          # Aider adapter
│   │   └── goose/          # Goose adapter
│   ├── workflows/          # Temporal workflow definitions
│   ├── integrations/       # MCP integrations
│   │   ├── jira/           # JIRA MCP client
│   │   └── confluence/     # Confluence MCP client
│   └── core/               # Shared utilities
├── tests/                  # Test suite
├── docs/                   # Documentation
│   ├── planning/           # Implementation plans
│   └── research/           # Research findings
└── integrations/           # Legacy adapters (to be migrated)
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/adapters/test_aider.py
```

### Code Quality

```bash
# Format code
ruff format src tests

# Lint code
ruff check src tests --fix

# Type check
mypy src
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`:
- Trailing whitespace removal
- Ruff linting and formatting
- Type checking with mypy

## Architecture

### Tool Adapters

All adapters implement the `ToolAdapter` interface:

```python
class ToolAdapter(ABC):
    async def execute(self, prompt: str, files: list[str]) -> ExecutionResult
    async def validate_output(self, result: ExecutionResult) -> bool
    def get_cost(self) -> float
```

### SDLC Pipeline (17 Steps)

1. Task Selection
2. Context Gathering
3. Architecture Review
4. Security Review
5. Code Quality Review
6. Tech-Stack Review
7. Implementation
8. Unit Testing
9. Integration Testing
10. Documentation
11. PR Creation
12. PR Review
13. CI/CD Validation
14. Merge
15. Deployment
16. Verification
17. Closure

## Research Results

Based on our backtesting (14 tests, 100% success):

| Tool | Simple | Medium | Complex | Recommendation |
|------|--------|--------|---------|----------------|
| **Aider** | ✅ 12s | ✅ 10s | ✅ 18s | Primary tool |
| **Goose** | ✅ 25s | ✅ 30s | ✅ 63s | Secondary tool |
| **OpenCode** | ✅ 20s | ✅ 25s | ❌ hung | Simple/Medium only |

## License

MIT
