from enum import Enum
from typing import Dict, Any

class RuntimePolicyAction(str, Enum):
    EXECUTE = "EXECUTE"
    DELEGATE = "DELEGATE"
    VERIFY = "VERIFY"
    REPLAN = "REPLAN"
    RETRIEVE_MEMORY = "RETRIEVE_MEMORY"
    RETRIEVE_KNOWLEDGE = "RETRIEVE_KNOWLEDGE"
    WAIT = "WAIT"
    ABORT = "ABORT"

class MetaRuntimePolicy:
    """
    Decides the next meta-level operation for the runtime.
    """
    def __init__(self):
        self.knowledge_base = []
        
    def get_next_action(self, runtime_state: Dict[str, Any]) -> RuntimePolicyAction:
        state_str = runtime_state.get("current_state")
        failures = len(runtime_state.get("failures", []))
        
        if failures > 3:
            return RuntimePolicyAction.ABORT
            
        if state_str == "INITIALIZED":
            return RuntimePolicyAction.EXECUTE
        elif state_str == "FAILED":
            return RuntimePolicyAction.REPLAN
            
        return RuntimePolicyAction.EXECUTE
