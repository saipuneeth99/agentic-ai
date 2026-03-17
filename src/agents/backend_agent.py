"""Backend Agent for server-side development"""

import time
from typing import Any, Dict, Optional
from datetime import datetime

from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
from src.config import logger
from src.utils import AgentExecutionError

# Optional LLM imports (lazy loading)
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False


class BackendAgent(BaseAgent):
    """Specialized agent for backend development"""

    def __init__(
        self,
        name: str = "Backend Developer",
        model: str = "gpt-4",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Backend Agent
        
        Args:
            name: Agent name
            model: LLM model
            config: Optional configuration with api_key
        """
        super().__init__(
            name=name,
            role="backend",
            model=model,
            description="Specialized in server-side development, databases, APIs, and system architecture",
            system_prompt="""You are an expert backend developer with deep expertise in:
- RESTful API design and GraphQL
- Database design (SQL, NoSQL)
- Authentication and security
- Scalability and performance optimization
- Cloud deployment (AWS, GCP, Azure)
- Microservices architecture

Always provide:
1. Clean, maintainable code
2. Proper error handling and logging
3. Security best practices
4. Database schema design
5. API documentation
6. Performance considerations""",
        )
        self.config = config or {}
        
        # Initialize LLM with API key if available
        if HAS_LANGCHAIN:
            api_key = self.config.get("api_key")
            try:
                if api_key:
                    self.llm = ChatOpenAI(model=self.model, api_key=api_key)
                    logger.info(f"{self.name}: Using real OpenAI API with key")
                else:
                    # Try using OPENAI_API_KEY env var
                    self.llm = ChatOpenAI(model=self.model)
                    logger.info(f"{self.name}: Using OpenAI API from environment")
            except Exception as e:
                logger.warning(f"{self.name}: Could not initialize real LLM - {e}")
                self.llm = None  # Fall back to mock mode
        else:
            self.llm = None  # Mock mode - no LLM client

    async def execute(self, task: TaskInput) -> TaskResult:
        """Execute a backend development task
        
        Args:
            task: Task input with query and context
            
        Returns:
            Task result with generated backend code/architecture
        """
        start_time = time.time()
        try:
            logger.info(f"{self.name}: Processing task - {task.query[:100]}")
            
            if HAS_LANGCHAIN and self.llm:
                # Build the prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", self.system_prompt),
                    ("human", f"""Design and generate backend code/architecture for the following requirements:

Query: {task.query}

Additional Context: {task.context or 'No additional context provided'}
User Requirements: {task.user_requirements or 'No specific requirements provided'}

Provide:
1. API endpoints specification
2. Database schema design
3. Authentication strategy
4. Code implementation (Python/Node.js/Go)
5. Error handling strategy
6. Security considerations
7. Deployment approach""")
                ])
                
                # Create chain and execute
                chain = prompt | self.llm
                response = await chain.ainvoke({"query": task.query})
                result_content = response.content
            else:
                # Mock response when LLM is not available
                result_content = f"Mock backend architecture for: {task.query[:50]}..."
            
            execution_time = time.time() - start_time
            
            result = TaskResult(
                agent_name=self.name,
                task_type="backend_development",
                status="completed",
                result={
                    "backend_architecture": result_content,
                    "components": ["API endpoints", "Database schema", "Authentication", "Error handling"],
                    "security_level": "Enterprise-grade",
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
                task_type="backend_development",
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
            "languages": ["Python", "Node.js", "Go", "Java", "Rust"],
            "frameworks": ["FastAPI", "Django", "Express", "Go Gin", "Spring Boot"],
            "databases": ["PostgreSQL", "MongoDB", "DynamoDB", "Redis", "Elasticsearch"],
            "specialties": [
                "REST API design",
                "GraphQL",
                "Microservices",
                "Database optimization",
                "Authentication & Authorization",
                "Caching strategies",
                "Message queues",
            ],
        }
