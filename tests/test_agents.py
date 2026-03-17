"""Tests for agents"""

import pytest
from src.agents import FrontendAgent, BackendAgent, OrchestratorAgent


class TestFrontendAgent:
    """Test Frontend Agent"""

    def test_frontend_agent_creation(self):
        """Test creating frontend agent"""
        agent = FrontendAgent()
        assert agent.name == "Frontend Developer"
        assert agent.role == "frontend"
        assert agent.model == "gemini-pro"

    def test_frontend_agent_capabilities(self):
        """Test frontend agent capabilities"""
        agent = FrontendAgent()
        capabilities = agent.get_capabilities()
        assert "design_systems" in capabilities
        assert "frameworks" in capabilities


class TestBackendAgent:
    """Test Backend Agent"""

    def test_backend_agent_creation(self):
        """Test creating backend agent"""
        agent = BackendAgent()
        assert agent.name == "Backend Developer"
        assert agent.role == "backend"
        assert agent.model == "gpt-4"

    def test_backend_agent_capabilities(self):
        """Test backend agent capabilities"""
        agent = BackendAgent()
        capabilities = agent.get_capabilities()
        assert "languages" in capabilities
        assert "frameworks" in capabilities


class TestOrchestratorAgent:
    """Test Orchestrator Agent"""

    def test_orchestrator_agent_creation(self):
        """Test creating orchestrator agent"""
        agent = OrchestratorAgent()
        assert agent.name == "Project Orchestrator"
        assert agent.role == "orchestrator"

    def test_orchestrator_agent_register(self):
        """Test registering agents"""
        orchestrator = OrchestratorAgent()
        frontend = FrontendAgent()
        
        orchestrator.register_agent("frontend", frontend)
        agents = orchestrator.get_registered_agents()
        
        assert "frontend" in agents
        assert agents["frontend"] == frontend


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
