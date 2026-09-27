from typing import Dict, Any, List

class RuntimeState:
    def __init__(self, runtime_id: str):
        self.runtime_id = runtime_id
        self.task_id = None
        self.current_state = "INITIALIZED"
        
        self.world_model_state = {}
        self.active_plan = None
        self.workspace = None
        
        self.active_agents = []
        self.memory_context = {}
        self.knowledge_context = {}
        
        self.pending_actions = []
        self.failures = []
        
        self.verification_state = {}
        self.learning_state = {}
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "runtime_id": self.runtime_id,
            "task_id": self.task_id,
            "current_state": self.current_state,
            "world_model_state": self.world_model_state,
            "active_plan": self.active_plan,
            "workspace": self.workspace,
            "active_agents": self.active_agents,
            "memory_context": self.memory_context,
            "knowledge_context": self.knowledge_context,
            "pending_actions": self.pending_actions,
            "failures": self.failures,
            "verification_state": self.verification_state,
            "learning_state": self.learning_state
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RuntimeState':
        st = cls(data["runtime_id"])
        st.task_id = data.get("task_id")
        st.current_state = data.get("current_state", "INITIALIZED")
        st.world_model_state = data.get("world_model_state", {})
        st.active_plan = data.get("active_plan")
        st.workspace = data.get("workspace")
        st.active_agents = data.get("active_agents", [])
        st.memory_context = data.get("memory_context", {})
        st.knowledge_context = data.get("knowledge_context", {})
        st.pending_actions = data.get("pending_actions", [])
        st.failures = data.get("failures", [])
        st.verification_state = data.get("verification_state", {})
        st.learning_state = data.get("learning_state", {})
        return st
