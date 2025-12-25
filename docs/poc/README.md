# Phase 0: Execution Engine POC

**Epic:** [V2-1](https://bounteous.jira.com/browse/V2-1) - POC: Execution Engine Comparison
**Status:** In Progress
**Started:** 2025-12-25

## Objective

Compare execution engines (Goose, Aider, OpenHands) to select the best option for VishkarV2.

## Success Criteria

- All three engines tested with standardized tasks
- Comparison matrix completed with quantitative metrics
- Clear winner selected with documented rationale
- Integration plan for selected engine

## Stories

| Key | Summary | Status | Assignee |
|-----|---------|--------|----------|
| [V2-2](https://bounteous.jira.com/browse/V2-2) | Set up Goose execution engine locally | To Do | - |
| [V2-3](https://bounteous.jira.com/browse/V2-3) | Set up Aider execution engine locally | To Do | - |
| [V2-4](https://bounteous.jira.com/browse/V2-4) | Set up OpenHands execution engine locally | To Do | - |
| [V2-5](https://bounteous.jira.com/browse/V2-5) | POC Test: Simple task - single file change | To Do | - |
| [V2-6](https://bounteous.jira.com/browse/V2-6) | POC Test: Medium task - multi-file feature | To Do | - |
| [V2-7](https://bounteous.jira.com/browse/V2-7) | POC Test: Complex task - feature with tests | To Do | - |
| [V2-8](https://bounteous.jira.com/browse/V2-8) | POC Evaluation: Document findings and select winner | To Do | - |

## Test Tasks

### Simple Task (V2-5)
**Task:** Add a utility function to an existing file

```
Target: Add a `format_date()` function to utils.py
Expected: Single file change, clean commit
```

### Medium Task (V2-6)
**Task:** Add a new API endpoint with model, service, and route

```
Target: Create /api/health endpoint with:
- Model: HealthStatus
- Service: health_service.py
- Route: health_router.py
Expected: 3+ file changes, proper imports
```

### Complex Task (V2-7)
**Task:** Implement a feature with unit tests and integration tests

```
Target: Add configuration management feature with:
- Config loader (YAML/JSON)
- Validation with Pydantic
- Unit tests (90% coverage)
- Integration test
Expected: 5+ files, tests pass
```

## Evaluation Criteria

| Criterion | Weight | Measurement |
|-----------|--------|-------------|
| **Speed** | 20% | Time to completion |
| **Quality** | 30% | Code review score, best practices |
| **Reliability** | 25% | Success rate, error recovery |
| **MCP Compatibility** | 15% | Integration with VISHKAR MCPs |
| **Developer Experience** | 10% | Setup complexity, usability |

## Test Environment

```
Repository: VishkarV2 (this repo)
Branch: poc-tests
Framework: Python/FastAPI (to be set up)
```

## Setup Instructions

- [Goose Setup](./goose-setup.md)
- [Aider Setup](./aider-setup.md)
- [OpenHands Setup](./openhands-setup.md)

## Results

See [Comparison Matrix](./comparison-matrix.md) for detailed results.

## Timeline

| Week | Activities |
|------|------------|
| Week 1 | Set up all three engines (V2-2, V2-3, V2-4) |
| Week 1-2 | Run tests (V2-5, V2-6, V2-7) |
| Week 2 | Evaluate and document (V2-8) |

## Decision

**Selected Engine:** TBD

**Rationale:** TBD

See [ADR-001: Execution Engine Selection](../decisions/ADR-001-execution-engine.md)
