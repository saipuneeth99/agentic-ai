#!/usr/bin/env python3
"""
Demo: How to Use the Agentic AI Project
Showcases the framework in action with real examples
"""

import asyncio
from src.framework import AgentFactory, TaskInput
from tests.mock_agents import MockFrontendAgent, MockBackendAgent, MockOrchestratorAgent


async def demo_1_simple_agent_usage():
    """Demo 1: Create and use a single agent"""
    print("\n" + "="*70)
    print("DEMO 1: Simple Agent Usage")
    print("="*70)
    
    # Create an agent
    frontend = MockFrontendAgent(name="UI Designer")
    
    # Run a task
    result = await frontend.run(
        query="Design a landing page for a SaaS product",
        context={"brand_color": "blue", "target_audience": "B2B"}
    )
    
    print(f"\nAgent: {result.agent_name}")
    print(f"Task Type: {result.task_type}")
    print(f"Status: {result.status}")
    if result.result:
        design_key = 'frontend_design' if 'frontend_design' in result.result else 'design'
        print(f"Result: {result.result.get(design_key, str(result.result)[:100])}")
    print(f"Execution Time: {result.execution_time:.4f}s")


async def demo_2_multiple_agents():
    """Demo 2: Coordinate multiple agents (no factory)"""
    print("\n" + "="*70)
    print("DEMO 2: Multiple Agents Coordination")
    print("="*70)
    
    frontend = MockFrontendAgent(name="Frontend Specialist")
    backend = MockBackendAgent(name="Backend Specialist")
    
    print("\n[Step 1] Frontend Agent designs the UI...")
    frontend_result = await frontend.run(
        query="Create a modern dashboard UI"
    )
    print(f"✓ Frontend Design: {frontend_result.status}")
    
    print("\n[Step 2] Backend Agent designs the API...")
    backend_result = await backend.run(
        query="Design REST API for dashboard data"
    )
    print(f"✓ Backend API: {backend_result.status}")
    
    print("\n[Step 3] Integration...")
    print(f"✓ Frontend and Backend integrated successfully")
    print(f"  - Frontend tasks: {len(frontend.get_history())}")
    print(f"  - Backend tasks: {len(backend.get_history())}")


async def demo_3_agent_factory():
    """Demo 3: Using AgentFactory to manage agents"""
    print("\n" + "="*70)
    print("DEMO 3: Agent Factory Pattern")
    print("="*70)
    
    # Create agents using factory
    AgentFactory.clear_agents()
    
    print("\nCreating agents with factory...")
    frontend = AgentFactory.create_agent("frontend", "web_designer", "gemini-pro")
    backend = AgentFactory.create_agent("backend", "api_developer", "gpt-4")
    orchestrator = AgentFactory.create_agent("orchestrator", "project_manager", "claude")
    
    print(f"✓ Created {len(AgentFactory.list_agents())} agents")
    
    # List all agents
    print("\nRegistered Agents:")
    for name, agent in AgentFactory.list_agents().items():
        print(f"  - {name}: {agent.role} (model: {agent.model})")


async def demo_4_task_tracking():
    """Demo 4: Task history and metrics"""
    print("\n" + "="*70)
    print("DEMO 4: Task Tracking & Metrics")
    print("="*70)
    
    agent = MockFrontendAgent(name="Performance Monitor")
    
    # Run multiple tasks
    print("\nRunning multiple tasks...")
    for i in range(3):
        await agent.run(query=f"Task {i+1}: Design component #{i+1}")
        print(f"  ✓ Task {i+1} completed")
    
    # Get summary
    summary = agent.get_summary()
    print("\nAgent Summary:")
    print(f"  Name: {summary['name']}")
    print(f"  Role: {summary['role']}")
    print(f"  Total Tasks: {summary['tasks_executed']}")
    print(f"  Successful: {summary['successful_tasks']}")
    print(f"  Failed: {summary['failed_tasks']}")
    
    # Get history
    history = agent.get_history()
    print(f"\nTask History ({len(history)} tasks):")
    for i, task in enumerate(history, 1):
        print(f"  {i}. {task.task_type} - {task.status}")


async def demo_5_real_world_scenario():
    """Demo 5: Real-world project scenario"""
    print("\n" + "="*70)
    print("DEMO 5: Real-World Scenario - Build E-Commerce Site")
    print("="*70)
    
    print("\nScenario: A startup wants to build an e-commerce platform")
    print("\n" + "-"*70)
    
    # Initialize agents
    orchestrator = MockOrchestratorAgent(name="Project Lead")
    frontend = MockFrontendAgent(name="Frontend Developer")
    backend = MockBackendAgent(name="Backend Developer")
    
    # Project planning
    print("\n[Phase 1] Project Planning & Analysis")
    plan = await orchestrator.run(
        query="Plan for an e-commerce website",
        context={
            "budget": "$50k", 
            "timeline": "3 months", 
            "team_size": 5,
            "user_requirements": {"payment_integration": True, "mobile_responsive": True}
        }
    )
    print(f"✓ Orchestrator created plan")
    
    # Frontend development
    print("\n[Phase 2] Frontend Development")
    ui = await frontend.run(
        query="Build product catalog UI with filters and cart",
    )
    print(f"✓ Frontend tasks: {len(frontend.get_history())}")
    
    # Backend development
    print("\n[Phase 3] Backend Development")
    api = await backend.run(
        query="Build REST API for products, users, and orders",
    )
    print(f"✓ Backend tasks: {len(backend.get_history())}")
    
    # Project summary
    print("\n[Phase 4] Project Summary")
    print(f"  Orchestrator: {orchestrator.get_summary()['tasks_executed']} task")
    print(f"  Frontend: {frontend.get_summary()['tasks_executed']} task")
    print(f"  Backend: {backend.get_summary()['tasks_executed']} task")
    print(f"✓ E-commerce platform ready!")


async def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("AGENTIC AI PROJECT - LIVE DEMONSTRATION")
    print("="*70)
    print("\nThis demo showcases 5 different ways to use the framework:")
    print("  1. Simple agent usage")
    print("  2. Multiple agents coordination")
    print("  3. Agent Factory pattern")
    print("  4. Task tracking & metrics")
    print("  5. Real-world scenario")
    
    # Run demos
    await demo_1_simple_agent_usage()
    await demo_2_multiple_agents()
    await demo_3_agent_factory()
    await demo_4_task_tracking()
    await demo_5_real_world_scenario()
    
    # Summary
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE!")
    print("="*70)
    print("\nKey Takeaways:")
    print("  ✓ Easy to create and manage agents")
    print("  ✓ Simple API for task execution")
    print("  ✓ Built-in tracking and metrics")
    print("  ✓ Scalable architecture")
    print("  ✓ Production-ready code")
    print("\nNext Steps:")
    print("  1. Explore src/ to understand the architecture")
    print("  2. Read docs/ for detailed documentation")
    print("  3. Check examples/ for more use cases")
    print("  4. Add your own agents by extending BaseAgent")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
