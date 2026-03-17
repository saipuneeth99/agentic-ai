"""Workflow management system for multi-agent coordination"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from enum import Enum

from src.framework.base_agent import BaseAgent, TaskInput, TaskResult
from src.config import logger


class WorkflowPhase(Enum):
    """Workflow execution phases"""
    PLANNING = "planning"
    REVIEW = "review"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMPLETE = "complete"


class WorkflowStep:
    """Single step in a workflow"""
    
    def __init__(
        self,
        step_id: str,
        description: str,
        agent_type: str,
        task_query: str,
        dependencies: Optional[List[str]] = None,
        estimated_time: int = 300,
    ):
        self.step_id = step_id
        self.description = description
        self.agent_type = agent_type
        self.task_query = task_query
        self.dependencies = dependencies or []
        self.estimated_time = estimated_time
        self.status = "pending"
        self.result: Optional[TaskResult] = None
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "step_id": self.step_id,
            "description": self.description,
            "agent_type": self.agent_type,
            "task_query": self.task_query,
            "dependencies": self.dependencies,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "created_at": self.created_at,
        }


class WorkflowPlan:
    """Generated workflow plan"""
    
    def __init__(
        self,
        workflow_id: str,
        project_name: str,
        description: str,
        steps: List[WorkflowStep],
    ):
        self.workflow_id = workflow_id
        self.project_name = project_name
        self.description = description
        self.steps = steps
        self.phase = WorkflowPhase.PLANNING
        self.created_at = datetime.now().isoformat()
        self.estimated_total_time = sum(s.estimated_time for s in steps)

    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        """Get step by ID"""
        return next((s for s in self.steps if s.step_id == step_id), None)

    def get_next_steps(self) -> List[WorkflowStep]:
        """Get steps ready for execution"""
        return [
            s for s in self.steps
            if s.status == "pending" 
            and all(self.get_step(dep).status == "completed" for dep in s.dependencies)
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "workflow_id": self.workflow_id,
            "project_name": self.project_name,
            "description": self.description,
            "steps": [s.to_dict() for s in self.steps],
            "phase": self.phase.value,
            "created_at": self.created_at,
            "estimated_total_time": self.estimated_total_time,
        }

    def save(self, directory: str = ".workflows") -> str:
        """Save plan to file"""
        Path(directory).mkdir(exist_ok=True)
        filename = f"{directory}/{self.workflow_id}.json"
        
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        
        logger.info(f"Workflow plan saved: {filename}")
        return filename

    @classmethod
    def load(cls, filename: str) -> "WorkflowPlan":
        """Load plan from file"""
        with open(filename, "r") as f:
            data = json.load(f)
        
        steps = [
            WorkflowStep(
                step_id=s["step_id"],
                description=s["description"],
                agent_type=s["agent_type"],
                task_query=s["task_query"],
                dependencies=s.get("dependencies", []),
                estimated_time=s.get("estimated_time", 300),
            )
            for s in data["steps"]
        ]
        
        plan = cls(
            workflow_id=data["workflow_id"],
            project_name=data["project_name"],
            description=data["description"],
            steps=steps,
        )
        plan.phase = WorkflowPhase(data["phase"])
        return plan


class WorkflowManager:
    """Manages workflow execution across multiple agents"""
    
    def __init__(self, name: str = "Workflow Manager"):
        self.name = name
        self.workflows: Dict[str, WorkflowPlan] = {}
        self.agents: Dict[str, BaseAgent] = {}
        self.agents_by_role: Dict[str, BaseAgent] = {}  # Key by role for workflow execution
        self.execution_history: List[Dict[str, Any]] = []

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent for workflow use"""
        self.agents[agent.name] = agent
        self.agents_by_role[agent.role] = agent  # Also index by role
        logger.info(f"Agent registered: {agent.name}")

    def create_plan(
        self,
        project_name: str,
        description: str,
        steps: List[WorkflowStep],
    ) -> WorkflowPlan:
        """Create a new workflow plan"""
        workflow_id = f"{project_name.lower()}-{int(time.time())}"
        plan = WorkflowPlan(
            workflow_id=workflow_id,
            project_name=project_name,
            description=description,
            steps=steps,
        )
        self.workflows[workflow_id] = plan
        logger.info(f"Workflow created: {workflow_id}")
        return plan

    async def execute_plan(self, plan: WorkflowPlan) -> Dict[str, Any]:
        """Execute a workflow plan"""
        logger.info(f"Starting execution of {plan.workflow_id}")
        plan.phase = WorkflowPhase.EXECUTION
        
        results = {}
        start_time = time.time()
        
        while plan.get_next_steps():
            next_steps = plan.get_next_steps()
            
            for step in next_steps:
                # Look up agent by role
                agent = self.agents_by_role.get(step.agent_type)
                if not agent:
                    logger.error(f"No agent found for type: {step.agent_type}")
                    step.status = "failed"
                    continue
                
                logger.info(f"Executing step: {step.step_id} on {agent.name}")
                task = TaskInput(query=step.task_query)
                result = await agent.execute(task)
                
                step.result = result
                step.status = "completed" if result.status == "completed" else "failed"
                results[step.step_id] = result
        
        plan.phase = WorkflowPhase.COMPLETE
        execution_time = time.time() - start_time
        
        execution_record = {
            "workflow_id": plan.workflow_id,
            "execution_time": execution_time,
            "completed_steps": len([s for s in plan.steps if s.status == "completed"]),
            "total_steps": len(plan.steps),
            "timestamp": datetime.now().isoformat(),
        }
        self.execution_history.append(execution_record)
        
        logger.info(f"Workflow completed in {execution_time:.2f}s")
        return {
            "workflow_id": plan.workflow_id,
            "results": results,
            "execution_time": execution_time,
            "phase": plan.phase.value,
        }

    def get_workflow_summary(self, workflow_id: str) -> Dict[str, Any]:
        """Get summary of a workflow"""
        plan = self.workflows.get(workflow_id)
        if not plan:
            return {}
        
        return {
            "workflow_id": workflow_id,
            "project_name": plan.project_name,
            "phase": plan.phase.value,
            "total_steps": len(plan.steps),
            "completed_steps": len([s for s in plan.steps if s.status == "completed"]),
            "failed_steps": len([s for s in plan.steps if s.status == "failed"]),
            "estimated_total_time": plan.estimated_total_time,
        }
