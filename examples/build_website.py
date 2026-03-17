"""Example: Build a portfolio website using the agentic system"""

import asyncio
from src.framework.agent_factory import AgentFactory
from src.config import logger, settings
from src.utils import print_json


async def build_website_example():
    """Example workflow: Building a portfolio website using multiple agents"""
    
    logger.info("=" * 80)
    logger.info("Starting Portfolio Website Builder Example")
    logger.info("=" * 80)
    
    # Create agents using the factory
    logger.info("\n1. Creating specialized agents...")
    
    orchestrator = AgentFactory.create_agent(
        agent_type="orchestrator",
        name="project_manager",
        model=settings.agent_model_orchestrator,
    )
    
    frontend_dev = AgentFactory.create_agent(
        agent_type="frontend",
        name="frontend_specialist",
        model=settings.agent_model_frontend,
    )
    
    backend_dev = AgentFactory.create_agent(
        agent_type="backend",
        name="backend_specialist",
        model=settings.agent_model_backend,
    )
    
    logger.info("✓ Agents created successfully")
    logger.info(f"  - Orchestrator: {orchestrator.name}")
    logger.info(f"  - Frontend: {frontend_dev.name}")
    logger.info(f"  - Backend: {backend_dev.name}")
    
    # Project requirements
    project_goal = "Build a modern portfolio website showcasing professional projects and skills"
    
    logger.info("\n2. Orchestrating project...")
    logger.info(f"Project Goal: {project_goal}")
    
    # Step 1: Orchestrator analyzes requirements and creates plan
    orchestration_result = await orchestrator.run(
        query=project_goal,
        context={
            "industry": "Technology",
            "target_audience": "Potential employers and clients",
            "features": ["Projects showcase", "Skills section", "Contact form", "Blog"]
        },
        user_requirements={
            "modern_design": True,
            "responsive": True,
            "seo_optimized": True,
            "dark_mode": True,
        }
    )
    
    logger.info(f"✓ Orchestration plan created")
    logger.info("\nOrchestration Plan:")
    logger.info(orchestration_result.result.get("orchestration_plan", "N/A")[:500])
    
    # Step 2: Frontend agent designs the UI
    logger.info("\n3. Frontend agent designing UI/UX...")
    
    frontend_result = await frontend_dev.run(
        query="Design modern portfolio website with dark mode, smooth animations, and responsive layout",
        context={"style_preference": "Minimalist", "color_scheme": "Dark with accent colors"},
        user_requirements={"accessibility": "WCAG 2.1 AA", "frameworks": "React with Tailwind CSS"}
    )
    
    logger.info(f"✓ Frontend design completed")
    if frontend_result.status == "completed":
        logger.info("Frontend Design Summary:")
        design = frontend_result.result.get("frontend_design", "")
        logger.info(design[:500] if isinstance(design, str) else str(design))
    
    # Step 3: Backend agent designs the architecture
    logger.info("\n4. Backend agent designing architecture...")
    
    backend_result = await backend_dev.run(
        query="Design backend API for portfolio website with project showcase, contact submissions, and blog posts",
        context={"database": "PostgreSQL", "hosting": "AWS"},
        user_requirements={"authentication": "JWT", "api_style": "RESTful"}
    )
    
    logger.info(f"✓ Backend architecture designed")
    if backend_result.status == "completed":
        logger.info("Backend Architecture Summary:")
        architecture = backend_result.result.get("backend_architecture", "")
        logger.info(architecture[:500] if isinstance(architecture, str) else str(architecture))
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("Project Summary")
    logger.info("=" * 80)
    
    logger.info("\nAgent Statistics:")
    for agent_name, agent in AgentFactory.list_agents().items():
        summary = agent.get_summary()
        logger.info(f"\n{agent_name}:")
        logger.info(f"  - Tasks executed: {summary['tasks_executed']}")
        logger.info(f"  - Successful: {summary['successful_tasks']}")
        logger.info(f"  - Failed: {summary['failed_tasks']}")
    
    logger.info("\n" + "=" * 80)
    logger.info("Portfolio Website Build Complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(build_website_example())
