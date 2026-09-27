import uuid
import time
from typing import Dict, Any, List

from ecos.kernel.state import RuntimeState
from ecos.kernel.events import RuntimeEvent, RuntimeEventType
from ecos.kernel.lifecycle import RuntimeLifecycleState
from ecos.kernel.snapshot import RuntimeSnapshot
from ecos.kernel.interfaces import IRuntime
from ecos.kernel.policy import MetaRuntimePolicy, RuntimePolicyAction

class ELIZARuntime(IRuntime):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.runtime_id = f"rt-{uuid.uuid4().hex[:8]}"
        self.state = RuntimeState(self.runtime_id)
        self.events: List[RuntimeEvent] = []
        self.policy = MetaRuntimePolicy()
        
        self.budget = {
            "max_model_calls": config.get("max_model_calls", 100),
            "max_tool_calls": config.get("max_tool_calls", 100),
            "max_replans": config.get("max_replans", 5),
            "max_runtime_seconds": config.get("max_runtime_seconds", 300)
        }
        self.usage = {
            "model_calls": 0,
            "tool_calls": 0,
            "replans": 0,
            "start_time": time.time()
        }
        
    def _emit(self, event_type: RuntimeEventType, payload: Dict[str, Any] = None):
        evt = RuntimeEvent(event_type, self.runtime_id, self.state.task_id, payload=payload)
        self.events.append(evt)
        return evt

    def check_budget(self) -> bool:
        if self.usage["model_calls"] >= self.budget["max_model_calls"]:
            self._emit(RuntimeEventType.BUDGET_EXCEEDED, {"reason": "max_model_calls"})
            return False
        if self.usage["tool_calls"] >= self.budget["max_tool_calls"]:
            self._emit(RuntimeEventType.BUDGET_EXCEEDED, {"reason": "max_tool_calls"})
            return False
        if self.usage["replans"] >= self.budget["max_replans"]:
            self._emit(RuntimeEventType.BUDGET_EXCEEDED, {"reason": "max_replans"})
            return False
        if time.time() - self.usage["start_time"] >= self.budget["max_runtime_seconds"]:
            self._emit(RuntimeEventType.BUDGET_EXCEEDED, {"reason": "max_runtime_seconds"})
            return False
        return True

    def run(self, task: str) -> Any:
        self.state.task_id = f"task-{uuid.uuid4().hex[:8]}"
        self.state.current_state = RuntimeLifecycleState.RUNNING.value
        self._emit(RuntimeEventType.TASK_CREATED, {"task": task})
        
        while self.state.current_state == RuntimeLifecycleState.RUNNING.value:
            if not self.check_budget():
                self.state.current_state = RuntimeLifecycleState.FAILED.value
                break
                
            action = self.policy.get_next_action(self.state.to_dict())
            
            if action == RuntimePolicyAction.EXECUTE:
                # Mock execution loop
                self.usage["model_calls"] += 1
                self.state.current_state = RuntimeLifecycleState.COMPLETED.value
            elif action == RuntimePolicyAction.ABORT:
                self.state.current_state = RuntimeLifecycleState.ABORTED.value
            else:
                self.state.current_state = RuntimeLifecycleState.COMPLETED.value
                
        self._emit(RuntimeEventType.TASK_COMPLETED, {"final_state": self.state.current_state})
        return self.state.current_state

    def observe(self, observation: str):
        self._emit(RuntimeEventType.OBSERVATION, {"observation": observation})

    def step(self):
        pass

    def pause(self):
        self.state.current_state = RuntimeLifecycleState.PAUSED.value

    def resume(self):
        self.state.current_state = RuntimeLifecycleState.RUNNING.value

    def snapshot(self) -> RuntimeSnapshot:
        snap = RuntimeSnapshot({
            "state": self.state.to_dict(),
            "usage": self.usage,
            "events": [e.to_dict() for e in self.events]
        })
        self._emit(RuntimeEventType.SNAPSHOT_CREATED)
        return snap

    def restore(self, snapshot: RuntimeSnapshot):
        self.state = RuntimeState.from_dict(snapshot.data["state"])
        self.usage = snapshot.data["usage"]
        self.events = [RuntimeEvent.from_dict(e) for e in snapshot.data["events"]]
        self._emit(RuntimeEventType.SNAPSHOT_RESTORED)

    def export_trace(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.events]
