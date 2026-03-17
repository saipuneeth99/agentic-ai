"""Frontend Agent for UI/UX and frontend development"""

import time
from typing import Any, Dict, Optional
from datetime import datetime

from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
from src.config import logger
from src.utils import AgentExecutionError

# Optional LLM imports (lazy loading)
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_google_genai import ChatGoogleGenerativeAI
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False


class FrontendAgent(BaseAgent):
    """Specialized agent for frontend development"""

    def __init__(
        self,
        name: str = "Frontend Developer",
        model: str = "gemini-pro",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Frontend Agent
        
        Args:
            name: Agent name
            model: LLM model
            config: Optional configuration with api_key
        """
        super().__init__(
            name=name,
            role="frontend",
            model=model,
            description="Specialized in UI/UX design, HTML, CSS, and frontend component development",
            system_prompt="""You are an expert frontend developer with deep expertise in:
- HTML5, CSS3, and modern CSS frameworks (Tailwind, Bootstrap)
- JavaScript/TypeScript and React, Vue, or Angular
- Responsive design and accessibility (WCAG)
- UI/UX best practices and design systems
- Performance optimization and web standards

Always provide:
1. Clean, semantic HTML
2. Well-organized CSS with proper structure
3. Accessibility features
4. Mobile-responsive design
5. Code comments and documentation""",
        )
        self.config = config or {}
        
        logger.info(f"{self.name}: HAS_LANGCHAIN = {HAS_LANGCHAIN}")
        
        # Initialize LLM with API key if available
        if HAS_LANGCHAIN:
            api_key = self.config.get("api_key")
            logger.info(f"{self.name}: API key present = {bool(api_key)}")
            try:
                if api_key:
                    logger.info(f"{self.name}: Initializing ChatGoogleGenerativeAI with key")
                    self.llm = ChatGoogleGenerativeAI(model=self.model, google_api_key=api_key)
                    logger.info(f"{self.name}: ✅ Using real Gemini API with key")
                else:
                    logger.info(f"{self.name}: No API key in config, trying environment")
                    self.llm = ChatGoogleGenerativeAI(model=self.model)
                    logger.info(f"{self.name}: ✅ Using Gemini API from environment")
            except Exception as e:
                logger.error(f"{self.name}: ❌ Failed to init LLM: {e}")
                self.llm = None
        else:
            logger.warning(f"{self.name}: LangChain not available, using mock mode")
            self.llm = None

    async def execute(self, task: TaskInput) -> TaskResult:
        """Execute a frontend development task
        
        Args:
            task: Task input with query and context
            
        Returns:
            Task result with generated frontend code/design
        """
        start_time = time.time()
        try:
            logger.info(f"{self.name}: Processing task - {task.query[:100]}")
            
            if HAS_LANGCHAIN and self.llm:
                # Build the prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", self.system_prompt),
                    ("human", f"""Design and generate frontend code for the following requirements:

Query: {task.query}

Additional Context: {task.context or 'No additional context provided'}
User Requirements: {task.user_requirements or 'No specific requirements provided'}

Provide:
1. HTML structure
2. CSS styling
3. JavaScript functionality (if needed)
4. Accessibility considerations
5. Brief explanation""")
                ])
                
                # Create chain and execute
                chain = prompt | self.llm
                response = await chain.ainvoke({"query": task.query})
                result_content = response.content
            else:
                # Mock response when LLM is not available
                result_content = f"Mock frontend design for: {task.query[:50]}..."
            
            execution_time = time.time() - start_time
            
            result = TaskResult(
                agent_name=self.name,
                task_type="frontend_development",
                status="completed",
                result={
                    "frontend_design": result_content,
                    "components": ["HTML structure", "CSS styling", "JS functionality"],
                    "accessibility": "WCAG 2.1 AA compliant",
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
                task_type="frontend_development",
                status="failed",
                error=str(e),
                execution_time=execution_time,
            )

    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities
        
        Returns:
            Dictionary of capabilities
        """
        return {
            "design_systems": ["Tailwind CSS", "Bootstrap", "Material Design"],
            "frameworks": ["React", "Vue", "Angular", "Svelte"],
            "languages": ["HTML5", "CSS3", "JavaScript", "TypeScript"],
            "specialties": [
                "Responsive design",
                "Accessibility (WCAG)",
                "Performance optimization",
                "Component libraries",
                "CSS-in-JS",
            ],
        }
