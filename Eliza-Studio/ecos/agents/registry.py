from typing import Dict, List, Optional
from ecos.agents.base import BaseAgent
from ecos.agents.roles import AgentRole

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        
    def register(self, agent: BaseAgent):
        if agent.id in self._agents:
            raise ValueError(f"Agent with ID {agent.id} already registered.")
        self._agents[agent.id] = agent
        
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        return self._agents.get(agent_id)
        
    def find_by_role(self, role: AgentRole) -> List[BaseAgent]:
        return [agent for agent in self._agents.values() if agent.role == role]
        
    def list_agents(self) -> List[BaseAgent]:
        return list(self._agents.values())
