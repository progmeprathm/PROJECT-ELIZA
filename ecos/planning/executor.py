from typing import Dict, Any, List
from ecos.planning.plan import Plan, PlanStatus, StepStatus
from ecos.planning.planner_v05 import Planner
from ecos.planning.validator import PlanValidator
from ecos.tools.registry import ToolRegistry
from ecos.world.graph import ECOSWorldModel
from ecos.memory.system import ECOSMemorySystem

class PlanExecutor:
    def __init__(self, planner: Planner, validator: PlanValidator, tool_registry: ToolRegistry, world_model: ECOSWorldModel, memory_system: ECOSMemorySystem):
        self.planner = planner
        self.validator = validator
        self.tool_registry = tool_registry
        self.world_model = world_model
        self.memory_system = memory_system
        self.context = {
            "environment": None, # Should be injected before run
            "memory_system": memory_system
        }

    def execute_plan(self, initial_plan: Plan, max_replans: int = 3) -> Plan:
        plan = initial_plan
        replan_count = 0
        
        while plan.status in (PlanStatus.CREATED, PlanStatus.ACTIVE) and replan_count <= max_replans:
            if not self.validator.validate(plan):
                plan.status = PlanStatus.FAILED
                break
                
            plan.status = PlanStatus.ACTIVE
            step = plan.get_current_step()
            
            if not step:
                plan.status = PlanStatus.COMPLETED
                plan.completion_reason = "All steps executed."
                break
                
            step.status = StepStatus.ACTIVE
            
            try:
                # Execute tool
                tool_name = step.action["tool"]
                tool_args = step.action["arguments"]
                result = self.tool_registry.execute(tool_name, tool_args, self.context)
                
                step.actual_result = result
                plan.observations.append(result)
                
                # Update World Model & Memory based on observation
                # Since tool results vary, we use heuristic to update world model if it's an environment action
                if tool_name == "environment_action" and "observation" in result:
                    obs = result["observation"]
                    self.world_model.process_observation(obs)
                    
                    episode = {
                        "type": "episode",
                        "goal": plan.goal,
                        "plan_id": plan.plan_id,
                        "step_id": step.step_id,
                        "observation": obs.get("message", ""),
                        "action": tool_args,
                        "state_before": self.world_model.get_state()
                    }
                    self.memory_system.store(f"cycle_{plan.plan_id}_{step.step_id}", episode)
                
                # Evaluate success
                if "error" in result:
                    step.status = StepStatus.FAILED
                    plan.status = PlanStatus.REPLANNING
                    plan.completion_reason = f"Step failed: {result['error']}"
                elif "observation" in result and isinstance(result["observation"], dict):
                    msg = result["observation"].get("message", "")
                    if "Incorrect" in msg or "prevents" in msg or "Unknown" in msg:
                        step.status = StepStatus.FAILED
                        plan.status = PlanStatus.REPLANNING
                        plan.completion_reason = f"Environmental failure: {msg}"
                    else:
                        step.status = StepStatus.COMPLETED
                        plan.advance_step()
                else:
                    step.status = StepStatus.COMPLETED
                    plan.advance_step()
                    
            except Exception as e:
                step.actual_result = {"error": str(e)}
                step.status = StepStatus.FAILED
                plan.status = PlanStatus.REPLANNING
                plan.completion_reason = f"Execution error: {str(e)}"
                
            if plan.status == PlanStatus.REPLANNING:
                if replan_count < max_replans:
                    replan_count += 1
                    world_state = self.world_model.get_state()
                    retrieved_mems = self.memory_system.retrieve(plan.goal, limit=3)
                    plan = self.planner.revise_plan(plan, step.actual_result, world_state, retrieved_mems)
                else:
                    plan.status = PlanStatus.FAILED
                    plan.completion_reason = "Max replans exceeded."
                    
        return plan
