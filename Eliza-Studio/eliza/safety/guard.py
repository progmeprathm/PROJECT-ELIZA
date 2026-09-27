"""
Safety Guard for ELIZA Cognitive Operating System.
Independent policy evaluation engine with absolute veto power over proposed actions.
"""

from typing import Any, Dict, List, Optional

from eliza.core.events import EventBus
from eliza.core.interface import ISafetyGuard
from eliza.core.types import Action, RiskAssessment, SubsystemType


class SafetyGuard(ISafetyGuard):
    """
    Safety Guard evaluates actions against immutable safety rules, policy constraints, and risk thresholds.
    Can veto any action regardless of executive priority or cognitive capability (Article XII, Axiom 8).
    """

    def __init__(self, max_risk_threshold: float = 0.70) -> None:
        self.max_risk_threshold = max_risk_threshold
        self._forbidden_actions: List[str] = [
            "BYPASS_SAFETY",
            "DELETE_HISTORICAL_LOGS",
            "UNRESTRICTED_SYSTEM_EXEC",
        ]
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.SAFETY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def add_forbidden_action(self, action_type: str) -> None:
        self._forbidden_actions.append(action_type)

    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> RiskAssessment:
        violations: List[str] = []
        vetoed = False
        reason = "Action approved by Safety Guard"

        # Check explicit forbidden action list
        if action.action_type in self._forbidden_actions:
            violations.append(f"Forbidden action type '{action.action_type}' violates core safety policy.")
            vetoed = True

        # Check risk score from parameters if present
        risk_score = float(action.parameters.get("estimated_risk", 0.10))
        if risk_score > self.max_risk_threshold:
            violations.append(f"Action risk score ({risk_score}) exceeds maximum threshold ({self.max_risk_threshold}).")
            vetoed = True

        # Check safety clearance flag
        if action.requires_safety_clearance and vetoed:
            reason = f"VETOED by SafetyGuard: {'; '.join(violations)}"
        elif vetoed:
            reason = f"VETOED: {'; '.join(violations)}"

        return RiskAssessment(
            action_id=action.id,
            risk_score=risk_score,
            policy_violations=violations,
            compliant=not vetoed,
            vetoed=vetoed,
            reason=reason,
        )
