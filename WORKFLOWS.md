# Workflow System - Concepts & Design

## Overview

The Agentic AI workflow system enables complex multi-agent projects with:
- **Phase-based execution** (Planning → Review → Execution → Validation → Complete)
- **Dependency management** (steps can depend on other steps)
- **Agent specialization** (Frontend/Backend/Orchestrator agents)
- **Parallel execution** (independent tasks run concurrently)
- **Audit trail** (all workflows saved for review)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Manager                         │
│                                                             │
│  - Maintains workflow state                               │
│  - Coordinates agent execution                            │
│  - Tracks metrics and history                             │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┴────────┐
       ↓                ↓
  ┌─────────┐      ┌──────────┐
  │ Workflow │      │ Workflow │
  │  Plan 1  │      │  Plan 2  │
  └────┬────┘      └────┬─────┘
       │                 │
   ┌───┴────┐        ┌───┴────┐
   ↓        ↓        ↓        ↓
 Step 1   Step 2   Step 3   Step 4
 (FE)     (BE)     (BE)     (Orch)
```

---

## Workflow Phases

### 1. Planning
- Workflow is created and stored
- Steps are defined with descriptions and dependencies
- Estimated execution time is calculated
- Plan is saved as JSON for review

### 2. Review
- Human review of the generated plan
- Optional: modify steps or dependencies
- Edit the JSON file directly if needed
- Confirm before execution

### 3. Execution
- Agents execute steps in order
- Dependencies are respected
- Independent steps run in parallel
- Real-time status updates

### 4. Validation
- Results are verified
- Errors are caught and logged
- Failed tasks are marked

### 5. Complete
- Workflow finishes
- Metrics are recorded
- Results are saved for audit

---

## Step Definition

Each step in a workflow has:

```python
WorkflowStep(
    step_id="unique-id",              # Unique identifier
    description="Human readable",      # What this step does
    agent_type="frontend|backend|orchestrator",  # Which agent
    task_query="What to do",          # What to execute
    dependencies=["step1", "step2"],  # Required previous steps
    estimated_time=300,               # Seconds
)
```

### Example: Build E-Commerce Site

```python
steps = [
    WorkflowStep(
        step_id="fe-design",
        description="Design product catalog UI",
        agent_type="frontend",
        task_query="Create responsive product catalog with filters",
    ),
    WorkflowStep(
        step_id="be-design",
        description="Design product API",
        agent_type="backend",
        task_query="Create REST API for products with filtering",
    ),
    WorkflowStep(
        step_id="fe-payment",
        description="Implement payment UI",
        agent_type="frontend",
        task_query="Create checkout and payment UI",
        dependencies=["fe-design"],
    ),
    WorkflowStep(
        step_id="be-payment",
        description="Integrate payment processor",
        agent_type="backend",
        task_query="Implement payment processing with Stripe",
        dependencies=["be-design"],
    ),
    WorkflowStep(
        step_id="orchestrate",
        description="Coordinate and integrate all components",
        agent_type="orchestrator",
        task_query="Ensure all components work together",
        dependencies=["fe-payment", "be-payment"],
    ),
]
```

---

## Execution Flow

### Sequential Execution (with dependencies)

```
Step 1: Frontend Design
   ↓
Step 2: Backend Design
   ↓
Step 3a: Payment UI  ←─┐
Step 3b: Payment API ←─┤ (parallel if independent)
   ↓                   ↓
Step 4: Orchestration
```

### Parallel Execution (when independent)

```
Frontend Design ─┐
                 ├→ Orchestration
Backend Design ──┤
                 ├→ Validation
Payment UI ──────┘
```

---

## Best Practices

### 1. Keep Steps Focused
- One clear responsibility per step
- Clear task query
- Realistic estimated time

### 2. Define Dependencies Correctly
- Only depend on truly required steps
- Too many dependencies = slow execution
- Too few = unclear dependencies

### 3. Use Meaningful IDs
```
✓ Good:  "fe-design", "be-auth", "payment-integration"
✗ Bad:   "step1", "s2", "xyz"
```

### 4. Realistic Estimation
```
Frontend Design:     300-600s
Backend Design:      300-600s
Integration:         180-300s
Testing:             150-300s
Deployment:          60-180s
```

### 5. Clear Descriptions
```
✓ "Create user authentication system with JWT"
✗ "Do auth"

