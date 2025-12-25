# Temporal.io Research

**Last Updated:** 2025-12-25
**Status:** Research Complete

## Overview

Temporal.io provides durable execution for long-running workflows. VishkarV2 will use Temporal to orchestrate the 17-Step SDLC workflow with reliability at scale.

## Why Temporal for AI Agents

**Sources:**
- [Temporal for AI](https://temporal.io/solutions/ai)
- [Durable Execution for AI](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai)

### Key Finding

[Replit uses Temporal](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal) for their AI coding assistant at massive scale.

## Benefits for VishkarV2

| Feature | Benefit |
|---------|---------|
| **Durable Execution** | Workflows survive server restarts, network failures |
| **State Persistence** | Multi-day implementation cycles with checkpoints |
| **Automatic Retries** | Handle LLM API failures gracefully |
| **Human Intervention** | Pause/resume for approval gates |
| **Schedules** | Ambient agents running on schedules |
| **Non-deterministic LLMs** | Deterministic workflow with non-deterministic decisions |

## Architecture Pattern

```
Temporal Workflow (durable, long-running)
    │
    ├── Activity: select_task
    │       └── JIRA MCP → Get next story
    │
    ├── Activity: execute_implementation
    │       └── Execution Engine (Goose/Aider) → Write code
    │
    ├── Activities: 4-Angle Review (parallel)
    │       ├── architecture_review → LangGraph agents
    │       ├── security_review → LangGraph agents
    │       ├── quality_review → LangGraph agents
    │       └── techstack_review → LangGraph agents
    │
    ├── Activity: run_tests
    │       └── Local execution → pytest/jest
    │
    ├── Activity: create_pr
    │       └── GitHub API → Create PR
    │
    ├── Signal: human_approval (BLOCKING)
    │       └── Wait for human approval
    │
    └── Activity: close_story
            └── JIRA MCP → Transition to Done
```

## Temporal + LangGraph Integration

**Pattern:** Temporal orchestrates the 17-step workflow, LangGraph orchestrates agent discussions within steps.

```python
# Temporal Activity calling LangGraph
@activity.defn
async def architecture_review(impl_result: ImplementationResult) -> ReviewFindings:
    # LangGraph handles the multi-agent discussion
    graph = create_review_graph()
    result = await graph.invoke({
        "files_changed": impl_result.files,
        "review_type": "architecture"
    })
    return ReviewFindings.from_langgraph(result)
```

## 17-Step Workflow Design

```python
@workflow.defn
class SDLCWorkflow:
    def __init__(self):
        self.human_approved = False

    @workflow.signal
    def approve(self):
        self.human_approved = True

    @workflow.run
    async def run(self, task: TaskInput) -> TaskOutput:
        # Step 1: Task Selection
        await workflow.execute_activity(
            select_task, task,
            start_to_close_timeout=timedelta(minutes=5)
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

        # Quality Gate
        if has_blocking_issues(reviews):
            await workflow.execute_activity(fix_issues, reviews)
            # Loop back to review...

        # Steps 8-11: Testing
        test_result = await workflow.execute_activity(
            run_tests, impl_result,
            start_to_close_timeout=timedelta(minutes=30)
        )

        # Step 12: PR Creation
        pr = await workflow.execute_activity(create_pr, impl_result)

        # Step 16: Human Approval (BLOCKING)
        await workflow.wait_condition(
            lambda: self.human_approved,
            timeout=timedelta(days=7)
        )

        # Step 17: Story Closure
        await workflow.execute_activity(close_story, task, pr)

        return TaskOutput(success=True, pr_url=pr.url)
```

## Deployment Options

### Local Development

```yaml
# docker-compose.yml
version: '3.8'
services:
  temporal:
    image: temporalio/auto-setup:latest
    ports:
      - "7233:7233"  # gRPC
      - "8233:8233"  # Web UI
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: temporal
      POSTGRES_PASSWORD: temporal
    volumes:
      - temporal-data:/var/lib/postgresql/data

volumes:
  temporal-data:
```

### Production

Options:
1. **Temporal Cloud** - Managed service
2. **Self-hosted on K8s** - Helm charts available
3. **AWS/GCP managed** - Via marketplaces

## Python SDK

```bash
pip install temporalio
```

```python
from temporalio.client import Client
from temporalio.worker import Worker

# Connect to Temporal
client = await Client.connect("localhost:7233")

# Start workflow
handle = await client.start_workflow(
    SDLCWorkflow.run,
    TaskInput(jira_key="V2-10"),
    id=f"sdlc-{jira_key}",
    task_queue="vishkar-sdlc"
)

# Run worker
worker = Worker(
    client,
    task_queue="vishkar-sdlc",
    workflows=[SDLCWorkflow],
    activities=[
        select_task,
        execute_implementation,
        architecture_review,
        # ...
    ]
)
await worker.run()
```

## Key Concepts

### Workflows vs Activities

| Concept | Purpose | Example |
|---------|---------|---------|
| **Workflow** | Durable orchestration logic | 17-Step SDLC |
| **Activity** | Individual units of work | Call JIRA API, Run tests |
| **Signal** | External input to workflow | Human approval |
| **Query** | Read workflow state | Get current step |

### Retry Policies

```python
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=5),
    maximum_attempts=5,
    non_retryable_error_types=["ValidationError"]
)
```

### Timeouts

```python
await workflow.execute_activity(
    my_activity,
    start_to_close_timeout=timedelta(hours=1),  # Max execution time
    schedule_to_start_timeout=timedelta(minutes=5),  # Max queue wait
    heartbeat_timeout=timedelta(seconds=30)  # For long activities
)
```

## Related Documents

- [Architecture Plan](../ARCHITECTURE_PLAN.md)
- [Execution Engines](./execution-engines.md)
