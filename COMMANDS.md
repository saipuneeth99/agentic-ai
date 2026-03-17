# Agentic AI - Commands Reference

## Quick Start

```bash
# Show all available commands
python3 agentic help

# Plan a workflow
python3 agentic workflow:plan "my-project" "Build a web application"

# Execute a workflow
python3 agentic workflow:execute "my-project-123456"

# Check workflow status
python3 agentic workflow:status
```

## Workflow Commands

### workflow:plan
Generate a multi-phase workflow plan for your project.

**Syntax:**
```bash
python3 agentic workflow:plan <project_name> <description>
```

**Example:**
```bash
python3 agentic workflow:plan "e-commerce" "Build modern e-commerce platform with payment integration"
```

**Output:**
- Generates a `.json` workflow file in `.workflows/` directory
- Contains frontend, backend, and orchestration phases
- Shows estimated execution time

**Output Example:**
```
✓ Workflow plan generated
  Project: e-commerce
  Steps: 3
  Estimated Time: 900s
  Saved: .workflows/e-commerce-1710723600.json
```

---

### workflow:execute
Execute a previously generated workflow plan.

**Syntax:**
```bash
python3 agentic workflow:execute <workflow_id_or_file>
```

**Usage Modes:**
```bash
# Execute by workflow ID
python3 agentic workflow:execute "e-commerce"

# Execute by file path
python3 agentic workflow:execute ".workflows/e-commerce-1710723600.json"
```

**Execution Phases:**
1. **Planning Phase** — Understanding requirements
2. **Review Phase** — Validation of plan
3. **Execution Phase** — Agents execute tasks
4. **Validation Phase** — Result verification
5. **Complete** — Workflow finished

**Output Example:**
```
✓ Workflow execution complete
  Execution Time: 2.34s
  Phase: complete
  Results: 3 tasks
```

---

### workflow:status
Display current workflow status and metrics.

**Syntax:**
```bash
python3 agentic workflow:status
```

**Output:**
Shows all active workflows with:
- Current phase
- Progress (completed tasks / total)
- Failed tasks count
- Estimated total time

**Example Output:**
```
======================================================================
WORKFLOW STATUS & METRICS
======================================================================

e-commerce (e-commerce-1710723600)
  Phase: complete
  Progress: 3/3
  Failed: 0
  Est. Time: 900s

my-project (my-project-1710723601)
  Phase: execution
  Progress: 1/3
  Failed: 0
  Est. Time: 600s

======================================================================
```

---

## Utility Commands

### help
Display all available commands with descriptions.

**Syntax:**
```bash
python3 agentic help
```

---

## Workflow File Format

Workflow plans are saved as JSON files with the following structure:

```json
{
  "workflow_id": "e-commerce-1710723600",
  "project_name": "e-commerce",
  "description": "Build modern e-commerce platform",
  "phase": "planning",
  "created_at": "2026-03-18T00:20:56",
  "estimated_total_time": 900,
  "steps": [
    {
      "step_id": "frontend-design",
      "description": "Design UI/UX for the project",
      "agent_type": "frontend",
      "task_query": "Design frontend for e-commerce",
      "dependencies": [],
      "estimated_time": 300,
      "status": "pending",
      "created_at": "2026-03-18T00:20:56"
    },
    {
      "step_id": "backend-design",
      "description": "Design backend architecture and APIs",
      "agent_type": "backend",
      "task_query": "Design backend architecture for e-commerce",
      "dependencies": [],
      "estimated_time": 300,
      "status": "pending",
      "created_at": "2026-03-18T00:20:56"
    },
    {
      "step_id": "orchestration",
      "description": "Coordinate all components",
      "agent_type": "orchestrator",
      "task_query": "Orchestrate integration for e-commerce",
      "dependencies": ["frontend-design", "backend-design"],
      "estimated_time": 300,
      "status": "pending",
      "created_at": "2026-03-18T00:20:56"
    }
  ]
}
```

---

## Real-World Examples

### Example 1: Web Application

```bash
# 1. Plan the workflow
python3 agentic workflow:plan "social-media" "Build social media platform"

# 2. Execute the plan
python3 agentic workflow:execute ".workflows/social-media-*.json"

# 3. Check status
python3 agentic workflow:status
```

### Example 2: API Service

```bash
# Plan API backend service
python3 agentic workflow:plan "payment-api" "RESTful payment processing API"

# Execute
python3 agentic workflow:execute "payment-api"
```

---

## Advanced Features

### Parallel Execution
Workflows automatically parallelize independent steps:
- Frontend and backend steps run in parallel
- Orchestration step waits for dependencies

### Status Tracking
Full execution metrics:
- Task completion status
- Execution time per step
- Error tracking and logging
- Full audit trail in `.workflows/` directory

### Plan Review
Generated plans are human-readable JSON files:
```bash
# View the plan before executing
cat .workflows/e-commerce-*.json
```

---

## Troubleshooting

### Command Not Found
```bash
✓ Make sure you're in the project directory
✓ Run: python3 -m src.cli.commands help
```

### Workflow Not Found
```bash
# List all workflows
ls -la .workflows/

# Use full path if needed
python3 agentic workflow:execute ".workflows/my-workflow-123.json"
```

### Execution Fails
```bash
# Check logs
tail -f logs/agentic.log

# Check agent availability
python3 agentic workflow:status
```

---

## Best Practices

1. **Plan Before Execute** — Always generate plan before execution
2. **Review Plans** — Check generated JSON files for accuracy
3. **Monitor Status** — Use `workflow:status` frequently
4. **Archive Results** — Save workflow files for audit trail
5. **Handle Errors** — Check logs when steps fail

---

## Integration

### With Existing Tools
Workflows work seamlessly with:
- Git version control
- MCP (Model Context Protocol)
- CI/CD pipelines
- Docker containers

### As Library
```python
from src.cli.commands import CLIInterface

cli = CLIInterface()
await cli.run("workflow:plan", ["my-project", "Description"])
```

---

## Environment Variables

Control workflow behavior via environment:

```bash
# Logging level
LOG_LEVEL=DEBUG python3 agentic workflow:execute "my-project"

# Timeout settings
WORKFLOW_TIMEOUT=3600 python3 agentic workflow:execute "my-project"

# Output format
OUTPUT_FORMAT=json python3 agentic workflow:execute "my-project"
```

---

For more details, see:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [WORKFLOWS.md](WORKFLOWS.md) - Workflow concepts
- [ADVANCED.md](ADVANCED.md) - Advanced usage
