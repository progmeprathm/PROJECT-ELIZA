from typing import Dict, Any
from ecos.tools.base import Tool

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluates simple arithmetic expressions."
    input_schema = {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Arithmetic expression to evaluate (e.g., '17 * 8')"}
        },
        "required": ["expression"]
    }
    output_schema = {
        "type": "object",
        "properties": {
            "result": {"type": "number"}
        }
    }

    def execute(self, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        expr = arguments.get("expression", "")
        # Very simple and safe parsing instead of eval
        allowed_chars = "0123456789+-*/. ()"
        if not all(c in allowed_chars for c in expr):
            return {"error": "Invalid characters in expression."}
        try:
            # Using compile to be slightly safer than raw eval, with strict boundaries
            code = compile(expr, "<string>", "eval")
            for name in code.co_names:
                return {"error": f"Invalid name in expression: {name}"}
            result = eval(code, {"__builtins__": {}}, {})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
