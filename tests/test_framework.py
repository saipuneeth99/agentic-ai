"""Tests for the agentic framework"""

import pytest
from src.framework import BaseAgent, TaskInput, TaskResult, AgentFactory
from src.config import settings
from datetime import datetime


class TestTaskInput:
    """Test TaskInput model"""

    def test_task_input_creation(self):
        """Test creating a task input"""
        task = TaskInput(query="Test query")
        assert task.query == "Test query"
        assert task.context is None

    def test_task_input_with_context(self):
        """Test task input with context"""
        context = {"key": "value"}
        task = TaskInput(query="Test", context=context)
        assert task.context == context


class TestTaskResult:
    """Test TaskResult model"""

    def test_task_result_creation(self):
        """Test creating a task result"""
        result = TaskResult(
            agent_name="test_agent",
            task_type="test",
            status="completed",
            result={"data": "test"}
        )
        assert result.agent_name == "test_agent"
        assert result.status == "completed"

    def test_task_result_timestamp(self):
        """Test task result has timestamp"""
        result = TaskResult(
            agent_name="test",
            task_type="test",
            status="completed"
        )
        assert isinstance(result.timestamp, datetime)


class TestAgentFactory:
    """Test AgentFactory"""

    def setup_method(self):
        """Clear agents before each test"""
        AgentFactory.clear_agents()

    def test_create_frontend_agent(self):
        """Test creating a frontend agent"""
        agent = AgentFactory.create_agent(
            agent_type="frontend",
            name="test_frontend",
            model="gemini-pro"
        )
        assert agent is not None
        assert agent.name == "test_frontend"
        assert agent.role == "frontend"

    def test_create_backend_agent(self):
        """Test creating a backend agent"""
        agent = AgentFactory.create_agent(
            agent_type="backend",
            name="test_backend",
            model="gpt-4"
        )
        assert agent is not None
        assert agent.role == "backend"

    def test_create_orchestrator_agent(self):
        """Test creating an orchestrator agent"""
        agent = AgentFactory.create_agent(
            agent_type="orchestrator",
            name="test_orchestrator",
            model="claude-3-opus-20240229"
        )
        assert agent is not None
        assert agent.role == "orchestrator"

    def test_get_agent(self):
        """Test getting an agent"""
        AgentFactory.create_agent(
            agent_type="frontend",
            name="test",
            model="gemini-pro"
        )
        agent = AgentFactory.get_agent("test")
        assert agent is not None
        assert agent.name == "test"

    def test_list_agents(self):
        """Test listing agents"""
        AgentFactory.create_agent(
            agent_type="frontend",
            name="agent1",
            model="gemini-pro"
        )
        AgentFactory.create_agent(
            agent_type="backend",
            name="agent2",
            model="gpt-4"
        )
        agents = AgentFactory.list_agents()
        assert len(agents) == 2

    def test_remove_agent(self):
        """Test removing an agent"""
        AgentFactory.create_agent(
            agent_type="frontend",
            name="test",
            model="gemini-pro"
        )
        removed = AgentFactory.remove_agent("test")
        assert removed is True
        assert AgentFactory.get_agent("test") is None

    def test_clear_agents(self):
        """Test clearing all agents"""
        AgentFactory.create_agent(
            agent_type="frontend",
            name="test",
            model="gemini-pro"
        )
        AgentFactory.clear_agents()
        agents = AgentFactory.list_agents()
        assert len(agents) == 0

    def test_invalid_agent_type(self):
        """Test creating agent with invalid type"""
        with pytest.raises(ValueError):
            AgentFactory.create_agent(
                agent_type="invalid",
                name="test",
                model="test"
            )


class TestSettings:
    """Test configuration settings"""

    def test_settings_loaded(self):
        """Test that settings are loaded"""
        assert settings is not None
        assert hasattr(settings, 'log_level')

    def test_default_log_level(self):
        """Test default log level"""
        assert settings.log_level in ["INFO", "DEBUG", "WARNING", "ERROR"]

    def test_environment(self):
        """Test environment setting"""
        assert settings.environment in ["development", "production"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
