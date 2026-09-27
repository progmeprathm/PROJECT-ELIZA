from typing import Dict, Any, List

class VerificationResult:
    def __init__(self, passed: bool, errors: List[str] = None):
        self.passed = passed
        self.errors = errors or []

class VerificationSystem:
    """
    Independent verification module that checks plans and outcomes.
    """
    def __init__(self, tool_registry=None):
        self.tool_registry = tool_registry
        
    def verify_plan(self, plan: Dict[str, Any]) -> VerificationResult:
        errors = []
        if not plan or "steps" not in plan:
            errors.append("Plan missing steps.")
        return VerificationResult(len(errors) == 0, errors)
        
    def verify_assignment(self, assignment: Dict[str, Any]) -> VerificationResult:
        if not assignment.get("agent_id"):
            return VerificationResult(False, ["No agent assigned."])
        return VerificationResult(True)
        
    def verify_final_result(self, expected: str, actual: str) -> VerificationResult:
        if str(expected).strip().lower() != str(actual).strip().lower():
            return VerificationResult(False, [f"Result mismatch: expected {expected}, got {actual}"])
        return VerificationResult(True)
