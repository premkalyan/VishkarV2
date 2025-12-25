# ADR-001: Execution Engine Selection

**Status:** Proposed
**Date:** 2025-12-25
**Decision Makers:** VishkarV2 Team

## Context

VishkarV2 needs an execution engine to autonomously implement code changes as part of the 17-Step SDLC workflow. The engine must:

1. Execute code changes locally on user's machine
2. Integrate with VISHKAR MCP ecosystem
3. Handle multi-file changes reliably
4. Support Git operations
5. Scale to 10,000+ concurrent users (via Temporal)

## Options Considered

### Option 1: Goose (Block)

**Source:** [github.com/block/goose](https://github.com/block/goose)

**Pros:**
- MCP-native (aligns with VISHKAR)
- Proven at scale (5,000+ Block employees)
- Local-first execution
- Recipe-based workflows
- Active development

**Cons:**
- Newer to VishkarV2 team
- Less autonomous than OpenHands

### Option 2: Aider

**Source:** [aider.chat](https://aider.chat/)

**Pros:**
- Best-in-class Git integration
- Clean, atomic commits
- Architect mode for planning
- Widely used and proven

**Cons:**
- CLI-only (harder to orchestrate)
- Less autonomous (needs guidance)
- No MCP support

### Option 3: OpenHands

**Source:** [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)

**Pros:**
- Full autonomy (shell, browser, files)
- Sandboxed execution (Docker)
- Web UI for debugging
- SDK available

**Cons:**
- Resource heavy (Docker required)
- Complex setup
- No native MCP

## Decision

**Selected:** TBD (after POC completion)

## Rationale

TBD (after POC testing with standardized tasks)

## Consequences

### Positive

TBD

### Negative

TBD

### Mitigations

TBD

## POC Results

See [Comparison Matrix](../poc/comparison-matrix.md) for detailed test results.

## Implementation Plan

TBD (after selection)

## References

- [Execution Engines Research](../research/execution-engines.md)
- [POC Overview](../poc/README.md)
- [Architecture Plan](../ARCHITECTURE_PLAN.md)
