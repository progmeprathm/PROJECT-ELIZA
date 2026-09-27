from typing import Dict, Any
from ecos.tools.base import Tool

class MemorySearchTool(Tool):
    name = "memory_search"
    description = "Retrieves information from episodic memory using a semantic query."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query to retrieve past experiences"}
        },
        "required": ["query"]
    }
    output_schema = {
        "type": "object",
        "properties": {
            "results": {"type": "array", "items": {"type": "string"}}
        }
    }

    def execute(self, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        query = arguments.get("query", "")
        if not context or "memory_system" not in context:
            return {"error": "Memory system not provided in context."}
            
        mem_sys = context["memory_system"]
        # Limit to 3 matches
        results = mem_sys.retrieve(query, limit=3)
        return {"results": [r.get("observation", str(r)) for r in results if isinstance(r, dict)]}
