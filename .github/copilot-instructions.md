# Copilot Instructions for Agentic Website Builder

## Project Overview

This is a professional, production-ready multi-agent AI system for building websites using specialized agents:

- **Frontend Agent (Gemini)**: UI/UX design, HTML, CSS, JavaScript
- **Backend Agent (GPT-4)**: API design, database architecture, server-side logic
- **Orchestrator Agent (Claude)**: Project coordination and integration

## Development Guidelines

### Architecture Principles
- Use async/await for all IO operations
- Maintain separation of concerns across agent roles
- Keep framework code generic and agent code specialized
- Use factory pattern for agent creation
- Leverage Pydantic for data validation

### Code Style
- PEP 8 compliance
- Type hints on all functions
- Comprehensive docstrings
- Logging using loguru
- Error handling with custom exceptions

### File Organization
```
src/
├── agents/          # Specialized agent implementations
├── framework/       # Core framework classes
├── config/          # Configuration and settings
├── utils/           # Utilities and helpers
examples/            # Example implementations
tests/               # Unit tests
docs/                # Documentation
```

### Key Conventions

1. **Agents**
   - Inherit from BaseAgent
   - Implement async execute() method
   - Return TaskResult with structured data
   - Maintain task history

2. **Configuration**
   - Load from environment variables via .env
   - Use Settings class from pydantic_settings
   - Never hardcode API keys

3. **Logging**
   - Use logger from src.config
   - Include context in log messages
   - Use appropriate log levels

4. **Error Handling**
   - Use custom exceptions from src.utils
   - Log before raising exceptions
   - Return failed TaskResult instead of raising in execute()

### Testing
- Write unit tests for new agents
- Test framework components
- Use pytest fixtures
- Mock LLM responses when appropriate
- Maintain >80% code coverage

### Documentation
- Update API_REFERENCE.md for API changes
- Update ARCHITECTURE.md for design changes
- Include docstrings on all public methods
- Add examples to README.md

### Git Workflow
1. Create feature branch from main
2. Commit with descriptive messages
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

## Common Tasks

### Adding a New Agent Type

1. Create new file in `src/agents/`
2. Inherit from BaseAgent
3. Implement async execute() method
4. Add to agent_factory.py create_agent()
5. Add tests in `tests/test_agents.py`
6. Update documentation

### Adding Configuration Options

1. Add environment variable to .env.example
2. Add field to Settings class
3. Use in applicable agents
4. Document in API_REFERENCE.md

### Adding Dependencies

1. Add to requirements.txt
2. Update pyproject.toml optional-dependencies
3. Document why it's needed
4. Ensure compatibility with existing packages

## Performance Considerations

- Use async for concurrent agent tasks
- Cache agent instances when possible
- Monitor execution times via TaskResult
- Clean up task history periodically
- Use appropriate log levels in production

## Debugging Tips

1. Enable DEBUG=true in .env
2. Check logs in logs/agentic.log
3. Use agent.get_history() to review past tasks
4. Verify API keys are properly set
5. Check Python version compatibility

## Contributing

When contributing to this project:
1. Follow these guidelines
2. Maintain code quality
3. Add tests for new features
4. Update documentation
5. Include examples when appropriate

## Resources

- [LangChain Documentation](https://langchain.readthedocs.io/)
- [Google Generative AI](https://developers.google.com/generative-ai)
- [OpenAI Docs](https://platform.openai.com/docs)
- [Anthropic Docs](https://docs.anthropic.com/)

## Project Status

- ✅ Core framework complete
- ✅ Specialized agents implemented
- ✅ Configuration management
- ✅ Comprehensive testing
- ✅ Full documentation
- 🔄 Ongoing: Advanced features and integrations
