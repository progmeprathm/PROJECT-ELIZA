from typing import Dict, Any, List
from ecos.agents.agent import Agent, AgentResult
from ecos.agents.roles import AgentRole
from ecos.agents.message import Message, MessageType

class PlannerAgent(Agent):
    """
    Responsible for task decomposition, dependency identification, plan creation, and plan revision.
    """
    def __init__(self, agent_id: str, router, context_budget: int = 4000):
        super().__init__(agent_id, AgentRole.PLANNER, ["decompose_task", "create_plan"], router, None, context_budget)
        
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        # Uses self.router to create plans
        # Placeholder for actual LLM call
        goal = task_context.get("task_goal", "")
        plan = {"steps": [{"id": "1", "desc": f"Execute {goal}"}]}
        return AgentResult(self.id, True, {"plan": plan})

class ResearchAgent(Agent):
    """
    Responsible for information gathering, memory retrieval, environment inspection, and evidence collection.
    """
    def __init__(self, agent_id: str, router, tool_registry, context_budget: int = 4000):
        super().__init__(agent_id, AgentRole.RESEARCHER, ["search_memory", "inspect_environment"], router, tool_registry, context_budget)
        
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        # Uses self.tool_registry to gather info
        return AgentResult(self.id, True, {"evidence": "Gathered data."})

class ExecutorAgent(Agent):
    """
    Responsible for executing validated actions, invoking tools, and interacting with the environment.
    """
    def __init__(self, agent_id: str, router, tool_registry, context_budget: int = 4000):
        super().__init__(agent_id, AgentRole.EXECUTOR, ["execute_action", "invoke_tool"], router, tool_registry, context_budget)
        
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        return AgentResult(self.id, True, {"result": "Action executed."})

class VerificationAgent(Agent):
    """
    Responsible for checking plans, checking intermediate results, detecting inconsistencies, and identifying failed assumptions.
    """
    def __init__(self, agent_id: str, router, context_budget: int = 4000):
        super().__init__(agent_id, AgentRole.VERIFIER, ["verify_plan", "check_results"], router, None, context_budget)
        
    def run(self, task_context: Dict[str, Any]) -> AgentResult:
        return AgentResult(self.id, True, {"verified": True})
