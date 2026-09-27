from typing import Dict, Any, List
from ecos.agents.agent import Agent, AgentResult
from ecos.agents.roles import AgentRole
from ecos.agents.workspace import CognitiveWorkspace
from ecos.agents.registry import AgentRegistry

class CoordinatorAgent(Agent):
    """
    Responsible for task decomposition, agent selection, delegation, aggregation, conflict resolution, final decision, and escalation.
    """
    def __init__(self, agent_id: str, router, registry: AgentRegistry, context_budget: int = 8000):
        super().__init__(agent_id, AgentRole.COORDINATOR, ["delegate", "aggregate", "resolve"], router, None, context_budget)
        self.registry = registry
        
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        workspace = task_context.get("workspace")
        if not isinstance(workspace, CognitiveWorkspace):
            return AgentResult(self.id, False, {}, errors=["Missing CognitiveWorkspace in context."])
            
        # Example Coordinator Loop (simplified):
        # 1. Ask Planner to decompose
        planner = next((a for a in self.registry.list_agents() if a.role == AgentRole.PLANNER), None)
        if planner:
            plan_res = planner.run({"task_goal": workspace.task_goal})
            if plan_res.success:
                workspace.candidate_solutions.append(plan_res.payload.get("plan"))
                
        # 2. Ask Verifier to check
        verifier = next((a for a in self.registry.list_agents() if a.role == AgentRole.VERIFIER), None)
        if verifier:
            verify_res = verifier.run({"plan": workspace.candidate_solutions[-1]})
            workspace.verification_results.append(verify_res.payload)
            
        return AgentResult(self.id, True, {"status": "Coordination complete", "workspace_summary": workspace.get_summary()})
