# VishkarV2 Architecture Plan

**Status:** Research Complete - Awaiting Decisions
**Date:** 2025-12-24

---

## 1. Executive Summary

VishkarV2 is a **continuation** of VISHKAR, adding the 17-Step SDLC implementation phase on top of the existing foundation (Project Registry, Enhanced Context MCP, LangGraph orchestration).

**Key Requirements:**
- Temporal.io for reliability at scale (10,000+ concurrent users)
- Agentic execution (not simple state machine)
- LangGraph orchestration retained
- Execution engine to be finalized (OpenHands / BMAD-METHOD / Aider)

---

## 2. Research Findings

### 2.1 Current VISHKAR Orchestration

**Location:** `/Users/premkalyan/code/VISHKAR/`

| Component | Implementation | Notes |
|-----------|---------------|-------|
| **Orchestration** | LangGraph StateGraph | workflow_parallel.py (369 lines) |
| **Parallelism** | ThreadPoolExecutor | 3 agents run simultaneously |
| **State** | TypedDict (in-memory) | DiscussionState in state.py |
| **Agents** | Alex (PM), Blake (Architect), Casey (PM) | agents.py (287 lines) |
| **Consensus** | Sign-off detection | consensus.py (132 lines) |
| **MCP** | HTTP POST to MCP servers | JIRA, Confluence, Enhanced Context |

**Key Pattern:** Parallel agent execution with conditional routing and consensus detection.

### 2.2 Temporal.io for AI Agents

