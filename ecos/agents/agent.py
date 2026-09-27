from typing import Dict, Any, List, Optional
from ecos.agents.base import BaseAgent

class AgentResult:
    def __init__(self, agent_id: str, success: bool, payload: Dict[str, Any], messages: List[Any] = None, errors: List[str] = None):
        self.agent_id = agent_id
        self.success = success
        self.payload = payload
        self.messages = messages or []
        self.errors = errors or []

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "success": self.success,
            "payload": self.payload,
            "messages": [m.to_dict() if hasattr(m, "to_dict") else m for m in self.messages],
            "errors": self.errors
        }

class Agent(BaseAgent):
    """
    Concrete implementation placeholder if we want generic agent fallback.
    Typically, we subclass this for specific roles (PlannerAgent, etc.).
    """
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        # Default implementation returning empty result
        return AgentResult(self.id, False, {}, errors=["Not implemented for base generic agent"])