✓ "Design responsive product catalog with search and filters"
✗ "Frontend"
```

---

## Workflow Patterns

### Pattern 1: Sequential (Waterfall)
All steps depend on previous step.
```
Plan → Frontend → Backend → Orchestrate → Complete
```
**When to use:** Simple projects, strict order required

### Pattern 2: Parallel (Agile)
Independent work in parallel, then integrate.
```
Frontend ─┐
          └→ Integration → Complete
Backend ──┘
```
**When to use:** Large teams, complex projects

### Pattern 3: Phased Release
Groups of features, released in phases.
```
Phase 1: Core Features
  ├─ Frontend
  └─ Backend
     ↓
Phase 2: Advanced Features
  ├─ Advanced Frontend
  └─ Advanced Backend
     ↓
Phase 3: DevOps & Deployment
  └─ Production Setup
```
**When to use:** MVP → Feature releases

### Pattern 4: A/B Testing
Multiple parallel implementations
```
Implementation A ─┐
                  ├→ Evaluation → Deploy Winner
Implementation B ─┘
```
**When to use:** Experimental features

---

## Advanced Concepts

### Conditional Execution
Workflows can branch based on results:
```python
if frontend_result.status == "completed":
    orchestrator_step.dependencies.append("fe-design")
```

### Error Handling
Failed steps don't block dependent steps:
```
Step 1: Frontend ─(fail)─→ Continues with degraded state
Step 2: Backend ─(success)
Step 3: Integration ─ Handles both states
```

### Retry Logic
Failed steps can be retried:
```python
# Retry failed step
step.status = "pending"
await workflow_manager.execute_plan(plan)
```

### Performance Optimization
```python
# Skip completed steps
completed_steps = [s for s in plan.steps if s.status == "completed"]
pending_steps = [s for s in plan.steps if s.status != "completed"]
```

---

## Workflow Storage

Workflows are persisted in `.workflows/` directory:

```
.workflows/
├── e-commerce-1710723600.json
├── social-media-1710723601.json
├── payment-api-1710723602.json
└── kanban-app-1710723603.json
```

Each file contains complete workflow state:
- All steps with status
- Execution results
- Timestamps
- Metrics

---

## Metrics & Monitoring

### Execution Metrics
```python
summary = workflow_manager.get_workflow_summary(workflow_id)
# Returns:
# {
#   "workflow_id": str,
#   "project_name": str,
#   "phase": str,
#   "total_steps": int,
#   "completed_steps": int,
#   "failed_steps": int,
#   "estimated_total_time": int
# }
```

### Performance Analysis
- Track execution time per step
- Identify bottlenecks
- Optimize future workflows
- Build metrics database

### Audit Trail
Every workflow execution is logged:
- What steps executed
- Which agents executed them
- Execution timings
- Success/failure status
- Timestamps

---

## Integration Examples

### With Git
```bash
# Commit workflow plan to repo
git add .workflows/
git commit -m "feat: workflow for user auth"

# Track workflow changes
git log -- .workflows/
```

### With CI/CD
```yaml
# .github/workflows/build.yml
- name: Execute Agentic Workflow
  run: python3 agentic workflow:execute "my-project"
```

### With Docker
```dockerfile
FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "agentic", "workflow:execute", "production"]
```

---

## Troubleshooting

### Step Execution Fails
1. Check agent availability
2. Verify task query is clear
3. Check logs for specific error
4. Retry with `workflow:status`

### Dependencies Not Resolving
1. Verify dependency IDs exist
2. Check for circular dependencies
3. Review workflow structure
4. Test with simpler workflow first

### Performance Issues
1. Reduce parallel steps
2. Increase estimated times
3. Profile agent execution
4. Check system resources

---

## See Also
- [COMMANDS.md](COMMANDS.md) - Command reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [ADVANCED.md](ADVANCED.md) - Advanced techniques
