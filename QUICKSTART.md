# Quick Start Guide

Get up and running with Agentic Website Builder in 5 minutes.

## 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# GOOGLE_API_KEY=your_key
# OPENAI_API_KEY=your_key
# ANTHROPIC_API_KEY=your_key
```

## 2. Basic Agent Creation

```python
from src.framework import AgentFactory
from src.config import settings
import asyncio

async def main():
    # Create agents
    frontend = AgentFactory.create_agent(
        agent_type="frontend",
        name="ui_designer",
        model=settings.agent_model_frontend
    )
    
    # Use agent
    result = await frontend.run(
        query="Design a modern landing page"
    )
    
    print(result)

asyncio.run(main())
```

## 3. Run Example

```bash
python examples/build_website.py
```

## 4. Key Concepts

### Agents
- **Frontend Agent**: Designs UI/UX, generates HTML/CSS/JS
- **Backend Agent**: Designs APIs, databases, architecture
- **Orchestrator Agent**: Coordinates and integrates all work

### Factory Pattern
```python
# Create any agent
agent = AgentFactory.create_agent(
    agent_type="frontend",  # or "backend", "orchestrator"
    name="my_agent",
    model="gemini-pro"
)
```

### Task Execution
```python
result = await agent.run(
    query="Your task",
    context={"info": "value"},
)

# Check status
if result.status == "completed":
    print(result.result)
else:
    print(result.error)
```

## 5. Configuration

### API Keys
All API keys go in `.env` file:
```env
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

### Models
Change which LLM each agent uses:
```env
AGENT_MODEL_FRONTEND=gemini-pro
AGENT_MODEL_BACKEND=gpt-4
AGENT_MODEL_ORCHESTRATOR=claude-3-opus-20240229
```

### Logging
```env
LOG_LEVEL=INFO
LOG_FILE=logs/agentic.log
```

## 6. Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

## 7. Next Steps

- Read [README.md](../README.md) for complete documentation
- Check [Architecture Guide](../docs/ARCHITECTURE.md) for system design
- Review [API Reference](../docs/API_REFERENCE.md) for all classes
- Explore [examples/](../examples/) for more use cases

## 8. Common Questions

**Q: How do I create a custom agent?**
A: Inherit from BaseAgent and implement async execute() method

**Q: Can I use different models?**
A: Yes! Update AGENT_MODEL_* in .env

**Q: How do I see what's happening?**
A: Check logs/agentic.log or set DEBUG=true

**Q: How do I test my changes?**
A: Create tests in tests/ and run pytest

## 9. Architecture Overview

```
User Input
    ↓
Orchestrator (Claude)
    ├─→ Frontend (Gemini)
    └─→ Backend (GPT-4)
    ↓
Integrated Output
```

## 10. Troubleshooting

**ImportError**: Make sure you're in the project root directory

**Missing API Keys**: Check .env file has all required keys

**Task Failed**: Check logs/agentic.log for error details

**Async Error**: Always use `await` with async functions

---

For more help, see [CONTRIBUTING.md](.github/CONTRIBUTING.md) or open an issue.
