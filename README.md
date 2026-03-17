# 🤖 Agentic AI - Professional Multi-Agent Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Quality: Production](https://img.shields.io/badge/Code%20Quality-Production-brightgreen.svg)](#)

A sophisticated, production-ready multi-agent AI orchestration system inspired by advanced AI collaboration patterns. Build complex projects by coordinating specialized AI agents with **phase-based workflows**, **dependency management**, and **parallel execution**.

## 🌟 Highlights

**Multi-Model Collaboration**
- `Gemini` → Frontend/UI specialist
- `GPT-4` → Backend/API specialist  
- `Claude` → Orchestrator & coordinator

**Enterprise Workflow System**
- Phase-based execution (Plan → Review → Execute → Validate → Complete)
- Dependency management between steps
- Parallel execution of independent tasks
- Workflow persistence and audit trail

**Professional CLI**
- 4+ slash commands for workflow management
- Real-time status monitoring
- Plan review and editing
- Human-readable workflow files

---

## ⚡ Quick Start

### Installation

```bash
# Clone and setup
git clone <repo-url> && cd agentic-website-builder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### First Workflow (60 seconds)

```bash
# 1. Generate a workflow plan
python3 agentic workflow:plan "my-project" "Build e-commerce site"

# 2. Review the generated plan
cat .workflows/my-project-*.json

# 3. Execute the workflow
python3 agentic workflow:execute ".workflows/my-project-*.json"

# 4. Monitor progress
python3 agentic workflow:status
```

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[COMMANDS.md](COMMANDS.md)** | CLI command reference & examples |
| **[WORKFLOWS.md](WORKFLOWS.md)** | Workflow concepts & best practices |
| **[ADVANCED.md](ADVANCED.md)** | Advanced patterns & customization |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design & source code |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Python API documentation |

---

## 🎯 Core Concepts

### Workflow System

```
workflow:plan → Generate multi-step plan
      ↓
workflow:execute → Orchestrate agent execution
      ↓
workflow:status → Monitor real-time progress
```

### Agent Specialization

```
Frontend Agent (Gemini)
├─ UI/UX Design
├─ HTML/CSS/JavaScript
└─ Responsive Components

Backend Agent (GPT-4)
├─ API Architecture
├─ Database Design
└─ Security Implementation

Orchestrator Agent (Claude)
├─ Workflow Coordination
├─ Quality Assurance
└─ Integration Management
```

---

## 🚀 Usage Examples

### Example 1: Simple Project

```python
from src.framework.agent_factory import AgentFactory
from src.framework.base_agent import TaskInput
import asyncio

async def main():
    agent = AgentFactory.create_agent("frontend", "UI Designer", "gemini-pro")
    task = TaskInput(query="Design a modern dashboard")
    result = await agent.execute(task)
    print(result)

asyncio.run(main())
```

### Example 2: Complete Workflow

See [WORKFLOWS.md](WORKFLOWS.md) for comprehensive workflow patterns.

```bash
python examples/build_website.py
```

## Project Structure

```
agentic-website-builder/
├── src/
│   ├── agents/                    # Specialized agents
│   │   ├── frontend_agent.py      # Gemini - Frontend specialist
│   │   ├── backend_agent.py       # GPT-4 - Backend specialist
│   │   └── orchestrator_agent.py  # Claude - Coordinator
│   ├── framework/                 # Core framework
│   │   ├── base_agent.py          # Base agent class
│   │   └── agent_factory.py       # Agent factory
│   ├── config/                    # Configuration
│   │   ├── settings.py            # Environment settings
│   │   └── logging_config.py      # Logging setup
│   ├── utils/                     # Utilities
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── helpers.py             # Helper functions
│   └── __init__.py
├── examples/
│   └── build_website.py           # Example implementation
├── tests/                         # Unit tests
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
└── README.md                      # This file
```

## Agent Architecture

### Frontend Agent (Gemini)
Specializes in:
- HTML5 semantic markup
- CSS3 and responsive design
- React, Vue, Angular components
- Accessibility (WCAG 2.1)
- Performance optimization

Capabilities:
- Design system implementation
- CSS frameworks (Tailwind, Bootstrap)
- JavaScript/TypeScript
- Mobile responsiveness

### Backend Agent (GPT-4)
Specializes in:
- REST API design
- Database architecture
- Authentication & security
- Microservices
- Cloud deployment

Capabilities:
- Python, Node.js, Go, Java
- PostgreSQL, MongoDB, DynamoDB
- GraphQL design
- Performance optimization

### Orchestrator Agent (Claude)
Specializes in:
- Project planning
- Workflow management
- Requirement analysis
- Quality assurance
- Integration coordination

Capabilities:
- Multi-agent coordination
- Risk assessment
- Timeline management
- Comprehensive documentation

## Configuration

### Environment Variables

```env
# API Keys (required)
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Agent Configuration
AGENT_MODEL_FRONTEND=gemini-pro
AGENT_MODEL_BACKEND=gpt-4
AGENT_MODEL_ORCHESTRATOR=claude-3-opus-20240229

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agentic.log

