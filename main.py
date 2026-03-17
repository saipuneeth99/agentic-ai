#!/usr/bin/env python
"""Main entry point for the agentic website builder"""

import asyncio
import sys
from typing import Optional
import fire
from src.framework import AgentFactory
from src.config import logger, settings
from src.utils import print_json


class AgenticCLI:
    """Command-line interface for the agentic system"""

    def create_agent(
        self,
        agent_type: str,
        name: str,
        model: Optional[str] = None,
    ):
        """Create a new agent
        
        Args:
            agent_type: Type of agent (frontend, backend, orchestrator)
            name: Agent name
            model: Optional model override
        """
        logger.info(f"Creating {agent_type} agent: {name}")
        
        # Use provided model or default
        model_map = {
            "frontend": settings.agent_model_frontend,
            "backend": settings.agent_model_backend,
            "orchestrator": settings.agent_model_orchestrator,
        }
        
        model = model or model_map.get(agent_type.lower())
        
        if not model:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent = AgentFactory.create_agent(
            agent_type=agent_type,
            name=name,
            model=model,
        )
        
        logger.info(f"✓ Agent created: {agent.name}")
        return {
            "name": agent.name,
            "role": agent.role,
            "model": agent.model,
        }

    def list_agents(self):
        """List all registered agents"""
        agents = AgentFactory.list_agents()
        logger.info(f"Registered agents: {len(agents)}")
        
        result = {}
        for name, agent in agents.items():
            result[name] = {
                "role": agent.role,
                "model": agent.model,
                "description": agent.description,
            }
        
        return result

    def remove_agent(self, name: str):
        """Remove an agent
        
        Args:
            name: Agent name
        """
        if AgentFactory.remove_agent(name):
            logger.info(f"✓ Agent removed: {name}")
            return {"status": "success", "removed": name}
        else:
            logger.warning(f"Agent not found: {name}")
            return {"status": "error", "message": f"Agent {name} not found"}

    def status(self):
        """Show system status"""
        agents = AgentFactory.list_agents()
        
        return {
            "registered_agents": len(agents),
            "environment": settings.environment,
            "debug": settings.debug,
            "log_level": settings.log_level,
            "agents": list(agents.keys()),
        }

    def run_example(self):
        """Run the portfolio website builder example"""
        logger.info("Running portfolio website builder example...")
        logger.info("This requires valid API keys in .env")
        
        try:
            # Import and run the example
            from examples.build_website import build_website_example
            asyncio.run(build_website_example())
            logger.info("✓ Example completed successfully!")
        except Exception as e:
            logger.error(f"Example failed: {e}")
            return {"status": "error", "error": str(e)}
        
        return {"status": "success", "message": "Example completed"}


def main():
    """Main entry point"""
    fire.Fire(AgenticCLI)


if __name__ == "__main__":
    main()
