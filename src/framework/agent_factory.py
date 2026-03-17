"""Agent factory for creating specialized agents"""

import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from src.agents.frontend_agent import FrontendAgent
from src.agents.backend_agent import BackendAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.framework.base_agent import BaseAgent
from src.config import logger


class AgentFactory:
    """Factory for creating agents"""

    _agents: Dict[str, BaseAgent] = {}

    @staticmethod
    def _get_current_user() -> Optional[str]:
        """Get current logged-in user"""
        session_file = Path(".users/.session")
        if session_file.exists():
            try:
                with open(session_file, "r") as f:
                    session = json.load(f)
                    return session.get("current_user")
            except:
                pass
        return None

    @staticmethod
    def _load_api_key(provider: str, username: Optional[str] = None) -> Optional[str]:
        """Load API key for a provider from user's token storage
        
        Args:
            provider: Provider name (google, openai, anthropic)
            username: Username (uses current user if not provided)
            
        Returns:
            API key or None if not found
        """
        if not username:
            username = AgentFactory._get_current_user()
        
        if not username:
            return None
        
        token_file = Path(f".oauth_tokens/{username}_{provider}_token.json")
        if token_file.exists():
            try:
                with open(token_file, "r") as f:
                    token_data = json.load(f)
                    return token_data.get("api_key")
            except Exception as e:
                logger.error(f"Failed to load {provider} API key: {e}")
        
        return None

    @classmethod
    def create_agent(
        cls,
        agent_type: str,
        name: str,
        model: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> BaseAgent:
        """Create an agent of the specified type with user's API keys
        
        Args:
            agent_type: Type of agent (frontend, backend, orchestrator)
            name: Agent name
            model: LLM model
            config: Optional configuration
            
        Returns:
            Created agent instance
        """
        if config is None:
            config = {}
        
        logger.info(f"Creating agent: {name} ({agent_type})")
        
        # Load API keys for the agent based on its type
        if agent_type.lower() == "frontend":
            api_key = cls._load_api_key("google")
            logger.info(f"Google API key loaded: {bool(api_key)}")
            if api_key:
                config["api_key"] = api_key
            agent = FrontendAgent(name=name, model=model, config=config)
        elif agent_type.lower() == "backend":
            api_key = cls._load_api_key("openai")
            logger.info(f"OpenAI API key loaded: {bool(api_key)}")
            if api_key:
                config["api_key"] = api_key
            agent = BackendAgent(name=name, model=model, config=config)
        elif agent_type.lower() == "orchestrator":
            api_key = cls._load_api_key("anthropic")
            logger.info(f"Anthropic API key loaded: {bool(api_key)}")
            if api_key:
                config["api_key"] = api_key
            agent = OrchestratorAgent(name=name, model=model, config=config)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

        cls._agents[name] = agent
        return agent

    @classmethod
    def get_agent(cls, name: str) -> Optional[BaseAgent]:
        """Get an agent by name
        
        Args:
            name: Agent name
            
        Returns:
            Agent or None if not found
        """
        return cls._agents.get(name)

    @classmethod
    def list_agents(cls) -> Dict[str, BaseAgent]:
        """List all registered agents
        
        Returns:
            Dictionary of agents
        """
        return cls._agents.copy()

    @classmethod
    def remove_agent(cls, name: str) -> bool:
        """Remove an agent
        
        Args:
            name: Agent name
            
        Returns:
            True if removed, False if not found
        """
        if name in cls._agents:
            del cls._agents[name]
            return True
        return False

    @classmethod
    def clear_agents(cls) -> None:
        """Clear all agents"""
        cls._agents.clear()
