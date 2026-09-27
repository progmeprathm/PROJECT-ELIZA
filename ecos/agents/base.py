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
        context_budget: int = 4000,
        event_bus: Optional[Any] = None,
        runtime_id: str = "sys"
    ):
        self.id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.router = router
        self.tool_registry = tool_registry
        self.context_budget = context_budget
        self.local_context = AgentContext(self.id)
        self.event_bus = event_bus
        self.runtime_id = runtime_id
        
        self._emit("AgentCreated", {"role": self.role.value, "capabilities": self.capabilities})
        
    def _emit(self, event_type: str, payload: Dict[str, Any]):
        if self.event_bus:
            from eliza.kernel.events import Event, EventType
            self.event_bus.emit(Event(
                event_type=EventType(event_type),
                runtime_id=self.runtime_id,
                agent_id=self.id,
                source=self.__class__.__name__,
                payload=payload
            ))

    def run(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's core loop for a given task context.
        Returns an AgentResult dictionary.
        """
        raise NotImplementedError("Agents must implement the run() method.")
