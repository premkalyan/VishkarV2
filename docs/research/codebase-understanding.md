# Codebase Understanding Tools

**Last Updated:** 2025-12-25
**Status:** Research Complete

## Overview

Before implementing any story, VishkarV2 must understand the existing codebase to avoid mistakes. This document covers tools and approaches for codebase analysis.

## Tool Comparison

| Tool | Approach | Best For | Open Source |
|------|----------|----------|-------------|
| **Repomix** | Repo → single file | Simple, any LLM | Yes |
| **Aider tree-sitter** | AST-based map | Token-optimized | Yes |
| **lsp-mcp** | LSP → MCP bridge | IDE-quality intelligence | Yes |
| **Qodo Context Engine** | Enterprise RAG | 10k+ repos | Enterprise |
| **Sourcegraph** | Semantic search | Cross-repo search | Freemium |

## Repomix (Recommended for MVP)

**Source:** [repomix.com](https://repomix.com/)

### What It Does

Packs entire repository into a single file optimized for LLM context windows.

### Usage

```bash
# Install
npm install -g repomix

# Pack repository
repomix --output context.txt

# With filtering
repomix --include "src/**/*.py" --exclude "**/__pycache__/**"
```

### Output Format

```xml
<file path="src/main.py">
def main():
    print("Hello, World!")
</file>

<file path="src/utils.py">
def helper():
    return 42
</file>
```

### Integration Plan

```
User connects project
    ↓
Run Repomix (simple, reliable)
    ↓
Generate codebase context JSON
    ↓
Store in .vishkar/cache/codebase-context.json
    ↓
Inject into agent system prompts
```

## lsp-mcp (Phase 2)

**Source:** [github.com/jonrad/lsp-mcp](https://github.com/jonrad/lsp-mcp)

### What It Does

Bridges Language Server Protocol to MCP, providing IDE-quality code intelligence.

### Capabilities

- Go to definition
- Find references
- Hover information
- Symbol search
- Diagnostics

### Integration

```json
{
  "mcpServers": {
    "lsp-python": {
      "command": "lsp-mcp",
      "args": ["--lsp", "pylsp"]
    }
  }
}
```

## VISHKAR Context Schema

Already defined in VISHKAR framework:

```json
{
  "project": {
    "name": "VishkarV2",
    "type": "web-application",
    "language": "python",
    "framework": "fastapi"
  },
  "structure": {
    "source_root": "src/",
    "test_root": "tests/",
    "entry_points": ["src/main.py"]
  },
  "dependencies": {
    "runtime": ["fastapi", "uvicorn", "pydantic"],
    "dev": ["pytest", "black", "mypy"]
  },
  "conventions": {
    "naming": "snake_case",
    "imports": "absolute",
    "formatting": "black"
  },
  "modules": [
    {
      "path": "src/api/",
      "purpose": "REST API endpoints",
      "key_files": ["routes.py", "schemas.py"]
    },
    {
      "path": "src/services/",
      "purpose": "Business logic",
      "key_files": ["workflow.py", "jira.py"]
    }
  ],
  "patterns": {
    "dependency_injection": true,
    "service_layer": true
  }
}
```

## Multi-Repository Analysis

### The Challenge

Monorepos have a significant advantage for AI assistants because they provide complete context. With polyrepos, AI suffers from "contextual fragmentation" - each repo interaction lacks memory of other parts of the system.

### Enterprise Solutions (Reference)

| Tool | Capability | Scale |
|------|-----------|-------|
| **Qodo Context Engine** | Traces through 6+ microservices | Enterprise |
| **Augment Code** | 400k-500k files, 12+ services | Enterprise |
| **Sourcegraph Cody** | Universal Code Graph | Enterprise |

### Open Source Options

| Tool | Description | Best For |
|------|-------------|----------|
| **Hound (Etsy)** | Fast regex search, Go backend | Self-hosted search |
| **OpenGrok** | Java-based, cross-reference | Legacy codebases |
| **Zoekt** | Google's trigram search | Raw speed |
| **SeaGOAT** | Semantic vector search | AI-native search |
| **Nx MCP Server** | Monorepo workspace context | Nx monorepos |

### VishkarV2 Approach

**Phase 1 (MVP):**
1. Support single repo analysis (Repomix)
2. Design schema to accommodate multiple repos
3. Store per-repo context in unified format

**Phase 2 (Multi-Repo):**
```
┌─────────────────────────────────────────────────────────────┐
│                    VishkarV2 Multi-Repo                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐             │
│   │  Repo A   │  │  Repo B   │  │  Repo C   │             │
│   │ (Backend) │  │(Frontend) │  │ (Shared)  │             │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘             │
│         │              │              │                    │
│         ▼              ▼              ▼                    │
│   ┌─────────────────────────────────────────────────────┐ │
│   │          Per-Repo Analysis (Repomix)                │ │
│   └─────────────────────────────────────────────────────┘ │
│                         │                                  │
│                         ▼                                  │
│   ┌─────────────────────────────────────────────────────┐ │
│   │           Unified System Context                    │ │
│   │   • Cross-repo dependencies                         │ │
│   │   • Service communication map                       │ │
│   │   • Shared types/interfaces                         │ │
│   │   • API contracts between services                  │ │
│   └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Phase 3 (Scale):**
- Integrate Zoekt/Hound for fast search across repos
- Consider Sourcegraph for enterprise customers

## Implementation Notes

### Cache Strategy

```
.vishkar/
├── cache/
│   ├── codebase-context.json    # Full context
│   ├── file-hashes.json         # For incremental updates
│   └── last-analyzed.txt        # Timestamp
└── config/
    └── analysis.yaml            # Exclusions, rules
```

### Incremental Updates

1. Watch for file changes
2. Hash comparison for modified files
3. Re-analyze only changed modules
4. Update context incrementally

### Token Optimization

- Prioritize files related to current task
- Use graph ranking (files with most imports first)
- Summarize large files
- Exclude generated code

## Related Documents

- [Execution Engines](./execution-engines.md)
- [Architecture Plan](../ARCHITECTURE_PLAN.md)
