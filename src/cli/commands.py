"""Professional CLI interface with workflow commands"""

import asyncio
import sys
from typing import Optional, List
from pathlib import Path
import getpass

from src.framework.workflow import WorkflowManager, WorkflowPlan, WorkflowStep
from src.framework.agent_factory import AgentFactory
from src.auth.user_manager import UserManager
from src.config import logger


class CLICommand:
    """Base class for CLI commands"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, args: List[str]) -> None:
        """Execute the command"""
        raise NotImplementedError


class WorkflowPlanCommand(CLICommand):
    """Generate workflow plan"""
    
    def __init__(self, workflow_manager: WorkflowManager):
        super().__init__("workflow:plan", "Generate a multi-phase workflow plan")
        self.workflow_manager = workflow_manager
    
    async def execute(self, args: List[str]) -> None:
        """Execute plan generation"""
        if not args:
            print("Usage: workflow:plan <project_name> <description>")
            return
        
        project_name = args[0]
        description = " ".join(args[1:]) if len(args) > 1 else "No description"
        
        # Create sample workflow steps
        steps = [
            WorkflowStep(
                step_id="frontend-design",
                description="Design UI/UX for the project",
                agent_type="frontend",
                task_query=f"Design frontend for {project_name}",
            ),
            WorkflowStep(
                step_id="backend-design",
                description="Design backend architecture and APIs",
                agent_type="backend",
                task_query=f"Design backend architecture for {project_name}",
            ),
            WorkflowStep(
                step_id="orchestration",
                description="Coordinate all components",
                agent_type="orchestrator",
                task_query=f"Orchestrate integration for {project_name}",
                dependencies=["frontend-design", "backend-design"],
            ),
        ]
        
        plan = self.workflow_manager.create_plan(
            project_name=project_name,
            description=description,
            steps=steps,
        )
        
        plan_file = plan.save()
        print(f"\n✓ Workflow plan generated")
        print(f"  Project: {project_name}")
        print(f"  Steps: {len(plan.steps)}")
        print(f"  Estimated Time: {plan.estimated_total_time}s")
        print(f"  Saved: {plan_file}\n")


class WorkflowExecuteCommand(CLICommand):
    """Execute workflow plan"""
    
    def __init__(self, workflow_manager: WorkflowManager):
        super().__init__("workflow:execute", "Execute a workflow plan")
        self.workflow_manager = workflow_manager
    
    async def execute(self, args: List[str]) -> None:
        """Execute workflow"""
        if not args:
            print("Usage: workflow:execute <workflow_id_or_file>")
            return
        
        workflow_ref = args[0]
        
        # Load plan from file if it's a path
        if workflow_ref.endswith('.json'):
            plan = WorkflowPlan.load(workflow_ref)
        else:
            plan = self.workflow_manager.workflows.get(workflow_ref)
            if not plan:
                print(f"Error: Workflow {workflow_ref} not found")
                return
        
        # Register agents if not already done
        if not self.workflow_manager.agents:
            frontend = AgentFactory.create_agent("frontend", "UI Designer", "gemini-1.5-pro")
            backend = AgentFactory.create_agent("backend", "API Developer", "gpt-3.5-turbo")
            orchestrator = AgentFactory.create_agent("orchestrator", "Orchestrator", "claude")
            
            self.workflow_manager.register_agent(frontend)
            self.workflow_manager.register_agent(backend)
            self.workflow_manager.register_agent(orchestrator)
        
        result = await self.workflow_manager.execute_plan(plan)
        
        print(f"\n✓ Workflow execution complete")
        print(f"  Execution Time: {result['execution_time']:.2f}s")
        print(f"  Phase: {result['phase']}")
        print(f"  Results: {len(result['results'])} tasks\n")


class WorkflowStatusCommand(CLICommand):
    """Show workflow status"""
    
    def __init__(self, workflow_manager: WorkflowManager):
        super().__init__("workflow:status", "Show workflow status and metrics")
        self.workflow_manager = workflow_manager
    
    async def execute(self, args: List[str]) -> None:
        """Show status"""
        print("\n" + "="*70)
        print("WORKFLOW STATUS & METRICS")
        print("="*70)
        
        for workflow_id, plan in self.workflow_manager.workflows.items():
            summary = self.workflow_manager.get_workflow_summary(workflow_id)
            print(f"\n{plan.project_name} ({workflow_id})")
            print(f"  Phase: {summary['phase']}")
            print(f"  Progress: {summary['completed_steps']}/{summary['total_steps']}")
            print(f"  Failed: {summary['failed_steps']}")
            print(f"  Est. Time: {summary['estimated_total_time']}s")
        
        if not self.workflow_manager.workflows:
            print("\nNo active workflows")
        
        print("\n" + "="*70 + "\n")


class AuthLoginCommand(CLICommand):
    """User login command"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__("auth:login", "Login to your account")
        self.user_manager = user_manager
    
    async def execute(self, args: List[str]) -> None:
        """Execute login"""
        if args and len(args) >= 1:
            username = args[0]
        else:
            username = input("Username: ").strip()
        
        if not username:
            print("Error: Username required")
            return
        
        password = getpass.getpass("Password: ")
        
        result = self.user_manager.login(username, password)
        
        if result["success"]:
            print(f"\n✓ {result['message']}\n")
        else:
            print(f"\n✗ {result['error']}\n")


