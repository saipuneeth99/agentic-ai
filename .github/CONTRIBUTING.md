# Contributing to Agentic Website Builder

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Avoid offensive language or behavior
- Provide constructive feedback
- Respect others' time and effort

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a feature branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Clone and setup
git clone <your-fork-url>
cd agentic-website-builder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run tests
pytest tests/ -v

# Run example
python examples/build_website.py
```

## Making Changes

1. **Branch naming**: Use `feature/`, `fix/`, or `docs/` prefixes
2. **Commits**: Write descriptive commit messages
3. **Types**: Type hint all function parameters and returns
4. **Tests**: Write tests for new functionality
5. **Documentation**: Update relevant documentation

## Commit Message Format

```
[TYPE] Brief description

Detailed explanation if needed.

Fixes: #issue_number (if applicable)
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

## Pull Request Process

1. Update documentation and examples
2. Add tests for new functionality
3. Ensure all tests pass: `pytest tests/`
4. Update CHANGELOG if applicable
5. Submit PR with clear description

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows PEP 8
- [ ] Type hints included
- [ ] Docstrings added
- [ ] No breaking changes (or documented)

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_agents.py -v

# Run specific test
pytest tests/test_agents.py::TestFrontendAgent::test_frontend_agent_creation -v
```

## Code Style

We follow PEP 8 with these preferences:

```python
# Type hints
def execute(self, task: TaskInput) -> TaskResult:
    """Execute a task."""
    pass

# Docstrings
def method(self, param: str) -> dict:
    """Brief description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass

# Imports
from typing import Dict, List, Optional
from src.framework import BaseAgent
```

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for design changes
- Update API_REFERENCE.md for API changes
- Include docstrings on all public functions
- Add examples for new features

## Reporting Bugs

Use the [Bug Report](/.github/ISSUE_TEMPLATE/bug_report.md) template.

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Python version
- Relevant logs

## Requesting Features

Use the [Feature Request](/.github/ISSUE_TEMPLATE/feature_request.md) template.

Include:
- Clear description
- Problem it solves
- Proposed solution
- Alternative approaches

## Questions?

- Check existing issues and discussions
- Review documentation in docs/
- Ask in pull request comments
- Open a discussion issue

## Resources

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Main README](README.md)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS file
- Release notes
- Project documentation

Thank you for contributing! 🙏
