from typing import Dict, Any, List
import uuid
import time
from ecos.agents.lifecycle import AgentState, TaskState
from ecos.agents.registry import AgentRegistry
from ecos.agents.workspace import CognitiveWorkspace

class AgentRuntime:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.events: List[Dict[str, Any]] = []
        self.agent_states: Dict[str, AgentState] = {agent.id: AgentState.AVAILABLE for agent in registry.list_agents()}
        
    def _emit(self, event_type: str, task_id: str, agent_id: str = None, payload: Dict[str, Any] = None):
        event = {
            "event_id": f"evt-{uuid.uuid4().hex[:8]}",
            "timestamp": time.time(),
            "event_type": event_type,
            "task_id": task_id,
            "agent_id": agent_id,
            "payload": payload or {},
            "provenance": []
        }
        self.events.append(event)
        
    def set_agent_state(self, agent_id: str, state: AgentState, task_id: str = None):
        old_state = self.agent_states.get(agent_id, AgentState.CREATED)
        self.agent_states[agent_id] = state
        self._emit("AGENT_STATE_CHANGE", task_id, agent_id, {"from": old_state.value, "to": state.value})

    def run_task(self, task_goal: str, coordinator_id: str, context: Dict[str, Any] = None) -> CognitiveWorkspace:
        workspace = CognitiveWorkspace(task_goal)
        task_id = workspace.workspace_id
        
        self._emit("TASK_CREATED", task_id)
        
        coordinator = self.registry.get(coordinator_id)
        if not coordinator:
            self._emit("TASK_FAILED", task_id, payload={"error": "Coordinator not found"})
            return workspace
            
        self.set_agent_state(coordinator.id, AgentState.ASSIGNED, task_id)
        self.set_agent_state(coordinator.id, AgentState.RUNNING, task_id)
        
        # In a real async loop, this would step through states.
        # We simulate the synchronous task orchestration here.
        task_context = {"workspace": workspace, "runtime": self}
        if context:
            task_context.update(context)
            
        result = coordinator.run(task_context)
        
        if result.success:
            self.set_agent_state(coordinator.id, AgentState.COMPLETED, task_id)
            self._emit("TASK_COMPLETED", task_id, payload={"final_result": workspace.final_result})
        else:
            self.set_agent_state(coordinator.id, AgentState.FAILED, task_id)
            self._emit("TASK_FAILED", task_id, payload={"errors": result.errors})
            
        return workspace

    def execute_agent(self, agent_id: str, task_context: Dict[str, Any]) -> Any:
        agent = self.registry.get(agent_id)
        task_id = task_context["workspace"].workspace_id
        
        self.set_agent_state(agent_id, AgentState.RUNNING, task_id)
        self._emit("AGENT_STARTED", task_id, agent_id)
        
        try:
            res = agent.run(task_context)
            if res.success:
                self.set_agent_state(agent_id, AgentState.COMPLETED, task_id)
                self._emit("AGENT_COMPLETED", task_id, agent_id, {"payload": res.payload})
            else:
                self.set_agent_state(agent_id, AgentState.FAILED, task_id)
                self._emit("AGENT_FAILED", task_id, agent_id, {"errors": res.errors})
            return res
        except Exception as e:
            self.set_agent_state(agent_id, AgentState.FAILED, task_id)
            self._emit("AGENT_FAILED", task_id, agent_id, {"errors": [str(e)]})
            return None
