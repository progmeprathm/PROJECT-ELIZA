from typing import Dict, Any, List
import json
from ecos.planning.plan import Plan, PlanStep, PlanStatus
from llms.router import ModelRouter, TaskIntent
from ecos.tools.registry import ToolRegistry

class Planner:
    def __init__(self, router: ModelRouter, tool_registry: ToolRegistry):
        self.router = router
        self.tool_registry = tool_registry

    def create_plan(self, goal: str, world_state: Dict[str, Any], memory: List[Any]) -> Plan:
        tools_schema = json.dumps(self.tool_registry.get_tool_schemas(), indent=2)
        prompt = (
            f"GOAL: {goal}\n"
            f"[WORLD_MODEL] CURRENT STATE: {world_state}\n"
            f"[MEMORY] RETRIEVED EXPERIENCES: {memory}\n"
            f"Available Tools:\n{tools_schema}\n\n"
            "Create a multi-step plan to achieve the goal using the available tools."
        )
        schema = {
            "type": "object",
            "properties": {
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "action": {
                                "type": "object",
                                "properties": {
                                    "tool": {"type": "string"},
                                    "arguments": {"type": "object"}
                                },
                                "required": ["tool", "arguments"]
                            },
                            "expected_result": {"type": "string"}
                        },
                        "required": ["description", "action", "expected_result"]
                    }
                }
            },
            "required": ["assumptions", "steps"]
        }

        try:
            result = self.router.route_task(TaskIntent.REASONING, prompt, schema=schema)
            if "steps" not in result:
                return self._create_fallback_plan(goal)
                
            steps = []
            for i, step_data in enumerate(result["steps"]):
                step_id = f"step-{i+1}"
                steps.append(PlanStep(
                    step_id=step_id,
                    description=step_data.get("description", ""),
                    action=step_data.get("action", {}),
                    expected_result=step_data.get("expected_result", ""),
                    dependencies=[f"step-{i}"] if i > 0 else []
                ))
            return Plan(goal, result.get("assumptions", []), steps)
            
        except Exception as e:
            plan = self._create_fallback_plan(goal)
            plan.completion_reason = f"Planner Error: {str(e)}"
            plan.status = PlanStatus.FAILED
            return plan

    def revise_plan(self, plan: Plan, observation: Dict[str, Any], world_state: Dict[str, Any], memory: List[Any]) -> Plan:
        context_goal = f"{plan.goal}\n\nNote: The previous plan failed. Failure observation: {observation}"
        new_plan = self.create_plan(context_goal, world_state, memory)
        new_plan.replanning_history.append(plan.to_dict())
        return new_plan

    def _create_fallback_plan(self, goal: str) -> Plan:
        return Plan(goal, [], [])
