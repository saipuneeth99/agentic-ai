# API Reference

## Core Classes

### BaseAgent

Base class for all agents.

#### Methods

##### `__init__(name, role, model, description, system_prompt=None)`
Initialize a base agent.

**Parameters:**
- `name` (str): Agent name
- `role` (str): Agent role
- `model` (str): LLM model to use
- `description` (str): Agent description
- `system_prompt` (str, optional): System prompt

##### `async execute(task: TaskInput) -> TaskResult`
Execute a task (abstract method).

##### `async run(query: str, context: Dict = None) -> TaskResult`
Run a task with query and optional context.

**Parameters:**
- `query` (str): Task query
- `context` (Dict, optional): Task context

**Returns:** `TaskResult`

##### `get_history() -> List[TaskResult]`
Get task execution history.

##### `clear_history() -> None`
Clear task history.

##### `get_summary() -> Dict`
Get agent summary with execution stats.

### TaskInput

Data model for task input.

**Attributes:**
- `query` (str): Task query
- `context` (Dict, optional): Task context
- `user_requirements` (Dict, optional): User requirements

### TaskResult

Data model for task result.

**Attributes:**
- `agent_name` (str): Name of executing agent
- `task_type` (str): Type of task
- `status` (str): Task status (pending, in_progress, completed, failed)
- `result` (Dict, optional): Task result data
- `error` (str, optional): Error message if failed
- `timestamp` (datetime): Execution timestamp
- `execution_time` (float, optional): Execution time in seconds

## Agent Classes

### FrontendAgent

Specialized agent for frontend development.

**Model:** Gemini Pro

**Inherits from:** BaseAgent

#### Methods

##### `async execute(task: TaskInput) -> TaskResult`
Execute frontend design task.

##### `get_capabilities() -> Dict`
Get frontend agent capabilities.

**Returns:**
```python
{
    "design_systems": ["Tailwind CSS", "Bootstrap", "Material Design"],
    "frameworks": ["React", "Vue", "Angular", "Svelte"],
    "languages": ["HTML5", "CSS3", "JavaScript", "TypeScript"],
    "specialties": [...]
}
```

### BackendAgent

Specialized agent for backend development.

**Model:** GPT-4

**Inherits from:** BaseAgent

#### Methods

##### `async execute(task: TaskInput) -> TaskResult`
Execute backend development task.

##### `get_capabilities() -> Dict`
Get backend agent capabilities.

**Returns:**
```python
{
    "languages": ["Python", "Node.js", "Go", "Java", "Rust"],
    "frameworks": ["FastAPI", "Django", "Express", ...],
    "databases": ["PostgreSQL", "MongoDB", "DynamoDB", ...],
    "specialties": [...]
}
```

### OrchestratorAgent

Specialized agent for orchestration and coordination.

**Model:** Claude 3 Opus

**Inherits from:** BaseAgent

#### Methods

##### `async execute(task: TaskInput) -> TaskResult`
Execute orchestration task.

##### `register_agent(agent_name: str, agent: Agent) -> None`
Register an agent for coordination.

##### `get_registered_agents() -> Dict[str, Agent]`
Get all registered agents.

##### `get_capabilities() -> Dict`
Get orchestrator capabilities.

## Factory Classes

### AgentFactory

Factory for creating and managing agents.

#### Class Methods

##### `create_agent(agent_type: str, name: str, model: str, config: Dict = None) -> BaseAgent`
Create an agent of specified type.

**Parameters:**
- `agent_type` (str): Type of agent (frontend, backend, orchestrator)
- `name` (str): Agent name
- `model` (str): LLM model
- `config` (Dict, optional): Configuration

**Returns:** `BaseAgent` instance

**Example:**
```python
agent = AgentFactory.create_agent(
    agent_type="frontend",
    name="frontend_dev",
    model="gemini-pro"
)
```

##### `get_agent(name: str) -> Optional[BaseAgent]`
Get agent by name.

##### `list_agents() -> Dict[str, BaseAgent]`
Get all registered agents.

##### `remove_agent(name: str) -> bool`
Remove an agent.

##### `clear_agents() -> None`
Clear all agents.

## Configuration

### Settings

**Location:** `src/config/settings.py`

**Attributes:**
- `google_api_key`: Google API key
- `openai_api_key`: OpenAI API key
- `anthropic_api_key`: Anthropic API key
- `agent_model_frontend`: Frontend agent model
- `agent_model_backend`: Backend agent model
- `agent_model_orchestrator`: Orchestrator agent model
- `log_level`: Logging level
- `log_file`: Log file path
- `environment`: Environment (development, production)
- `debug`: Debug mode flag

**Usage:**
```python
from src.config import settings

print(settings.google_api_key)
print(settings.log_level)
```

## Utilities

### Exceptions

**Location:** `src/utils/exceptions.py`

- `AgenticException`: Base exception
- `AgentExecutionError`: Agent execution failure
- `APIError`: API call failure
- `ConfigurationError`: Configuration error
- `ValidationError`: Validation error

**Usage:**
```python
from src.utils import AgentExecutionError

try:
    result = await agent.run(query)
except AgentExecutionError as e:
    print(f"Error: {e}")
```

### Helpers

**Location:** `src/utils/helpers.py`

##### `print_json(data: Any, indent: int = 2) -> str`
Pretty print JSON data.

##### `safe_parse_json(text: str, default: Dict = None) -> Dict`
Safely parse JSON with fallback.

##### `format_task_output(task_result: Dict) -> str`
Format task result for output.

## Logging

### Logger

**Location:** `src/config/logging_config.py`

**Usage:**
```python
from src.config import logger

logger.info("Information message")
logger.error("Error message")
logger.debug("Debug message")
```

**Log Levels:**
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Examples

### Creating Agents

```python
from src.framework import AgentFactory
from src.config import settings

# Create using factory
frontend = AgentFactory.create_agent(
    agent_type="frontend",
    name="ui_designer",
    model=settings.agent_model_frontend
)

backend = AgentFactory.create_agent(
    agent_type="backend",
    name="api_developer",
    model=settings.agent_model_backend
)

orchestrator = AgentFactory.create_agent(
    agent_type="orchestrator",
    name="project_manager",
    model=settings.agent_model_orchestrator
)
```

### Running Tasks

```python
import asyncio
from src.framework import TaskInput

async def main():
    task = TaskInput(
        query="Design a landing page",
        context={"style": "modern"},
        user_requirements={"responsive": True}
    )
    
    result = await frontend.execute(task)
    
    print(f"Status: {result.status}")
    print(f"Execution time: {result.execution_time}s")
    if result.status == "completed":
        print(result.result)
    else:
        print(f"Error: {result.error}")

asyncio.run(main())
```

### Error Handling

```python
from src.utils import AgentExecutionError

try:
    result = await agent.run("Design a page")
    if result.status == "failed":
        raise AgentExecutionError(result.error)
except AgentExecutionError as e:
    logger.error(f"Task failed: {e}")
```

---

For more details, see module source code and examples.
