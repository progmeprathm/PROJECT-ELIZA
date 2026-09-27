"""
Explainability Tracer for ELIZA.
Maintains structured decision provenance and explanation records.
"""

from typing import Dict, Optional

from eliza.core.events import EventBus
from eliza.core.interface import IExplainabilityTracer
from eliza.core.types import Explanation, SubsystemType


class ExplainabilityTracer(IExplainabilityTracer):
    """
    Traces and records explanations for all cognitive decisions in ELIZA.
    Ensures every decision is fully inspectable.
    """

    def __init__(self) -> None:
        self._explanations: Dict[str, Explanation] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.EXPLAINABILITY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def record_decision(self, explanation: Explanation) -> None:
        self._explanations[explanation.decision_id] = explanation

    def get_explanation(self, decision_id: str) -> Optional[Explanation]:
        return self._explanations.get(decision_id)

    def format_explanation_summary(self, decision_id: str) -> str:
        exp = self.get_explanation(decision_id)
        if not exp:
            return f"No explanation record found for decision ID '{decision_id}'."

        lines = [
            f"=== Cognitive Decision Explanation [{exp.decision_id}] ===",
            f"Why: {exp.why}",
            f"Confidence: {exp.confidence.value:.2f} (Source: {exp.confidence.source})",
            f"Evidence: {', '.join(exp.evidence) if exp.evidence else 'None'}",
            f"Beliefs Used: {', '.join(exp.beliefs_used) if exp.beliefs_used else 'None'}",
            f"Assumptions: {', '.join(exp.assumptions) if exp.assumptions else 'None'}",
            f"Alternatives Considered: {', '.join(exp.alternatives_considered) if exp.alternatives_considered else 'None'}",
        ]
        return "\n".join(lines)
