from enum import Enum
from typing import List, Dict, Any, Optional
import uuid

class StepStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    INVALIDATED = "INVALIDATED"

class PlanStatus(str, Enum):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REPLANNING = "REPLANNING"
    ABORTED = "ABORTED"

class PlanStep:
    def __init__(self, step_id: str, description: str, action: Dict[str, Any], expected_result: str, dependencies: List[str] = None):
        self.step_id = step_id
        self.description = description
        self.action = action  # e.g., {"tool": "calculator", "arguments": {"expression": "1+1"}}
        self.expected_result = expected_result
        self.dependencies = dependencies or []
        self.status = StepStatus.PENDING
        self.actual_result = None

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "description": self.description,
            "action": self.action,
            "expected_result": self.expected_result,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "actual_result": self.actual_result
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        step = cls(
            step_id=data["step_id"],
            description=data["description"],
            action=data["action"],
            expected_result=data["expected_result"],
            dependencies=data.get("dependencies", [])
        )
        step.status = StepStatus(data["status"])
        step.actual_result = data.get("actual_result")
        return step

class Plan:
    def __init__(self, goal: str, assumptions: List[str], steps: List[PlanStep]):
        self.plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        self.goal = goal
        self.assumptions = assumptions
        self.steps = steps
        self.current_step = 0
        self.status = PlanStatus.CREATED
        self.observations = []
        self.replanning_history = []
        self.completion_reason = ""

    def get_current_step(self) -> Optional[PlanStep]:
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def advance_step(self):
        if self.current_step < len(self.steps):
            self.current_step += 1

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "assumptions": self.assumptions,
            "steps": [s.to_dict() for s in self.steps],
            "current_step": self.current_step,
            "status": self.status.value,
            "observations": self.observations,
            "replanning_history": self.replanning_history,
            "completion_reason": self.completion_reason
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        plan = cls(
            goal=data["goal"],
            assumptions=data["assumptions"],
            steps=[PlanStep.from_dict(s) for s in data["steps"]]
        )
        plan.plan_id = data.get("plan_id", plan.plan_id)
        plan.current_step = data.get("current_step", 0)
        plan.status = PlanStatus(data.get("status", "CREATED"))
        plan.observations = data.get("observations", [])
        plan.replanning_history = data.get("replanning_history", [])
        plan.completion_reason = data.get("completion_reason", "")
        return plan
