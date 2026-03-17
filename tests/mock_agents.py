"""Mock agents for testing the framework without LLM dependencies"""

import time
from typing import Any, Dict, Optional
from src.framework.base_agent import BaseAgent, TaskInput, TaskResult


class MockFrontendAgent(BaseAgent):
    """Mock Frontend Agent for testing"""

    def __init__(self, name: str = "Mock Frontend", model: str = "gemini-mock"):
        super().__init__(
            name=name,
            role="frontend",
            model=model,
            description="Mock frontend agent for testing",
        )

    async def execute(self, task: TaskInput) -> TaskResult:
        """Mock execution"""
        start_time = time.time()
        try:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="frontend_development",
                status="completed",
                result={"design": "Mock frontend design", "query": task.query},
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="frontend_development",
                status="failed",
                error=str(e),
                execution_time=execution_time,
            )


class MockBackendAgent(BaseAgent):
    """Mock Backend Agent for testing"""

    def __init__(self, name: str = "Mock Backend", model: str = "gpt-4-mock"):
        super().__init__(
            name=name,
            role="backend",
            model=model,
            description="Mock backend agent for testing",
        )

    async def execute(self, task: TaskInput) -> TaskResult:
        """Mock execution"""
        start_time = time.time()
        try:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="backend_development",
                status="completed",
                result={"architecture": "Mock API design", "query": task.query},
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="backend_development",
                status="failed",
                error=str(e),
                execution_time=execution_time,
            )


class MockOrchestratorAgent(BaseAgent):
    """Mock Orchestrator Agent for testing"""

    def __init__(self, name: str = "Mock Orchestrator", model: str = "claude-mock"):
        super().__init__(
            name=name,
            role="orchestrator",
            model=model,
            description="Mock orchestrator agent for testing",
        )
        self.agent_registry: Dict[str, Any] = {}

    async def execute(self, task: TaskInput) -> TaskResult:
        """Mock execution"""
        start_time = time.time()
        try:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="orchestration",
                status="completed",
                result={"plan": "Mock orchestration plan", "query": task.query},
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                agent_name=self.name,
                task_type="orchestration",
                status="failed",
                error=str(e),
                execution_time=execution_time,
            )

    def register_agent(self, agent_name: str, agent: Any) -> None:
        """Register an agent"""
        self.agent_registry[agent_name] = agent

    def get_registered_agents(self) -> Dict[str, Any]:
        """Get registered agents"""
        return self.agent_registry.copy()

    def get_capabilities(self) -> Dict[str, Any]:
        """Get capabilities"""
        return {
            "coordination": ["Mock coordination"],
            "planning": ["Mock planning"],
            "quality": ["Mock QA"],
        }
