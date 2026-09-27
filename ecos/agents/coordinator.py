from typing import Dict, Any, List
from ecos.agents.agent import Agent, AgentResult
from ecos.agents.roles import AgentRole
from ecos.agents.workspace import CognitiveWorkspace
from ecos.agents.registry import AgentRegistry

from llms.router import ModelRouter

class CoordinatorAgent(Agent):
    """
    Responsible for task decomposition, agent selection, delegation, aggregation, conflict resolution, final decision, and escalation.
    """
    def __init__(self, agent_id: str, router: ModelRouter, registry: AgentRegistry, context_budget: int = 8000) -> None:
        super().__init__(agent_id, AgentRole.COORDINATOR, ["delegate", "aggregate", "resolve"], router, None, context_budget)
        self.registry = registry
        
    def run(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        self._emit("AgentStateChanged", {"previous": "IDLE", "current": "EXECUTING"})
        self._emit("AgentTaskStarted", {"task_context": "workspace_evaluation"})
        workspace = task_context.get("workspace")
        if not isinstance(workspace, CognitiveWorkspace):
            self._emit("AgentTaskCompleted", {"success": False})
            self._emit("AgentStateChanged", {"previous": "EXECUTING", "current": "IDLE"})
            return AgentResult(self.id, False, {}, errors=["Missing CognitiveWorkspace in context."]).to_dict()
            
        # Example Coordinator Loop (simplified):
        # 1. Ask Planner to decompose
        planner = next((a for a in self.registry.list_agents() if a.role == AgentRole.PLANNER), None)
        if planner:
            self._emit("TaskDelegated", {"to_agent": planner.id, "task": "decompose_goal"})
            plan_res = planner.run({"task_goal": workspace.task_goal})
            if plan_res.get("success"):
                workspace.candidate_solutions.append(plan_res.get("payload", {}).get("plan"))
                self._emit("GoalTreeUpdated", {"new_plans": len(workspace.candidate_solutions)})
                
        # 2. Ask Verifier to check
        verifier = next((a for a in self.registry.list_agents() if a.role == AgentRole.VERIFIER), None)
        if verifier:
            self._emit("TaskDelegated", {"to_agent": verifier.id, "task": "verify_plan"})
            self._emit("VerificationStarted", {"plan_index": -1})
            verify_res = verifier.run({"plan": workspace.candidate_solutions[-1]})
            workspace.verification_results.append(verify_res.get("payload", {}))
            self._emit("VerificationCompleted", {"success": verify_res.get("success")})
            
        self._emit("CoordinationCompleted", {"workspace_summary": workspace.get_summary()})
        self._emit("AgentTaskCompleted", {"success": True})
        self._emit("AgentStateChanged", {"previous": "EXECUTING", "current": "IDLE"})
        return AgentResult(self.id, True, {"status": "Coordination complete", "workspace_summary": workspace.get_summary()}).to_dict()