# Environment
ENVIRONMENT=development
DEBUG=False
```

## Core Components

### TaskInput

```python
from src.framework import TaskInput

task = TaskInput(
    query="Design a landing page",
    context={"industry": "Tech"},
    user_requirements={"framework": "React"}
)
```

### TaskResult

```python
from src.framework import TaskResult

# Returned by agents
result = TaskResult(
    agent_name="Frontend Developer",
    task_type="frontend_development",
    status="completed",  # pending, in_progress, completed, failed
    result={...},
    execution_time=2.5
)
```

### AgentFactory

```python
from src.framework import AgentFactory

# Create agent
agent = AgentFactory.create_agent(
    agent_type="frontend",
    name="frontend_dev",
    model="gemini-pro"
)

# List agents
agents = AgentFactory.list_agents()

# Get specific agent
agent = AgentFactory.get_agent("frontend_dev")
```

## Usage Examples

### Example 1: Building a Website

```python
import asyncio
from src.framework import AgentFactory
from src.config import settings

async def build_website():
    # Create orchestrator
    orchestrator = AgentFactory.create_agent(
        agent_type="orchestrator",
        name="manager",
        model=settings.agent_model_orchestrator
    )
    
    # Run orchestration
    result = await orchestrator.run(
        query="Build an e-commerce website",
        context={"budget": "High", "timeline": "3 months"}
    )
    
    print(result)

asyncio.run(build_website())
```

### Example 2: Direct Agent Usage

```python
import asyncio
from src.agents import FrontendAgent

async def design_ui():
    agent = FrontendAgent()
    
    result = await agent.run(
        query="Create a modern navigation bar",
        context={"style": "minimalist"}
    )
    
    print(result.result["frontend_design"])

asyncio.run(design_ui())
```

## Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Extending the System

### Creating a Custom Agent

```python
from src.framework import BaseAgent, TaskInput, TaskResult

class CustomAgent(BaseAgent):
    def __init__(self, name: str, model: str):
        super().__init__(
            name=name,
            role="custom",
            model=model,
            description="Custom agent"
        )
    
    async def execute(self, task: TaskInput) -> TaskResult:
        # Your implementation
        pass
```

### Registering with Factory

```python
from src.framework import AgentFactory

# Add to agent_factory.py in create_agent method
if agent_type.lower() == "custom":
    agent = CustomAgent(name=name, model=model)
```

## Best Practices

1. **Always await async operations**
   ```python
   result = await agent.run(query="...")  # Not agent.run(...)
   ```

2. **Use context for additional information**
   ```python
   await agent.run(
       query="Design a page",
       context={"industry": "Tech", "target": "startups"}
   )
   ```

3. **Check task status before using results**
   ```python
   if result.status == "completed":
       data = result.result
   else:
       error = result.error
   ```

4. **Monitor execution times**
   ```python
   logger.info(f"Execution took {result.execution_time:.2f}s")
   ```

## Performance Tips

- Use agent factory for efficient agent management
- Cache agent instances when possible
- Monitor logs via `logs/agentic.log`
- Use appropriate log levels in production

## Troubleshooting

### API Key Issues

```python
from src.config import settings

# Check if keys are loaded
print(settings.google_api_key)  # Should not be None
```

### Import Errors

Ensure Python path includes src:
```python
import sys
sys.path.insert(0, '/path/to/agentic')
```

### Async Issues

Always run async code with asyncio:
```python
import asyncio
asyncio.run(main())
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Contact

For questions or support:
- Email: your.email@example.com
- GitHub: @yourhandle

## Acknowledgments

Built with:
- [LangChain](https://langchain.readthedocs.io/)
- [Google Generative AI](https://developers.google.com/generative-ai)
- [OpenAI](https://openai.com/)
- [Anthropic](https://www.anthropic.com/)

---

**Made with ❤️ for agentic AI enthusiasts**
