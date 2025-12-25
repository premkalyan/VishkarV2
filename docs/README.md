# VishkarV2 Documentation

**VishkarV2** is the implementation phase of VISHKAR - a 17-Step SDLC platform for autonomous software development.

## Documentation Structure

| Directory | Purpose | Confluence Location |
|-----------|---------|---------------------|
| [architecture/](./architecture/) | System design, diagrams, patterns | V2 > Architecture |
| [research/](./research/) | Deep research findings | V2 > Research |
| [poc/](./poc/) | POC execution and findings | V2 > POC |
| [decisions/](./decisions/) | Architecture Decision Records | V2 > Decisions |

## Quick Links

### Architecture
- [Architecture Plan](./ARCHITECTURE_PLAN.md) - Complete system design

### Research
- [Execution Engines](./research/execution-engines.md) - Goose, Aider, OpenHands comparison
- [Temporal.io](./research/temporal-io.md) - Durable workflow execution
- [Codebase Understanding](./research/codebase-understanding.md) - Repomix, lsp-mcp, tools

### POC Phase
- [POC Overview](./poc/README.md) - Phase 0 goals and tracking
- [Goose Setup](./poc/goose-setup.md) - V2-2
- [Aider Setup](./poc/aider-setup.md) - V2-3
- [OpenHands Setup](./poc/openhands-setup.md) - V2-4
- [Comparison Matrix](./poc/comparison-matrix.md) - V2-8

## Sync with Confluence

All documentation in this directory is synced to Confluence space **V2**.

To update Confluence from local:
```bash
# Using VishkarV2 sync script (TBD)
./scripts/sync-confluence.sh
```

## JIRA Tracking

| Epic | Key | Status |
|------|-----|--------|
| POC: Execution Engine Comparison | V2-1 | In Progress |

See [JIRA Board](https://bounteous.jira.com/jira/software/projects/V2/boards) for full backlog.
