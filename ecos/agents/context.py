from typing import Dict, Any, List

class AgentContext:
    """
    Private local context for an agent, independent from the global shared workspace or world model.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.working_memory: List[Dict[str, Any]] = []
        self.local_retrieved_memories: List[Any] = []
        self.local_hypotheses: List[str] = []
        self.temporary_plans: List[Any] = []
        
    def add_to_working_memory(self, item: Dict[str, Any]):
        self.working_memory.append(item)
        # Cap working memory if context budget is tight
        if len(self.working_memory) > 10:
            self.working_memory.pop(0)
            
    def get_summary(self) -> Dict[str, Any]:
        return {
            "working_memory": self.working_memory,
            "local_retrieved_memories": self.local_retrieved_memories,
            "local_hypotheses": self.local_hypotheses
        }
