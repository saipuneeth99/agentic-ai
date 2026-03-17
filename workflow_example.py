#!/usr/bin/env python3
"""
Professional Workflow System - Comprehensive Example

This example demonstrates:
1. Workflow planning and generation
2. Multi-agent orchestration
3. Dependency management
4. Metrics collection
5. Professional status reporting
"""

import asyncio
import json
from datetime import datetime

from src.framework.workflow import WorkflowManager, WorkflowStep
from src.framework.agent_factory import AgentFactory
from src.config import logger


async def main():
    """Demonstrate professional workflow system"""
    
    print("\n" + "="*80)
    print("AGENTIC AI - PROFESSIONAL WORKFLOW DEMONSTRATION")
    print("="*80 + "\n")
    
    # Initialize workflow manager and agents
    print("[1/6] Initializing Workflow Manager...")
    workflow_manager = WorkflowManager()
    
    # Create and register agents
    print("[2/6] Creating and registering specialized agents...")
    frontend_agent = AgentFactory.create_agent(
        "frontend",
        "Frontend Specialist",
        "gemini-pro"
    )
    backend_agent = AgentFactory.create_agent(
        "backend",
        "Backend Specialist",
        "gpt-4"
    )
    orchestrator_agent = AgentFactory.create_agent(
        "orchestrator",
        "Project Orchestrator",
        "claude"
    )
    
    workflow_manager.register_agent(frontend_agent)
    workflow_manager.register_agent(backend_agent)
    workflow_manager.register_agent(orchestrator_agent)
    
    print(f"   ✓ Registered {len(workflow_manager.agents)} agents")
    print()
    
    # Define workflow steps
    print("[3/6] Defining workflow steps...")
    steps = [
        WorkflowStep(
            step_id="requirements-analysis",
            description="Analyze and clarify project requirements",
            agent_type="orchestrator",
            task_query="Analyze requirements for a modern SaaS platform",
            estimated_time=300,
        ),
        WorkflowStep(
            step_id="ui-design",
            description="Design user interface and experience",
            agent_type="frontend",
            task_query="Design UI for SaaS dashboard with real-time analytics",
            dependencies=["requirements-analysis"],
            estimated_time=400,
        ),
        WorkflowStep(
            step_id="api-design",
            description="Design REST API architecture",
            agent_type="backend",
            task_query="Design scalable REST API for SaaS platform",
            dependencies=["requirements-analysis"],
            estimated_time=400,
        ),
        WorkflowStep(
            step_id="database-design",
            description="Design database schema and queries",
            agent_type="backend",
            task_query="Design PostgreSQL schema for user management and billing",
            dependencies=["api-design"],
            estimated_time=300,
        ),
        WorkflowStep(
            step_id="frontend-components",
            description="Develop reusable UI components",
            agent_type="frontend",
            task_query="Create React components for dashboard, settings, and reports",
            dependencies=["ui-design"],
            estimated_time=350,
        ),
        WorkflowStep(
            step_id="integration",
            description="Orchestrate full integration",
            agent_type="orchestrator",
            task_query="Ensure all frontend and backend components integrate seamlessly",
            dependencies=["frontend-components", "database-design"],
            estimated_time=250,
        ),
    ]
    
    print(f"   ✓ Defined {len(steps)} workflow steps")
    print()
    
    # Create workflow plan
    print("[4/6] Generating workflow plan...")
    plan = workflow_manager.create_plan(
        project_name="enterprise-saas",
        description="Complete enterprise SaaS platform with real-time features",
        steps=steps,
    )
    
    # Save plan
    plan_file = plan.save()
    print(f"   ✓ Plan saved to: {plan_file}")
    print(f"   ✓ Estimated total time: {plan.estimated_total_time}s ({plan.estimated_total_time // 60} min)")
    print()
    
    # Execute workflow
    print("[5/6] Executing workflow with parallelization...")
    print()
    
    # Get parallelization info
    pending = plan.get_next_steps()
    print(f"   Initial parallel steps: {len(pending)}")
    for step in pending:
        print(f"      - {step.step_id}: {step.description}")
    print()
    
    result = await workflow_manager.execute_plan(plan)
    
    print()
    
    # Display summary
    print("[6/6] Workflow Summary & Metrics")
    print("-" * 80)
    
    summary = workflow_manager.get_workflow_summary(plan.workflow_id)
    
    print(f"\nProject: {summary['project_name']}")
    print(f"Workflow ID: {summary['workflow_id']}")
    print(f"Status: {summary['phase']}")
    print()
    print(f"Execution Metrics:")
    print(f"  Total Steps: {summary['total_steps']}")
    print(f"  Completed: {summary['completed_steps']}")
    print(f"  Failed: {summary['failed_steps']}")
    print(f"  Success Rate: {(summary['completed_steps']/summary['total_steps']*100):.1f}%")
    print()
    print(f"Timing:")
    print(f"  Estimated: {summary['estimated_total_time']}s ({summary['estimated_total_time']//60} min)")
    print(f"  Actual: {result['execution_time']:.2f}s ({result['execution_time']/60:.2f} min)")
    print()
    
    # Show step results
    print("Step Results:")
    print("-" * 80)
    for step in plan.steps:
        status_icon = "✓" if step.status == "completed" else "✗" if step.status == "failed" else "○"
        print(f"{status_icon} {step.step_id:<25} [{step.status:<10}] {step.description}")
    
    print("\n" + "="*80)
    print("WORKFLOW EXECUTION COMPLETE")
    print("="*80 + "\n")
    
    # Show saved files
    print("Generated Artifacts:")
    print(f"  Workflow Plan: {plan_file}")
    print(f"  Logs: logs/agentic.log")
    print()
    
    # Show next steps
    print("Next Steps:")
    print("  1. Review the workflow plan: cat", plan_file)
    print("  2. Check detailed logs: tail -f logs/agentic.log")
    print("  3. Run CLI commands: python3 agentic help")
    print()
    
    print("Documentation:")
    print("  • COMMANDS.md - CLI command reference")
    print("  • WORKFLOWS.md - Workflow concepts and patterns")
    print("  • ADVANCED.md - Advanced techniques")
    print("  • ARCHITECTURE.md - System design")
    print()


if __name__ == "__main__":
    asyncio.run(main())
