"""Orchestrator Agent for coordinating other agents"""

import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
from src.config import logger
from src.utils import AgentExecutionError

# Optional LLM imports (lazy loading)
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_anthropic import ChatAnthropic
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False


class OrchestratorAgent(BaseAgent):
    """Specialized agent for orchestrating other agents"""

    def __init__(
        self,
        name: str = "Project Orchestrator",
        model: str = "claude-3-opus-20240229",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Orchestrator Agent
        
        Args:
            name: Agent name
            model: LLM model
            config: Optional configuration with api_key
        """
        super().__init__(
            name=name,
            role="orchestrator",
            model=model,
            description="Specialized in coordinating multiple agents, project planning, and workflow management",
            system_prompt="""You are an expert project orchestrator with deep expertise in:
- Multi-agent coordination and workflow management
- Project planning and task decomposition
- Requirement analysis and clarification
- Quality assurance and integration
- Risk management and contingency planning
- Team communication and collaboration

Your responsibilities:
1. Understand user requirements comprehensively
2. Break down projects into manageable tasks
3. Assign tasks to appropriate specialists
4. Coordinate between frontend and backend teams
5. Ensure seamless integration
6. Monitor progress and quality
7. Provide comprehensive project summaries""",
        )
        self.config = config or {}
        
        # Initialize LLM with API key if available
        if HAS_LANGCHAIN:
            api_key = self.config.get("api_key")
            try:
                if api_key:
                    self.llm = ChatAnthropic(model=self.model, api_key=api_key)
                    logger.info(f"{self.name}: Using real Anthropic API with key")
                else:
                    # Try using ANTHROPIC_API_KEY env var
                    self.llm = ChatAnthropic(model=self.model)
                    logger.info(f"{self.name}: Using Anthropic API from environment")
            except Exception as e:
                logger.warning(f"{self.name}: Could not initialize real LLM - {e}")
                self.llm = None  # Fall back to mock mode
        
        else:
            self.llm = None  # Mock mode - no LLM client
        self.agent_registry: Dict[str, Any] = {}

    async def execute(self, task: TaskInput) -> TaskResult:
        """Execute orchestration task
        
        Args:
            task: Task input with query and context
            
        Returns:
            Task result with orchestration plan
        """
        start_time = time.time()
        try:
            logger.info(f"{self.name}: Processing orchestration task - {task.query[:100]}")
            
            if HAS_LANGCHAIN and self.llm:
                # Build the prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", self.system_prompt),
                    ("human", f"""Analyze the following project requirements and create a comprehensive orchestration plan:

Project Goal: {task.query}

Additional Context: {task.context or 'No additional context provided'}
User Requirements: {task.user_requirements or 'No specific requirements provided'}

Provide:
1. Project Analysis and Understanding
2. Task Breakdown and Decomposition
3. Frontend Agent Tasks
4. Backend Agent Tasks
5. Integration Points
6. Timeline and Milestones
7. Risk Assessment
8. Quality Assurance Plan
9. Success Criteria""")
                ])
                
                # Create chain and execute
                chain = prompt | self.llm
                response = await chain.ainvoke({"query": task.query})
                result_content = response.content
            else:
                # Mock response when LLM is not available
                result_content = f"Mock orchestration plan for: {task.query[:50]}..."
            
            execution_time = time.time() - start_time
            
            result = TaskResult(
                agent_name=self.name,
                task_type="orchestration",
                status="completed",
                result={
                    "orchestration_plan": result_content,
                    "coordination_strategy": "Multi-agent workflow",
                    "integration_points": ["Frontend-Backend", "Database", "API", "Authentication"],
                },
                execution_time=execution_time,
            )
            
            logger.info(f"{self.name}: Task completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{self.name}: Task failed - {str(e)}")
            
            return TaskResult(
                agent_name=self.name,
                task_type="orchestration",
                status="failed",
                error=str(e),
                execution_time=execution_time,
            )

    def register_agent(self, agent_name: str, agent: Any) -> None:
        """Register an agent
        
        Args:
            agent_name: Agent name
            agent: Agent instance
        """
        self.agent_registry[agent_name] = agent
        logger.info(f"Registered agent: {agent_name}")

    def get_registered_agents(self) -> Dict[str, Any]:
        """Get all registered agents
        
        Returns:
            Dictionary of registered agents
        """
        return self.agent_registry.copy()

    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities
        
        Returns:
            Dictionary of capabilities
        """
        return {
            "coordination": [
                "Multi-agent workflows",
                "Task scheduling",
                "Agent communication",
                "Conflict resolution",
            ],
            "planning": [
                "Requirement analysis",
                "Task decomposition",
                "Timeline management",
                "Resource allocation",
            ],
            "quality": [
                "Integration testing",
                "Code review",
                "Performance monitoring",
                "Risk assessment",
            ],
        }
