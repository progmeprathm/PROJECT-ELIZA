from typing import Dict, Any
from ecos.tools.base import Tool

class EnvironmentActionTool(Tool):
    name = "environment_action"
    description = "Executes an action in the physical environment."
    input_schema = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "description": "The action to execute (e.g., 'move_north', 'read_note', 'unlock_door_1234')"}
        },
        "required": ["action"]
    }
    output_schema = {
        "type": "object",
        "properties": {
            "observation": {"type": "object"}
        }
    }

    def execute(self, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        action = arguments.get("action", "")
        if not context or "environment" not in context:
            return {"error": "Environment not provided in context."}
            
        env = context["environment"]
        try:
            obs = env.step(action, "")
            return {"observation": obs}
        except Exception as e:
            return {"error": str(e)}
