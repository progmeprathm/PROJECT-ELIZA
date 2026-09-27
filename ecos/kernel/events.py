from enum import Enum
from typing import Dict, Any, List
import uuid
import time

class RuntimeEventType(str, Enum):
    ACTION_EXECUTED = "ACTION_EXECUTED"
    TASK_CREATED = "TASK_CREATED"
    OBSERVATION = "OBSERVATION"
    MEMORY_RETRIEVAL = "MEMORY_RETRIEVAL"
    PLAN_CREATED = "PLAN_CREATED"
    AGENT_ASSIGNED = "AGENT_ASSIGNED"
    TOOL_EXECUTED = "TOOL_EXECUTED"
    VERIFICATION = "VERIFICATION"
    REPLANNING = "REPLANNING"
    TASK_COMPLETED = "TASK_COMPLETED"
    LEARNING_EVENT = "LEARNING_EVENT"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    CAPABILITY_DENIED = "CAPABILITY_DENIED"
    SNAPSHOT_CREATED = "SNAPSHOT_CREATED"
    SNAPSHOT_RESTORED = "SNAPSHOT_RESTORED"

class RuntimeEvent:
    def __init__(self, event_type: RuntimeEventType, runtime_id: str, task_id: str = None, agent_id: str = None, payload: Dict[str, Any] = None, provenance: List[str] = None):
        self.event_id = f"evt-{uuid.uuid4().hex[:8]}"
        self.timestamp = time.time()
        self.type = event_type
        self.runtime_id = runtime_id
        self.task_id = task_id
        self.agent_id = agent_id
        self.payload = payload or {}
        self.provenance = provenance or []
        
    def to_dict(self):
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "type": self.type.value,
            "runtime_id": self.runtime_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "payload": self.payload,
            "provenance": self.provenance
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RuntimeEvent':
        evt = cls(
            event_type=RuntimeEventType(data["type"]),
            runtime_id=data["runtime_id"],
            task_id=data.get("task_id"),
            agent_id=data.get("agent_id"),
            payload=data.get("payload", {}),
            provenance=data.get("provenance", [])
        )
        evt.event_id = data.get("event_id", evt.event_id)
        evt.timestamp = data.get("timestamp", evt.timestamp)
        return evt
