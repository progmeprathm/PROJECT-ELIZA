from ecos.planning.plan import Plan, PlanStatus

class PlanValidator:
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry

    def validate(self, plan: Plan) -> bool:
        if not plan.steps:
            plan.completion_reason = "PLAN_VALIDATION_ERROR: No steps."
            plan.status = PlanStatus.FAILED
            return False
            
        step_ids = set()
        for step in plan.steps:
            if not step.step_id:
                plan.completion_reason = "PLAN_VALIDATION_ERROR: Missing step_id."
                plan.status = PlanStatus.FAILED
                return False
            if step.step_id in step_ids:
                plan.completion_reason = f"PLAN_VALIDATION_ERROR: Duplicate step_id {step.step_id}."
                plan.status = PlanStatus.FAILED
                return False
            step_ids.add(step.step_id)
            
            # Validate action and tool schema
            action = step.action
            if not action or "tool" not in action or "arguments" not in action:
                plan.completion_reason = f"PLAN_VALIDATION_ERROR: Invalid action format in step {step.step_id}."
                plan.status = PlanStatus.FAILED
                return False
                
            tool = self.tool_registry.get(action["tool"])
            if not tool:
                plan.completion_reason = f"PLAN_VALIDATION_ERROR: Tool '{action['tool']}' does not exist."
                plan.status = PlanStatus.FAILED
                return False
                
            # Basic argument validation
            for arg_key in tool.input_schema.get("required", []):
                if arg_key not in action["arguments"]:
                    plan.completion_reason = f"PLAN_VALIDATION_ERROR: Missing required argument '{arg_key}' for tool '{tool.name}'."
                    plan.status = PlanStatus.FAILED
                    return False
                    
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    plan.completion_reason = f"PLAN_VALIDATION_ERROR: Unknown dependency '{dep}' in step {step.step_id}."
                    plan.status = PlanStatus.FAILED
                    return False
                    
        return True
