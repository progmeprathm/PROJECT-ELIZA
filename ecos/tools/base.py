from typing import Dict, Any

class Tool:
    name: str = ""
    description: str = ""
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}

    def execute(self, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        raise NotImplementedError