class AuthRegisterCommand(CLICommand):
    """User registration command"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__("auth:register", "Create a new account")
        self.user_manager = user_manager
    
    async def execute(self, args: List[str]) -> None:
        """Execute registration"""
        print("\n" + "="*70)
        print("CREATE NEW ACCOUNT")
        print("="*70 + "\n")
        
        username = input("Username (min 3 chars): ").strip()
        email = input("Email (optional): ").strip()
        
        password = getpass.getpass("Password (min 6 chars): ")
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print("\n✗ Passwords don't match\n")
            return
        
        result = self.user_manager.register(username, password, email)
        
        if result["success"]:
            print(f"\n✓ {result['message']}\n")
        else:
            print(f"\n✗ {result['error']}\n")


class AuthLogoutCommand(CLICommand):
    """User logout command"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__("auth:logout", "Logout from your account")
        self.user_manager = user_manager
    
    async def execute(self, args: List[str]) -> None:
        """Execute logout"""
        result = self.user_manager.logout()
        
        if result["success"]:
            print(f"\n✓ {result['message']}\n")
        else:
            print(f"\n✗ {result['error']}\n")


class AuthProfileCommand(CLICommand):
    """Show user profile"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__("auth:profile", "View your profile and API keys")
        self.user_manager = user_manager
    
    async def execute(self, args: List[str]) -> None:
        """Show profile"""
        profile = self.user_manager.get_user_profile()
        
        if not profile:
            print("\n✗ Not logged in\n")
            return
        
        print("\n" + "="*70)
        print(f"USER PROFILE - {profile['username']}")
        print("="*70)
        print(f"\nUsername: {profile['username']}")
        print(f"Email: {profile['email'] or 'Not set'}")
        print(f"Created: {profile['created_at'][:10]}")
        
        print(f"\nAPI Keys:")
        for provider, status in profile['api_keys_configured'].items():
            print(f"  {provider.capitalize()}: {status}")
        
        print(f"\nSettings:")
        for key, value in profile['settings'].items():
            print(f"  {key}: {value}")
        
        print("\n" + "="*70 + "\n")


class AuthAddKeyCommand(CLICommand):
    """Add API key"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__("auth:add-key", "Add or update API key")
        self.user_manager = user_manager
    
    async def execute(self, args: List[str]) -> None:
        """Add API key"""
        if not self.user_manager.get_current_user():
            print("\n✗ Not logged in. Use 'auth:login' first.\n")
            return
        
        if args and len(args) >= 1:
            provider = args[0].lower()
        else:
            provider = input("Provider (google/openai/anthropic): ").lower().strip()
        
        if provider not in ["google", "openai", "anthropic"]:
            print(f"\n✗ Unknown provider: {provider}\n")
            return
        
        api_key = getpass.getpass(f"Enter your {provider.upper()} API key: ")
        
        if not api_key.strip():
            print("\n✗ API key cannot be empty\n")
            return
        
        result = self.user_manager.add_api_key(provider, api_key)
        
        if result["success"]:
            print(f"\n✓ {result['message']}\n")
        else:
            print(f"\n✗ {result['error']}\n")


