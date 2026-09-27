from typing import Any, Dict, Generator, List, Optional
from llms.base import LanguageModel

class MockAdapter(LanguageModel):
    """Deterministic Mock Adapter for tests and offline development."""
    def __init__(self, model_name: str = "mock-model") -> None:
        super().__init__(model_name)
        self.api_key = "dummy"

    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        if self.api_key == "":
            raise ValueError(f"Missing API key for mock provider '{self.model_name}'")
        if "Create a multi-step plan" in prompt:
            if "previous plan failed" in prompt or "recently altered" in prompt:
                # Replan
                return {
                    "assumptions": ["Multiplier changed"],
                    "steps": [
                        {"description": "Calculate new code", "action": {"tool": "calculator", "arguments": {"expression": "12 * 5"}}, "expected_result": "60"},
                        {"description": "Unlock Door", "action": {"tool": "environment_action", "arguments": {"action": "unlock_door_60"}}, "expected_result": "Door unlocked"},
                        {"description": "Move east to Goal", "action": {"tool": "environment_action", "arguments": {"action": "move_east"}}, "expected_result": "At goal"}
                    ]
                }
            return {
                "assumptions": ["Goal is reachable"],
                "steps": [
                    {"description": "Move east to Room A", "action": {"tool": "environment_action", "arguments": {"action": "move_east"}}, "expected_result": "In Room A"},
                    {"description": "Read note", "action": {"tool": "environment_action", "arguments": {"action": "read_note"}}, "expected_result": "Got base code"},
                    {"description": "Move east to Room B", "action": {"tool": "environment_action", "arguments": {"action": "move_east"}}, "expected_result": "In Room B"},
                    {"description": "Read wall", "action": {"tool": "environment_action", "arguments": {"action": "read_wall"}}, "expected_result": "Got multiplier"},
                    {"description": "Calculate code", "action": {"tool": "calculator", "arguments": {"expression": "12 * 4"}}, "expected_result": "48"},
                    {"description": "Move east to Door", "action": {"tool": "environment_action", "arguments": {"action": "move_east"}}, "expected_result": "At door"},
                    {"description": "Unlock Door", "action": {"tool": "environment_action", "arguments": {"action": "unlock_door_48"}}, "expected_result": "Door unlocked"},
                    {"description": "Move east to Goal", "action": {"tool": "environment_action", "arguments": {"action": "move_east"}}, "expected_result": "At goal"}
                ]
            }

        # Deterministic logic for v0.3 Memory Relevance Experiment (1D)
        action = "move_forward"
        if "'agent_location': 1" in prompt and "password_discovered" not in prompt and "8592" not in prompt:
            action = "read_note"
        elif "'agent_location': 3" in prompt:
            if "'door_locked': True" in prompt and "'door_locked': False" not in prompt:
                if "8592" in prompt:
                    action = "unlock_door_8592"
                else:
                    action = "move_backward"
            else:
                action = "move_forward"
                
        # Deterministic logic for v0.4 2D Environment
        if "(0, 0)" in prompt:
            action = "move_east"
        elif "(1, 0)" in prompt:
            action = "move_north"
        elif "(1, 1)" in prompt and "8592" not in prompt:
            action = "read_note"
        elif "(1, 1)" in prompt and "8592" in prompt:
            action = "move_east"
        elif "(2, 1)" in prompt:
            action = "move_north"
        elif "(2, 2)" in prompt:
            if "'door_locked': True" in prompt and "'door_locked': False" not in prompt:
                if "8592" in prompt:
                    action = "unlock_door_8592"
                else:
                    action = "move_west"
            else:
                action = "move_east"
        elif "(3, 2)" in prompt:
            action = "move_north"
            
        # Deterministic logic for v0.5 Planning World Reactive Baseline
        if "'agent_location': 0" in prompt:
            action = "move_east"
        elif "'agent_location': 1" in prompt:
            if "base code is 12" not in prompt:
                action = "read_note"
            else:
                action = "move_east"
        elif "'agent_location': 2" in prompt:
            if "multiplier is 4" not in prompt and "multiplier is 5" not in prompt:
                action = "read_wall"
            else:
                action = "move_east"
        elif "'agent_location': 3" in prompt:
            if "'door_locked': True" in prompt:
                if "48" in prompt or ("12" in prompt and "4" in prompt):
                    action = "unlock_door_48"
                elif "60" in prompt or ("12" in prompt and "5" in prompt):
                    action = "unlock_door_60"
                else:
                    action = "move_west"
            else:
                action = "move_east"
            
        return {
            "model": self.model_name,
            "provider": "mock",
            "action": action,
            "reasoning": "Deterministic mock logic."
        }

    def embed(self, text: str) -> List[float]:
        return [0.1] * 10

    def tokenize(self, text: str) -> List[int]:
        return [1, 2, 3]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        yield "Mock stream"
