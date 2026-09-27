from typing import Dict, Any

class AgentPerformanceTracker:
    def __init__(self):
        self.profiles: Dict[str, Dict[str, Any]] = {}
        
    def init_profile(self, agent_id: str, role: str):
        if agent_id not in self.profiles:
            self.profiles[agent_id] = {
                "agent_id": agent_id,
                "role": role,
                "success_count": 0,
                "failure_count": 0,
                "verification_accuracy": 0.0,
                "average_latency": 0.0,
                "tool_failure_rate": 0.0,
                "recovery_rate": 0.0
            }
            
    def record_success(self, agent_id: str):
        if agent_id in self.profiles:
            self.profiles[agent_id]["success_count"] += 1
            
    def record_failure(self, agent_id: str):
        if agent_id in self.profiles:
            self.profiles[agent_id]["failure_count"] += 1
