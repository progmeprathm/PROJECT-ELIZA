from typing import Dict, Any, List
from ecos.tools.base import Tool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return [{
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema,
            "output_schema": t.output_schema
        } for t in self._tools.values()]

    def execute(self, name: str, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found.")
        return tool.execute(arguments, context)
