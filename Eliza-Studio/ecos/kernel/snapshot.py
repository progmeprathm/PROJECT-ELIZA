import os
import json
from typing import Dict, Any
from ecos.kernel.state import RuntimeState

class RuntimeSnapshot:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        
    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Strip secrets if any
        safe_data = {k: v for k, v in self.data.items() if "secret" not in k and "key" not in k}
        with open(filepath, "w") as f:
            json.dump(safe_data, f, indent=2)
            
    @classmethod
    def load(cls, filepath: str) -> 'RuntimeSnapshot':
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(data)
