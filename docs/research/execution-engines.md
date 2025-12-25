# Execution Engines Research

**Last Updated:** 2025-12-25
**Status:** Research Complete - POC In Progress

## Overview

VishkarV2 needs an execution engine to autonomously implement code changes. This document compares the top candidates.

## Comparison Matrix

| Feature | Goose (Block) | Aider | OpenHands |
|---------|---------------|-------|-----------|
| **Local Execution** | Yes | Yes | Docker |
| **MCP Support** | Yes (native) | No | No |
| **Git Awareness** | Yes | Best-in-class | Yes |
| **Autonomous** | Full | Semi | Full |
| **Proven Scale** | 5,000 Block employees | Widely used | Open source |
| **License** | Apache 2.0 | Apache 2.0 | MIT |

## Goose (Block)

**Source:** [github.com/block/goose](https://github.com/block/goose)

### Why Goose is Promising

1. **MCP-Based** - Built on Model Context Protocol (co-developed with Anthropic)
   - Aligns with existing VISHKAR MCP infrastructure
   - Can receive instructions from VishkarV2 orchestrator

2. **Proven at Scale** - 5,000 Block employees use it weekly
   - Real-world validation at enterprise scale
   - Active development and community

3. **Local-First** - Runs entirely on user's machine
   - No cloud sandbox needed
   - Access to user's existing tools (npm, pytest, git)

4. **Recipes** - YAML-based workflow definitions
   - Asynchronous, trigger-driven workflows
   - Can monitor GitHub issues and auto-fix
   - Could integrate with Temporal for durability

5. **Dual Interface** - CLI + Desktop app
   - Flexible for different use cases

### Goose Configuration

```yaml
# ~/.config/goose/profiles/vishkar.yaml
provider: openrouter
model: x-ai/grok-4-fast:free
extensions:
  - name: vishkar-mcp
    type: mcp
    server_url: https://enhanced-context-mcp.vercel.app/api/mcp
```

### Key Commands

```bash
# Install
brew install goose

# Run with profile
goose --profile vishkar

# Run recipe
goose run recipe.yaml
```

## Aider

**Source:** [aider.chat](https://aider.chat/), [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider)

### Strengths

1. **Best-in-class Git Awareness**
   - Clean, atomic commits
   - Meaningful commit messages
   - Multi-file coordinated changes

2. **Architect Mode**
   - Separate planning from implementation
   - Higher-level reasoning for complex tasks

3. **Model Flexibility**
   - Works with Claude, GPT, local models
   - Easy to switch between providers

4. **Proven Track Record**
   - Widely used in developer community
   - Well-documented

### Considerations

- **CLI-only** - Less GUI integration
- **Less autonomous** - Requires more human guidance
- **No native MCP** - Would need adapter

### Key Commands

```bash
# Install
pip install aider-chat

# Run with Claude
aider --model claude-3-5-sonnet-20241022

# Architect mode
aider --architect
```

## OpenHands

**Source:** [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)

### Strengths

1. **Full Autonomy**
   - Shell, browser, file operations
   - Complete development environment

2. **Sandboxed Execution**
   - Docker-based isolation
   - Safe for untrusted operations

3. **Web UI + VS Code Integration**
   - Visual debugging
   - Jupyter notebook support

4. **Integrations**
   - Slack, Jira, Linear
   - GitHub Actions

### Considerations

- **Resource Heavy** - Requires Docker containers
- **Complex Setup** - More infrastructure needed
- **No native MCP** - Would need adapter

### Docker Setup

```bash
# Pull and run
docker pull ghcr.io/all-hands-ai/openhands:latest

docker run -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 3000:3000 \
  ghcr.io/all-hands-ai/openhands:latest
```

## BMAD-METHOD (Research Only)

**Source:** [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)

### Overview

- 21 specialized agents
- 4-phase lifecycle matching SDLC
- Story-driven development
- Scale-adaptive (bug to enterprise)

### Status

Newer project, less proven. Not included in POC but worth monitoring.

## Recommendation

**Start with Goose** because:
1. MCP alignment with existing VISHKAR infrastructure
2. Proven at enterprise scale (Block)
3. Local-first matches user requirement
4. Recipes provide workflow primitives
5. Can be wrapped by Temporal for durability

**Fallback:** Aider for simpler, more controlled implementations

## POC Plan

1. Set up all three engines locally
2. Test with standardized tasks:
   - Simple: Single file change
   - Medium: Multi-file feature
   - Complex: Feature with tests
3. Measure: Speed, quality, reliability, MCP compatibility
4. Select winner

## Related Documents

- [POC Overview](../poc/README.md)
- [Goose Setup](../poc/goose-setup.md)
- [Aider Setup](../poc/aider-setup.md)
- [OpenHands Setup](../poc/openhands-setup.md)
