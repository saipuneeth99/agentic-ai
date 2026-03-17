# Advanced Techniques & Patterns

## Table of Contents
1. [Custom Agents](#custom-agents)
2. [Workflow Customization](#workflow-customization)
3. [Performance Optimization](#performance-optimization)
4. [Error Recovery](#error-recovery)
5. [Multi-Workflow Coordination](#multi-workflow-coordination)
6. [Integration Patterns](#integration-patterns)

---

## Custom Agents

### Creating a Specialized Agent

Extend the `BaseAgent` class for domain-specific tasks:

```python
from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
import time

class DataAnalysisAgent(BaseAgent):
    """Specialized agent for data analysis tasks"""
    
    def __init__(self, name: str = "Data Analyst", model: str = "gpt-4"):
        super().__init__(
            name=name,
            role="analytics",
            model=model,
            description="Specialized in data analysis and insights",
            system_prompt="""You are an expert data analyst with expertise in:
            - Statistical analysis
            - Data visualization
            - Business intelligence
            - Predictive modeling"""
        )
    
    async def execute(self, task: TaskInput) -> TaskResult:
        """Execute data analysis task"""
        start_time = time.time()
        try:
            # Your analysis logic here
            result_data = await self.analyze_data(task.query)
            
            return TaskResult(
                agent_name=self.name,
                task_type="data_analysis",
                status="completed",
                result={"analysis": result_data},
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            return TaskResult(
                agent_name=self.name,
                task_type="data_analysis",
                status="failed",
                error=str(e),
                execution_time=time.time() - start_time,
            )
    
    async def analyze_data(self, query: str):
        """Implement your analysis logic"""
        # Your implementation
        pass

# Register and use
from src.framework.agent_factory import AgentFactory

agent = DataAnalysisAgent()
task = TaskInput(query="Analyze sales trends for Q1")
result = await agent.execute(task)
```

### Register in AgentFactory

Update `src/framework/agent_factory.py`:

```python
class AgentFactory:
    @classmethod
    def create_agent(cls, agent_type: str, name: str, model: str, ...):
        if agent_type == "analytics":
            agent = DataAnalysisAgent(name=name, model=model)
        # ... other types
        
        cls._agents[name] = agent
        return agent
```

---

## Workflow Customization

### Dynamic Workflow Generation

Generate workflows based on input requirements:

```python
from src.framework.workflow import WorkflowManager, WorkflowStep
from datetime import datetime

class DynamicWorkflowBuilder:
    """Build workflows from requirements"""
    
    def build_from_requirements(self, requirements: dict):
        """Convert requirements to workflow steps"""
        steps = []
        
        # Generate frontend step if needed
        if requirements.get("needs_ui"):
            steps.append(WorkflowStep(
                step_id="frontend",
                description=requirements.get("ui_description", "Design UI"),
                agent_type="frontend",
                task_query=requirements.get("ui_query", "Design user interface"),
            ))
        
        # Generate backend step if needed
        if requirements.get("needs_api"):
            steps.append(WorkflowStep(
                step_id="backend",
                description=requirements.get("api_description", "Design API"),
                agent_type="backend",
                task_query=requirements.get("api_query", "Design API"),
                dependencies=["frontend"] if requirements.get("needs_ui") else [],
            ))
        
        return steps

# Usage
builder = DynamicWorkflowBuilder()
requirements = {
    "needs_ui": True,
    "needs_api": True,
    "ui_description": "Design modern dashboard",
    "api_query": "Create analytics API",
}

steps = builder.build_from_requirements(requirements)
workflow = workflow_manager.create_plan("dashboard", "Modern dashboard app", steps)
```

### Workflow Templates

Reusable workflow templates:

```python
class WorkflowTemplates:
    """Pre-built workflow templates"""
    
    @staticmethod
    def web_app_template(app_name: str):
        """Template for web applications"""
        return [
            WorkflowStep(
                step_id="design",
                description="Design UI/UX",
                agent_type="frontend",
                task_query=f"Design UI for {app_name}",
            ),
            WorkflowStep(
                step_id="api",
                description="Design API",
                agent_type="backend",
                task_query=f"Design API for {app_name}",
            ),
            WorkflowStep(
                step_id="integrate",
                description="Integration",
                agent_type="orchestrator",
                task_query=f"Integrate all components for {app_name}",
                dependencies=["design", "api"],
            ),
        ]
    
    @staticmethod
    def microservices_template(service_name: str):
        """Template for microservices"""
        return [
            WorkflowStep(
                step_id="spec",
                description="API Specification",
                agent_type="backend",
                task_query=f"Create API spec for {service_name}",
            ),
            # ... more steps
        ]

# Usage
steps = WorkflowTemplates.web_app_template("MyApp")
workflow = workflow_manager.create_plan("MyApp", "Web application", steps)
```

---

## Performance Optimization

### Parallel Execution Strategy

```python
class PerformanceOptimizer:
    """Optimize workflow execution performance"""
    
    @staticmethod
    def analyze_dependencies(steps: list) -> dict:
        """Analyze which steps can run in parallel"""
        parallelizable = []
        sequential = []
        
        # Group steps by dependencies
        for step in steps:
            if not step.dependencies:
                parallelizable.append(step)
            else:
                sequential.append(step)
        
        return {
            "parallel": parallelizable,
            "sequential": sequential,
            "parallelization_factor": len(parallelizable) / len(steps),
        }
    
    @staticmethod
    def optimize_execution_order(steps: list) -> list:
        """Reorder steps for optimal execution"""
        # Topological sort for dependency graph
        sorted_steps = []
        remaining = set(steps)
        
        while remaining:
            # Find steps with satisfied dependencies
            ready = [
                s for s in remaining
                if all(dep not in [x.step_id for x in remaining] for dep in s.dependencies)
            ]
            sorted_steps.extend(ready)
            remaining -= set(ready)
        
        return sorted_steps

# Usage
optimizer = PerformanceOptimizer()
metrics = optimizer.analyze_dependencies(workflow.steps)
print(f"Parallelization factor: {metrics['parallelization_factor']:.2%}")

optimized = optimizer.optimize_execution_order(workflow.steps)
```

### Caching Results

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

class WorkflowCache:
    """Cache workflow results for reuse"""
    
    def __init__(self, cache_dir: str = ".cache/workflows"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, workflow_id: str, step_id: str) -> str:
        """Generate cache key"""
        return f"{workflow_id}:{step_id}"
    
    def save_result(self, key: str, result: dict, ttl_hours: int = 24):
        """Save result with TTL"""
        data = {
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "ttl_hours": ttl_hours,
        }
        
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, "w") as f:
            json.dump(data, f)
    
    def get_result(self, key: str) -> dict:
        """Retrieve cached result if valid"""
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, "r") as f:
            data = json.load(f)
        
        # Check TTL
        cached_time = datetime.fromisoformat(data["timestamp"])
        if datetime.now() - cached_time > timedelta(hours=data["ttl_hours"]):
            cache_file.unlink()  # Delete expired
            return None
        
        return data["result"]

# Usage
cache = WorkflowCache()
result = cache.get_result("workflow-123:frontend-design")
if result:
    print("Using cached result")
else:
    result = await agent.execute(task)
    cache.save_result("workflow-123:frontend-design", result.result)
```

---

## Error Recovery

### Automatic Retry with Backoff

```python
import asyncio
from typing import Callable

class RetryStrategy:
    """Retry failed tasks with exponential backoff"""
    
    def __init__(self, max_retries: int = 3, base_delay: int = 1):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ):
        """Execute function with retries"""
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                
                delay = self.base_delay * (2 ** attempt)
                print(f"Retry after {delay}s - Attempt {attempt + 1}/{self.max_retries}")
                await asyncio.sleep(delay)

# Usage
retry = RetryStrategy(max_retries=3, base_delay=2)

async def execute_step_with_retry(step, agent):
    return await retry.execute_with_retry(agent.execute, TaskInput(query=step.task_query))
```

### Partial Failure Handling

```python
class FailureRecovery:
    """Handle partial workflow failures"""
    
    async def resume_workflow(self, plan: WorkflowPlan):
        """Resume a workflow after partial failure"""
        # Skip completed steps
        completed = [s for s in plan.steps if s.status == "completed"]
        pending = [s for s in plan.steps if s.status in ("pending", "failed")]
        
        print(f"Resuming: {len(completed)} completed, {len(pending)} pending")
        
        # Re-execute pending steps
        for step in pending:
            # ... execute step
            pass
    
    def get_failure_summary(self, plan: WorkflowPlan) -> dict:
        """Get detailed failure information"""
        failed_steps = [s for s in plan.steps if s.status == "failed"]
        
        return {
            "failed_steps": len(failed_steps),
            "total_steps": len(plan.steps),
            "success_rate": 1 - len(failed_steps) / len(plan.steps),
            "failures": [
                {
                    "step_id": s.step_id,
                    "error": s.result.error if s.result else "Unknown",
                }
                for s in failed_steps
            ],
        }
```

---

## Multi-Workflow Coordination

### Workflow Chaining

```python
class WorkflowChain:
    """Chain multiple workflows together"""
    
    def __init__(self, name: str):
        self.name = name
        self.workflows = []
    
    def add_workflow(self, workflow_id: str, condition: Callable = None):
        """Add workflow to chain with optional condition"""
        self.workflows.append({
            "id": workflow_id,
            "condition": condition or (lambda x: True),
        })
    
    async def execute(self, workflow_manager):
        """Execute chain sequentially"""
        for workflow_meta in self.workflows:
            plan = workflow_manager.workflows[workflow_meta["id"]]
            
            if workflow_meta["condition"](plan):
                result = await workflow_manager.execute_plan(plan)
```

### Workflow Composition

```python
class CompositeWorkflow:
    """Compose multiple workflows"""
    
    def __init__(self, name: str):
        self.name = name
        self.sub_workflows = []
    
    async def execute_parallel(self, workflow_manager):
        """Execute sub-workflows in parallel"""
        tasks = [
            workflow_manager.execute_plan(wf)
            for wf in self.sub_workflows
        ]
        return await asyncio.gather(*tasks)
```

---

## Integration Patterns

### With Git Workflow

```python
class GitIntegration:
    """Integrate with Git"""
    
    @staticmethod
    def save_workflow_to_git(workflow: WorkflowPlan, branch: str):
        """Save workflow and create git commit"""
        workflow.save()
        
        # Git operations
        import subprocess
        subprocess.run(["git", "add", ".workflows/"])
        subprocess.run(["git", "commit", "-m", f"workflow: {workflow.workflow_id}"])
```

### With Monitoring

```python
class MonitoringIntegration:
    """Send metrics to monitoring system"""
    
    async def send_metrics(self, execution_record: dict):
        """Send to Datadog/New Relic/etc"""
        metrics = {
            "workflow_id": execution_record["workflow_id"],
            "execution_time": execution_record["execution_time"],
            "completed_steps": execution_record["completed_steps"],
            "total_steps": execution_record["total_steps"],
            "timestamp": execution_record["timestamp"],
        }
        
        # Send to monitoring service
        # await send_to_datadog(metrics)
```

### With Notification

```python
class NotificationIntegration:
    """Send notifications on workflow events"""
    
    async def notify_completion(self, workflow_id: str, status: str):
        """Send Slack/email notification"""
        message = f"Workflow {workflow_id} completed with status: {status}"
        
        # Send to Slack
        # await slack.send(message)
        
        # Send email
        # await email.send(message)
```

---

## Performance Benchmarks

Typical execution times:

```
Frontend Design:     150-300ms (mock)  | 5-15s (with LLM)
Backend Design:      150-300ms (mock)  | 5-15s (with LLM)
Integration:         100-200ms (mock)  | 2-5s (with LLM)

Full Workflow:       400-700ms (mock)  | 20-40s (with LLM)
```

---

See Also:
- [WORKFLOWS.md](WORKFLOWS.md) - Workflow concepts
- [COMMANDS.md](COMMANDS.md) - CLI reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
