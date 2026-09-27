from typing import Dict, Any, Optional
from ecos.agents.roles import AgentRole
from ecos.agents.context import AgentContext
from llms.router import ModelRouter
from ecos.tools.registry import ToolRegistry

class BaseAgent:
    """
    Base abstraction for any agent in the E.L.I.Z.A. multi-agent cognitive runtime.
    """
    def __init__(
        self, 
        agent_id: str, 
        role: AgentRole, 
        capabilities: list[str],
        router: ModelRouter,
        tool_registry: Optional[ToolRegistry] = None,
        context_budget: int = 4000
    ):
        self.id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.router = router
        self.tool_registry = tool_registry
        self.context_budget = context_budget
        self.local_context = AgentContext(self.id)
        
    def run(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's core loop for a given task context.
        Returns an AgentResult dictionary.
        """
        raise NotImplementedError("Agents must implement the run() method.")
