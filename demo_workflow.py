#!/usr/bin/env python3
"""Quick demo of the multi-agent workflow system"""

import asyncio
from src.framework import AgentFactory, TaskInput
from tests.mock_agents import MockFrontendAgent, MockBackendAgent, MockOrchestratorAgent

async def demo():
    print("\n" + "="*70)
    print("DEMO: Multi-Agent Workflow System")
    print("="*70)
    
    # Create mock agents
    frontend = MockFrontendAgent(name="UI Designer")
    backend = MockBackendAgent(name="API Developer")
    orchestrator = MockOrchestratorAgent(name="Orchestrator")
    
    print("\n[Phase 1] Frontend Agent - Design UI for Landing Page")
    print("-" * 70)
    frontend_result = await frontend.run(
        query="Design a landing page for an AI startup",
        context={"brand": "Agentic AI", "color_scheme": "blue-white"}
    )
    print(f"Status: {frontend_result.status}")
    print(f"Execution Time: {frontend_result.execution_time:.4f}s")
    print(f"Output: {str(frontend_result.result)[:200]}...")
    
    print("\n[Phase 2] Backend Agent - Develop API & Database")
    print("-" * 70)
    backend_result = await backend.run(
        query="Create REST API for user authentication",
        context={"frontend_design": frontend_result.result}
    )
    print(f"Status: {backend_result.status}")
    print(f"Execution Time: {backend_result.execution_time:.4f}s")
    print(f"Output: {str(backend_result.result)[:200]}...")
    
    print("\n[Phase 3] Orchestrator - Integrate Components")
    print("-" * 70)
    integration_result = await orchestrator.run(
        query="Integrate frontend and backend components",
        context={
            "frontend_design": frontend_result.result,
            "backend_api": backend_result.result
        }
    )
    print(f"Status: {integration_result.status}")
    print(f"Execution Time: {integration_result.execution_time:.4f}s")
    print(f"Output: {str(integration_result.result)[:200]}...")
    
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)
    print(f"Total Agents Used: 3")
    total_time = frontend_result.execution_time + backend_result.execution_time + integration_result.execution_time
    print(f"Total Execution Time: {total_time:.4f}s")
    print("\nResult Summary:")
    print(f"  ✓ Frontend Design: {frontend_result.status}")
    print(f"  ✓ Backend API: {backend_result.status}")
    print(f"  ✓ Integration: {integration_result.status}")

if __name__ == "__main__":
    asyncio.run(demo())