**Sources:** [Temporal for AI](https://temporal.io/solutions/ai), [Durable Execution for AI](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai)

**Key Finding:** [Replit uses Temporal](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal) for their AI coding assistant at massive scale.

| Feature | Benefit for VishkarV2 |
|---------|----------------------|
| **Durable Execution** | Workflows survive server restarts, network failures |
| **State Persistence** | Multi-day implementation cycles with checkpoints |
| **Automatic Retries** | Handle LLM API failures gracefully |
| **Human Intervention** | Pause/resume for approval gates |
| **Schedules** | Ambient agents running on schedules |
| **Non-deterministic LLMs** | Deterministic workflow with non-deterministic decisions |

**Architecture Pattern:**
```
Temporal Workflow (durable, long-running)
    ↓
Activities (LangGraph agent calls, MCP calls, tool execution)
    ↓
External Systems (JIRA, GitHub, Claude API, Execution Engine)
```

### 2.3 Execution Engine Options

#### Option A: OpenHands
**Source:** [OpenHands GitHub](https://github.com/All-Hands-AI/OpenHands)

| Pros | Cons |
|------|------|
| Full autonomy (shell, browser, files) | Resource heavy (Docker containers) |
| Python SDK for orchestration | Complex setup |
| Scale to 1000s of agents | Learning curve |
| Integrations (Slack, Jira, Linear) | |

#### Option B: BMAD-METHOD
**Source:** [BMAD-METHOD GitHub](https://github.com/bmad-code-org/BMAD-METHOD)

| Pros | Cons |
|------|------|
| 21 specialized agents | Newer, less proven |
| 4-phase lifecycle matches SDLC | Requires customization |
| Story-driven development | |
| Scale-adaptive (bug to enterprise) | |

#### Option C: Aider
**Sources:** [Aider](https://aider.chat/), [Aider GitHub](https://github.com/Aider-AI/aider)

| Pros | Cons |
|------|------|
| Git-aware, clean commit history | CLI-based (less programmatic control) |
| Multi-file changes | No built-in orchestration |
| Architect mode for planning | |
| Proven, widely used | |
| Works with Claude, GPT, local models | |

#### Option D: Claude Code (Current)
| Pros | Cons |
|------|------|
| Already integrated | MCP timeout bug (10-15s limit) |
| High quality | Rate limits |
| Tool use | Cost at scale |

### 2.4 Architecture Comparison

| Approach | Orchestration | Execution | State | Scale |
|----------|--------------|-----------|-------|-------|
| **Current VISHKAR** | LangGraph | Claude API | In-memory | Single user |
| **Temporal + OpenHands** | Temporal | OpenHands containers | Durable | 10,000+ |
| **Temporal + Aider** | Temporal | Aider CLI | Durable | 10,000+ |
| **Temporal + BMAD** | Temporal | BMAD agents | Durable | 10,000+ |

---

## 3. Proposed Architecture

### 3.1 High-Level Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VishkarV2 Architecture                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                     Web UI (Next.js 15)                            │    │
│   │  • Project Dashboard    • Story Board    • 17-Step Workflow View  │    │
│   │  • Real-time Updates    • Approval Gates • Progress Monitoring    │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                     │                                       │
│                                     ▼                                       │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                    VishkarV2 API (FastAPI)                         │    │
│   │  • Project Management   • Workflow Triggers   • WebSocket Events  │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                     │                                       │
│                                     ▼                                       │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                      Temporal.io Server                            │    │
│   │  • Durable Workflows    • State Persistence   • Retry Logic       │    │
│   │  • Human Approval Gates • Scheduling          • Monitoring        │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                     │                                       │
│         ┌───────────────────────────┼───────────────────────────┐          │
│         ▼                           ▼                           ▼          │
│   ┌─────────────┐           ┌─────────────┐           ┌─────────────┐     │
│   │  LangGraph  │           │  Execution  │           │    MCPs     │     │
│   │   Agents    │           │   Engine    │           │             │     │
│   │             │           │             │           │ • Project   │     │
│   │ • 4-Angle   │           │ • OpenHands │           │   Registry  │     │
│   │   Review    │           │ • Aider     │           │ • Enhanced  │     │
│   │ • Planning  │           │ • BMAD      │           │   Context   │     │
│   │ • QA        │           │ • Claude    │           │ • JIRA      │     │
│   └─────────────┘           └─────────────┘           │ • Confluence│     │
│                                     │                 └─────────────┘     │
│                                     ▼                                       │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                   User's Local Repository                          │    │
│   │  • Git Operations   • File Changes   • Test Execution             │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Temporal Workflow Design

```python
# Pseudo-code for 17-Step SDLC Workflow

@workflow.defn
class SDLCWorkflow:
    @workflow.run
    async def run(self, task: TaskInput) -> TaskOutput:
        # Step 1: Task Selection
        await workflow.execute_activity(
            select_task, task, start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 2: Implementation
        impl_result = await workflow.execute_activity(
            execute_implementation, task,
            start_to_close_timeout=timedelta(hours=2),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

        # Steps 3-6: 4-Angle Review (parallel)
        reviews = await asyncio.gather(
            workflow.execute_activity(architecture_review, impl_result),
            workflow.execute_activity(security_review, impl_result),
            workflow.execute_activity(quality_review, impl_result),
            workflow.execute_activity(techstack_review, impl_result),
        )

        # Quality Gate: Check for Critical/High issues
        if has_blocking_issues(reviews):
            # Step 7: Feedback Implementation
            await workflow.execute_activity(fix_issues, reviews)
            # Retry reviews...

        # Steps 8-11: Testing
        test_result = await workflow.execute_activity(
            run_tests, impl_result,
            start_to_close_timeout=timedelta(minutes=30)
        )

        # Quality Gate: 90% pass, 80% coverage
        if not meets_test_threshold(test_result):
            raise QualityGateFailure("Tests below threshold")

        # Step 12: PR Creation
        pr = await workflow.execute_activity(create_pr, impl_result)

        # Step 13-14: PR Review + Feedback (PR-Agent)
        pr_feedback = await workflow.execute_activity(pr_agent_review, pr)
        await workflow.execute_activity(implement_pr_feedback, pr_feedback)

        # Step 15: CI/CD
        ci_result = await workflow.execute_activity(wait_for_ci, pr)

        # Step 16: Human Approval Gate (ONLY human gate)
        approved = await workflow.wait_condition(
            lambda: self.human_approved,
            timeout=timedelta(days=7)
        )

        # Step 17: Story Closure
        await workflow.execute_activity(close_story, task, pr)

        return TaskOutput(success=True, pr_url=pr.url)
```

### 3.3 LangGraph + Temporal Integration

**Pattern:** Temporal orchestrates the 17-step workflow, LangGraph orchestrates agent discussions within steps.

```
Temporal Workflow (17 steps, durable)
    ├── Step 3: Architecture Review
    │       └── Temporal Activity → LangGraph Agent Discussion
    │                                   └── Multiple agents discuss
    │                                   └── Consensus reached
    │                                   └── Return findings
    │
    ├── Step 4: Security Review
    │       └── Temporal Activity → LangGraph Agent Discussion
    │                                   └── ...
```

---

## 4. User Decisions (Confirmed)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Repository** | Separate VishkarV2 repo | Clean from Phase 1 complexity; Phase 2 for production use |
| **Temporal** | Start local, migrate later | Docker Compose for dev, Cloud/K8s for production |
| **Local Access** | User's local machine | Most developers have local setup; no cloud dependency |

---

## 5. Execution Engine Deep Comparison

### Comparison Matrix

| Tool | Local? | MCP? | Git-aware? | Autonomous? | Proven Scale | License |
|------|--------|------|------------|-------------|--------------|---------|
| **Goose (Block)** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Full | 5,000 Block employees | Apache 2.0 |
| **OpenHands** | ✅ Docker | ❌ No | ✅ Yes | ✅ Full | Open source community | MIT |
| **Aider** | ✅ Yes | ❌ No | ✅✅ Best | ⚠️ Semi | Widely used | Apache 2.0 |
| **BMAD-METHOD** | ❓ | ❌ No | ❓ | ✅ Full | Newer | MIT |

### Goose (Block) - **Recommended Starting Point**
**Source:** [GitHub - block/goose](https://github.com/block/goose)

**Why Goose is promising for VishkarV2:**
1. **MCP-Based** - Built on Model Context Protocol (co-developed with Anthropic) - aligns with VISHKAR MCPs!
2. **Proven at Scale** - 5,000 Block employees use it weekly
3. **Local-First** - Runs entirely on user's machine
4. **Recipes** - YAML-based workflow definitions for multi-step tasks
5. **Extensible** - Modular architecture with plugin system
6. **Dual Interface** - CLI + Desktop app

**Goose "Recipes":**
- Asynchronous, trigger-driven workflows
- Can monitor GitHub issues and auto-fix
- YAML-based task specifications
- Could potentially integrate with Temporal for durability

### OpenHands - **Enterprise Alternative**
**Source:** [GitHub - All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)

**Strengths:**
- Full autonomous agent (code, terminal, browser, APIs)
- Web UI + VS Code integration
- Jupyter notebook support
- Docker sandboxed execution

**Considerations:**
- More resource-heavy (Docker containers)
- No native MCP support (would need adapter)

### Aider - **Best for Incremental Work**
**Source:** [Aider.chat](https://aider.chat/)

**Strengths:**
- Best-in-class Git awareness (clean commits)
- Multi-file coordinated changes
- Architect mode for planning
- Works with any LLM

**Considerations:**
- CLI-only (less GUI integration)
- Less autonomous than Goose/OpenHands
- No native MCP support

### Recommendation
**Start with Goose** because:
1. MCP alignment with existing VISHKAR infrastructure
2. Proven at enterprise scale (Block)
3. Local-first matches user requirement
4. Recipes provide workflow primitives
5. Can be wrapped by Temporal for durability

**Fallback:** Aider for simpler, more controlled implementations

---

## 6. Codebase Understanding Tools

### Critical Requirement
Before implementing any story, VishkarV2 must understand the existing codebase to avoid mistakes.

### Tool Options

| Tool | Approach | Best For | Open Source |
|------|----------|----------|-------------|
| **Repomix** | Repo → single file | Simple, any LLM | ✅ Yes |
| **Aider tree-sitter** | AST-based map | Token-optimized, language-aware | ✅ Yes |
| **lsp-mcp** | LSP → MCP bridge | IDE-quality intelligence | ✅ Yes |
| **Qodo Context Engine** | Enterprise RAG | 10k+ repos | ❌ Enterprise |
| **Sourcegraph** | Semantic search | Cross-repo search | ⚠️ Freemium |

### Recommended Approach

**Phase 1 (MVP):**
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

**Phase 2 (Enhanced):**
- Add lsp-mcp for IDE-quality code intelligence
- Graph ranking for token optimization
- Incremental updates when files change

**Phase 3 (Scale):**
- Sourcegraph integration for multi-repo
- Custom knowledge graph

### VISHKAR Schema (Already Defined)
```json
{
  "project": { "name", "type", "language", "framework" },
  "structure": { "source_root", "test_root", "entry_points" },
  "dependencies": { "runtime", "dev" },
  "conventions": { "naming", "imports", "formatting" },
  "modules": [{ "path", "purpose", "key_files" }],
  "patterns": { "dependency_injection", "service_layer" }
}
```

### Multi-Repository Analysis (Research Complete)

**Key Insight:** Monorepos have a significant advantage for AI assistants because they provide complete context. With polyrepos, AI suffers from "contextual fragmentation" - each repo interaction lacks memory of other parts of the system.

**Enterprise Solutions (Reference):**
| Tool | Capability | Scale | License |
|------|-----------|-------|---------|
| **Qodo Context Engine** | Traces through 6+ microservices | Enterprise | Commercial |
| **Augment Code** | 400k-500k files, 12+ services | Enterprise | Commercial |
| **Sourcegraph Cody** | Universal Code Graph | Enterprise | Freemium |

**Open Source Options:**
| Tool | Description | Best For |
|------|-------------|----------|
| **Hound (Etsy)** | Fast regex search, Go backend | Self-hosted search |
| **OpenGrok** | Java-based, cross-reference | Legacy codebases |
| **Zoekt** | Google's trigram search | Raw speed |
| **SeaGOAT** | Semantic vector search | AI-native search |
| **Nx MCP Server** | Monorepo workspace context | Nx monorepos |

**Sources:**
- [Qodo Context Engine](https://www.qodo.ai/blog/introducing-qodo-aware-deep-codebase-intelligence-for-enterprise-development/)
- [Augment Code](https://www.augmentcode.com/guides/monorepo-vs-multi-repo-ai-architecture-based-ai-tool-selection)
- [Monorepo.tools AI](https://monorepo.tools/ai)
- [Hound](https://github.com/etsy/hound)

**Recommended Approach for VishkarV2:**

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
│   │   • Structure   • Dependencies   • Patterns         │ │
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
│                         │                                  │
│                         ▼                                  │
│   ┌─────────────────────────────────────────────────────┐ │
│   │        Inject into Agent System Prompts             │ │
│   └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Phase 3 (Scale):**
- Integrate Zoekt/Hound for fast search across repos
- Consider Sourcegraph for enterprise customers

---

## 7. Local Agent Architecture

### Options Researched

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Goose local** | Already runs locally | MCP-based, proven | New to VishkarV2 |
| **Custom daemon** | Build WebSocket service | Full control | Development effort |
| **E2B/AgentSphere** | Ephemeral sandboxes | Secure, isolated | Cloud-dependent |
| **OpenHands Docker** | Containerized | Sandboxed | Resource heavy |

### Recommended: Goose as Local Agent

**Architecture:**
```
VishkarV2 API (Temporal orchestrator)
    ↓ (instructions via MCP or WebSocket)
Goose (local on user's machine)
    ↓
User's Repository (file/git operations)
```

**Why this works:**
1. Goose already speaks MCP - can receive instructions from VishkarV2
2. Local execution - no cloud sandbox needed
3. User's existing tools - npm, pytest, git all available
4. Recipes - can define VishkarV2 workflow steps as Goose recipes

---

## 8. Decisions Made

| Question | Decision | Notes |
|----------|----------|-------|
| **Execution Engine** | POC comparison first | Compare Goose vs Aider vs OpenHands |
| **Multi-repo** | Research first, support from MVP | Design schema for multi-repo from start |
| **Database** | PostgreSQL + Prisma | Continue from VISHKAR pattern |

## 8.1 Reference Project Analysis (COMPLETE)

**Project:** `/Users/premkalyan/code/CincaraProd/Cincara-Context/`
**API Key:** `pk_wo1F6KQEYNFQBPdmjlsKSlR_EVcn-EBSgAkJV7srKf4`

### What Claude Does VERY WELL:
| Aspect | Evidence |
|--------|----------|
| **Architecture** | Clean service/model/schema separation |
| **Type Safety** | 100% type hints, Pydantic validation |
| **Testing** | 33 test files, ~5,900 lines, factories/fixtures |
| **Security** | OWASP-aware (SSRF, SQL injection prevention) |
| **4-Angle Reviews** | V1-49_findings.json with 11 issues (9 fixed) |
| **Documentation** | IMPLEMENTATION_PLAN.md, .standards/, retrospectives |
| **CI/CD** | GitHub Actions (lint, security, tests) |

### What Claude Tends to SKIP:
| Gap | Description |
|-----|-------------|
| **JIRA Transitions** | V1-81 coded without "In Progress" transition |
| **Async Workers** | Celery architecture defined but not implemented |
| **Frontend** | Phase 6 completely deferred |
| **Some Security Headers** | SEC-003 deferred to later phase |
| **Structured Logging** | QUAL-002 deferred |

### Key Statistics:
- **13 JIRA tickets** completed (V1-49 through V1-86)
- **33 test files** with 5,914 lines of test code
- **9 database models** + 8 service modules
- **11 findings** in 4-Angle review (9 fixed, 2 deferred)
- **1 SDLC gap** documented in retrospective

### Critical Insight for VishkarV2:
Claude implements **depth-first by phase** and when gaps occur (like V1-81), documents them in retrospectives rather than silently ignoring. **VishkarV2 must automate SDLC enforcement** to prevent these gaps.

## 8.2 POC Scope (Confirmed)

**Test all levels:**
1. Simple (single file change)
2. Medium (multi-file feature)
3. Complex (with tests)

Compare: **Goose vs Aider vs OpenHands**

---

## 9. Final Architecture

### 9.1 High-Level System Design

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           VishkarV2 Architecture                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                       Web UI (Next.js 15)                                │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────────────┐  │   │
│  │  │   Project    │ │   Story      │ │   17-Step SDLC Workflow        │  │   │
│  │  │   Selector   │ │   Board      │ │   with Compliance Monitor      │  │   │
│  │  │              │ │              │ │                                │  │   │
│  │  │ [API Key]    │ │ To Do: 5     │ │ [1] Select ✓  [10] Test ○     │  │   │
│  │  │ [Connect]    │ │ In Prog: 1   │ │ [2] Impl   ●  [11] Gate ○     │  │   │
│  │  │              │ │ Done: 12     │ │ [3-6] Review  [16] Human ⚠️    │  │   │
│  │  └──────────────┘ └──────────────┘ └────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      VishkarV2 API (FastAPI)                            │   │
│  │  • Project Management    • Workflow Triggers    • WebSocket Events     │   │
│  │  • SDLC Compliance       • Step Enforcement     • Lessons Learned      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      Temporal.io (Durable Execution)                    │   │
│  │  • 17-Step Workflow      • State Persistence    • Retry Logic          │   │
│  │  • Quality Gates         • Human Approval       • Monitoring           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│         ┌─────────────────────────────┼─────────────────────────────┐          │
│         ▼                             ▼                             ▼          │
│  ┌─────────────────┐       ┌─────────────────────┐       ┌─────────────────┐  │
│  │    LangGraph    │       │  Execution Engine   │       │     MCPs        │  │
│  │     Agents      │       │   (Pluggable)       │       │                 │  │
│  │                 │       │                     │       │ • Project Reg   │  │
│  │ • 4-Angle       │       │ • Goose (primary)   │       │ • Enhanced Ctx  │  │
│  │   Review        │       │ • Aider (fallback)  │       │ • JIRA          │  │
│  │ • Planning      │       │ • OpenHands (scale) │       │ • Confluence    │  │
│  └─────────────────┘       └─────────────────────┘       └─────────────────┘  │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                 User's Local Machine (via Goose)                        │   │
│  │  • Repository Access    • Git Operations    • Test Execution            │   │
│  │  • Multi-repo Support   • Codebase Context  • Build & Lint              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 SDLC Enforcement (Key Innovation)

Based on Cincara-Context learnings, VishkarV2 will **enforce SDLC compliance**:

```
┌──────────────────────────────────────────────────────────────────┐
│                    SDLC Enforcement Engine                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   BEFORE allowing Step N+1, verify Step N is complete:           │
│                                                                  │
│   Step 1: Task Selection                                         │
│       ├── ✓ JIRA ticket exists                                   │
│       └── ✓ Transitioned to "In Progress"                        │
│                                                                  │
│   Step 2: Implementation                                         │
│       ├── ✓ Codebase context loaded                              │
│       ├── ✓ Execution engine invoked                             │
│       └── ✓ Files changed recorded                               │
│                                                                  │
│   Steps 3-6: 4-Angle Review                                      │
│       ├── ✓ Architecture review completed                        │
│       ├── ✓ Security review completed                            │
│       ├── ✓ Code quality review completed                        │
│       ├── ✓ Tech-stack review completed                          │
│       └── ✓ Findings stored in .reviews/                         │
│                                                                  │
│   Quality Gate: 0 Critical, 0 High                               │
│       └── ✗ BLOCKED if violations exist                          │
│                                                                  │
│   Steps 7-11: Testing & Feedback                                 │
│       ├── ✓ Tests created/updated                                │
│       ├── ✓ Tests pass (≥90%)                                    │
│       └── ✓ Coverage meets threshold                             │
│                                                                  │
│   Steps 12-15: PR & CI/CD                                        │
│       ├── ✓ PR created                                           │
│       ├── ✓ PR-Agent review completed                            │
│       ├── ✓ Feedback implemented                                 │
│       └── ✓ CI/CD green                                          │
│                                                                  │
│   Step 16: Human Approval (MANDATORY)                            │
│       └── ✓ Human explicitly approves                            │
│                                                                  │
│   Step 17: Story Closure                                         │
│       ├── ✓ Worklog added                                        │
│       ├── ✓ JIRA transitioned to "Done"                          │
│       └── ✓ Lessons learned stored                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 10. Phased Implementation Plan (Final)

### Phase 0: POC - Execution Engine Comparison
**Goal:** Select best execution engine for VishkarV2
**Duration:** 1-2 weeks

| Task | Description |
|------|-------------|
| Set up Goose locally | Install, configure, test basic usage |
| Set up Aider locally | Install, configure, test basic usage |
| Set up OpenHands | Docker setup, test basic usage |
| Test: Simple task | Single file change with each engine |
| Test: Medium task | Multi-file feature with each engine |
| Test: Complex task | Feature with tests with each engine |
| Evaluate | Compare speed, quality, reliability, MCP compat |
| **Decision** | Select primary engine (likely Goose) |

### Phase 1: Foundation
**Goal:** VishkarV2 repo structure + Temporal + Codebase Understanding

| Task | Description |
|------|-------------|
| Create VishkarV2 repo | Next.js 15 + FastAPI structure |
| Set up Temporal.io | Docker Compose for local dev |
| Implement codebase analysis | Repomix-based, VISHKAR schema |
| Multi-repo schema | Design for future multi-repo support |
| Project Registry integration | Connect via API key |
| Basic API endpoints | Projects, workflows |

### Phase 2: JIRA Integration & Story Board
**Goal:** Connect to JIRA, display stories, enable selection

| Task | Description |
|------|-------------|
| JIRA MCP integration | Search, get details, transitions |
| Story board UI | Kanban view (To Do / In Progress / Done) |
| Story detail view | Show description, acceptance criteria |
| Story selection | Pick story for implementation |
| Worklog tracking | Log time on completion |

### Phase 3: Execution Engine Integration
**Goal:** Connect selected engine, enable local execution

| Task | Description |
|------|-------------|
| Integrate primary engine | Goose (or winner from POC) |
| File operations | Read, write, edit via local agent |
| Git operations | Branch, commit, push |
| Test execution | Run tests, capture results |
| Build/lint | Run project build and linting |

### Phase 4: 17-Step Workflow
**Goal:** Full SDLC workflow with enforcement

| Task | Description |
|------|-------------|
| Temporal workflow | Define 17-step workflow |
| Step enforcement | Block progression on incomplete steps |
| LangGraph integration | 4-Angle review agents |
| Quality gates | Enforce 0 Critical/High |
| Human approval gate | Step 16 mandatory approval |

### Phase 5: Monitoring & Compliance
**Goal:** Dashboards, alerts, lessons learned

| Task | Description |
|------|-------------|
| Progress dashboard | Real-time step completion |
| Compliance alerts | Notify on skipped steps |
| Lessons learned | Store and retrieve patterns |
| Analytics | Track success rates, common issues |

---

## 11. Known Issues & Workarounds

### MCP Timeout Bug (Critical)
**Problem:** Claude Code has hardcoded ~10-15s timeout for HTTP MCPs, ignoring `MCP_TIMEOUT` env var.
**Impact:** JIRA, Confluence, and other slow MCPs timeout before completing.
**Workaround:** Use `curl` commands for slow MCP operations:

```bash
# Example: Search JIRA issues via curl
curl -X POST https://jira-mcp-pi.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -H "X-API-Key: pk_wo1F6KQEYNFQBPdmjlsKSlR_EVcn-EBSgAkJV7srKf4" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_issues","arguments":{"jql":"project = V1","maxResults":50}},"id":1}'
```

**VishkarV2 Solution:** Backend API will proxy MCP calls with proper timeout handling.

---

## 12. Key Files to Reference

| Purpose | Path |
|---------|------|
| Current orchestration | `/Users/premkalyan/code/VISHKAR/langgraph-demo/workflow_parallel.py` |
| Agent definitions | `/Users/premkalyan/code/VISHKAR/langgraph-demo/agents.py` |
| State management | `/Users/premkalyan/code/VISHKAR/langgraph-demo/state.py` |
| MCP integration | `/Users/premkalyan/code/VISHKAR/vishkar/docs/mcp-integration/` |
| 13-step SDLC spec | `/Users/premkalyan/code/VISHKAR/vishkar/docs/sdlc-agents/` |
| VishkarV2 spec | `/Users/premkalyan/code/VishkarV2/VISHKAR_FRAMEWORK_SPEC.md` |

---

## 11. Research Sources

### Execution Engines
- [Goose (Block)](https://github.com/block/goose) - MCP-based, 5000 Block employees
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) - Full autonomous agent
- [Aider](https://aider.chat/) - Git-aware AI pair programming
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) - 21 agents, story-driven

### Codebase Understanding
- [Repomix](https://repomix.com/) - Repo packing for LLMs
- [lsp-mcp](https://github.com/jonrad/lsp-mcp) - LSP to MCP bridge
- [Qodo Context Engine](https://www.qodo.ai/blog/introducing-qodo-aware-deep-codebase-intelligence-for-enterprise-development/) - Enterprise RAG

### Temporal.io
- [Temporal for AI](https://temporal.io/solutions/ai)
- [Replit uses Temporal](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal)
- [OpenAI Agents SDK + Temporal](https://temporal.io/blog/announcing-openai-agents-sdk-integration)

### Local Agent Options
- [E2B Sandbox](https://www.koyeb.com/blog/top-sandbox-code-execution-platforms-for-ai-code-execution-2025)
- [AgentSphere](https://dev.to/agentsphere/why-ai-agents-need-a-new-infrastructure-layer-a-deep-dive-into-2025s-ai-native-sandbox-platforms-5gda)

---

## 14. Next Steps (Ready for Approval)

### Immediate (Phase 0: POC)
1. **Set up execution engine POC environment**
   - Install Goose, Aider, OpenHands locally
   - Test with simple/medium/complex tasks
   - Document findings and select winner

2. **Use curl for MCP operations** until timeout issue resolved
   - JIRA queries, Confluence updates
   - VishkarV2 backend will proxy these

### After POC Approval
3. **Initialize VishkarV2 repository**
   - Next.js 15 + FastAPI structure
   - Temporal.io Docker Compose
   - PostgreSQL + Prisma setup

4. **Implement core features in phases**
   - Follow Phase 1-5 plan above

---

## Summary

**VishkarV2** is a continuation of VISHKAR, adding:
- **17-Step SDLC enforcement** with step blocking
- **Temporal.io** for durable, scalable workflows
- **Pluggable execution engines** (Goose primary)
- **Multi-repo codebase understanding** from day 1
- **Real-time compliance monitoring** to prevent skipped steps

**Key Innovation:** Learn from Cincara-Context gaps - VishkarV2 will **automatically enforce** SDLC compliance, not rely on LLM discipline.

**Ready for approval to begin Phase 0 POC.**