class HelpCommand(CLICommand):
    """Show help message"""
    
    def __init__(self, commands: dict):
        super().__init__("help", "Show available commands")
        self.commands = commands
    
    async def execute(self, args: List[str]) -> None:
        """Show help"""
        print("\n" + "="*70)
        print("AGENTIC AI - Professional Workflow System")
        print("="*70)
        
        print("\nAuthentication Commands:")
        for cmd_name, cmd in self.commands.items():
            if "auth" in cmd_name:
                print(f"  {cmd_name:<20} {cmd.description}")
        
        print("\nWorkflow Commands:")
        for cmd_name, cmd in self.commands.items():
            if "workflow" in cmd_name:
                print(f"  {cmd_name:<20} {cmd.description}")
        
        print("\nUtility Commands:")
        for cmd_name, cmd in self.commands.items():
            if "workflow" not in cmd_name and "auth" not in cmd_name:
                print(f"  {cmd_name:<20} {cmd.description}")
        
        print("\n" + "="*70 + "\n")
        
        # Show current user if logged in
        if hasattr(self, 'user_manager') and self.user_manager.get_current_user():
            print(f"Logged in as: {self.user_manager.get_current_user()}\n")


class CLIInterface:
    """Professional CLI interface"""
    
    def __init__(self):
        self.workflow_manager = WorkflowManager()
        self.user_manager = UserManager()
        self.commands = self._init_commands()
    
    def _init_commands(self) -> dict:
        """Initialize all commands"""
        commands = {
            # Authentication commands
            "auth:login": AuthLoginCommand(self.user_manager),
            "auth:register": AuthRegisterCommand(self.user_manager),
            "auth:logout": AuthLogoutCommand(self.user_manager),
            "auth:profile": AuthProfileCommand(self.user_manager),
            "auth:add-key": AuthAddKeyCommand(self.user_manager),
            
            # Workflow commands
            "workflow:plan": WorkflowPlanCommand(self.workflow_manager),
            "workflow:execute": WorkflowExecuteCommand(self.workflow_manager),
            "workflow:status": WorkflowStatusCommand(self.workflow_manager),
            
            # Help - will be added after
            "help": None,
        }
        
        # Create help command with all commands
        help_cmd = HelpCommand(commands)
        commands["help"] = help_cmd
        
        return commands
    
    async def run(self, command: str, args: Optional[List[str]] = None) -> None:
        """Run a command"""
        args = args or []
        
        if not command:
            await self.commands["help"].execute([])
            return
        
        cmd_obj = self.commands.get(command)
        if not cmd_obj:
            print(f"Error: Unknown command '{command}'")
            print(f"Use 'help' to see available commands")
            return
        
        try:
            await cmd_obj.execute(args)
        except Exception as e:
            logger.error(f"Command failed: {str(e)}")
            print(f"Error: {str(e)}")


async def main():
    """Main CLI entrypoint"""
    cli = CLIInterface()
    cli.commands["help"].commands = cli.commands
    
    if len(sys.argv) < 2:
        await cli.run("help")
        return
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    await cli.run(command, args)


if __name__ == "__main__":
    asyncio.run(main())
