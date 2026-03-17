"""Framework initialization"""

from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
from src.framework.agent_factory import AgentFactory

__all__ = [
    "BaseAgent",
    "TaskInput",
    "TaskResult",
    "AgentFactory",
]
