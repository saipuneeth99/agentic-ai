"""Base Agent class for the agentic framework"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from loguru import logger
import json


class TaskInput(BaseModel):
    """Task input model"""
    query: str
    context: Optional[Dict[str, Any]] = None
    user_requirements: Optional[Dict[str, Any]] = None


class TaskResult(BaseModel):
    """Task result model"""
    agent_name: str
    task_type: str
    status: str  # "pending", "in_progress", "completed", "failed"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    execution_time: Optional[float] = None


class BaseAgent(ABC):
    """Base class for all agents in the agentic framework"""

    def __init__(
        self,
        name: str,
        role: str,
        model: str,
        description: str,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the base agent
        
        Args:
            name: Agent name
            role: Agent role (e.g., frontend, backend, orchestrator)
            model: LLM model to use
            description: Agent description
            system_prompt: Optional system prompt for the agent
        """
        self.name = name
        self.role = role
        self.model = model
        self.description = description
        self.system_prompt = system_prompt
        self.task_history: List[TaskResult] = []
        
        logger.info(f"Initialized agent: {self.name} (role: {self.role})")

    @abstractmethod
    async def execute(self, task: TaskInput) -> TaskResult:
        """Execute a task
        
        Args:
            task: Task input
            
        Returns:
            Task result
        """
        pass

    async def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> TaskResult:
        """Run a task
        
        Args:
            query: Task query
            context: Optional context
            
        Returns:
            Task result
        """
        task = TaskInput(query=query, context=context)
        result = await self.execute(task)
        self.task_history.append(result)
        return result

    def get_history(self) -> List[TaskResult]:
        """Get task history"""
        return self.task_history

    def clear_history(self) -> None:
        """Clear task history"""
        self.task_history = []

    def get_summary(self) -> Dict[str, Any]:
        """Get agent summary"""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.model,
            "description": self.description,
            "tasks_executed": len(self.task_history),
            "successful_tasks": sum(1 for t in self.task_history if t.status == "completed"),
            "failed_tasks": sum(1 for t in self.task_history if t.status == "failed"),
        }
