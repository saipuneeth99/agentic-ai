"""Main package initialization"""

from src.config import settings, logger
from src.framework import BaseAgent, TaskInput, TaskResult, AgentFactory
from src.agents import FrontendAgent, BackendAgent, OrchestratorAgent

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "settings",
    "logger",
    "BaseAgent",
    "TaskInput",
    "TaskResult",
    "AgentFactory",
    "FrontendAgent",
    "BackendAgent",
    "OrchestratorAgent",
]
