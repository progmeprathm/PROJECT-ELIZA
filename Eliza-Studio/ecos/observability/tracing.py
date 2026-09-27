import json
from typing import List, Dict, Any

class RuntimeTrace:
    def __init__(self):
        self.events = []
        
    def add_event(self, event: Dict[str, Any]):
        self.events.append(event)
        
    def export(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump(self.events, f, indent=2)
            
    def load(self, filepath: str):
        with open(filepath, "r") as f:
            self.events = json.load(f)
