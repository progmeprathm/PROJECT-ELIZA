from typing import Dict, Any, List
import uuid

class DelegationPolicy:
    FIXED = "FIXED"
    CAPABILITY = "CAPABILITY"
    ADAPTIVE = "ADAPTIVE"

class DynamicDelegator:
    def __init__(self, registry, performance_profiles=None):
        self.registry = registry
        self.performance_profiles = performance_profiles or {}
        self.decision_records = []
        
    def delegate(self, task_id: str, subtask_id: str, required_capabilities: List[str], policy: str, max_agents: int = 1) -> List[str]:
        candidates = []
        for agent in self.registry.list_agents():
            if all(cap in agent.capabilities for cap in required_capabilities):
                candidates.append(agent)
                
        if not candidates:
            return []
            
        selected = []
        if policy == DelegationPolicy.ADAPTIVE:
            # Sort by performance success_rate if adaptive
            candidates.sort(key=lambda a: self._get_success_rate(a.id), reverse=True)
            # Take top max_agents
            selected = [c.id for c in candidates[:max_agents]]
        elif policy == DelegationPolicy.CAPABILITY:
            # Just take the first valid ones
            selected = [c.id for c in candidates[:max_agents]]
        elif policy == DelegationPolicy.FIXED:
            # Take exactly one matching the first capability's implicit role (mock logic)
            selected = [candidates[0].id]
            
        self.decision_records.append({
            "task_id": task_id,
            "subtask_id": subtask_id,
            "candidate_agents": [c.id for c in candidates],
            "selected_agent": selected,
            "required_capabilities": required_capabilities,
            "policy": policy
        })
        
        return selected
        
    def _get_success_rate(self, agent_id: str) -> float:
        profile = self.performance_profiles.get(agent_id, {})
        s = profile.get("success_count", 0)
        f = profile.get("failure_count", 0)
        if s + f == 0:
            return 0.5
        return s / (s + f)
