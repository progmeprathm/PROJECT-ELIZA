"""
Meta-Cognition Subsystem for ELIZA.
Enforces Axiom 17 & 18: Hierarchical, recursive self-evaluation of plans, knowledge, and confidence.
"""

from typing import List, Optional

from eliza.core.events import EventBus, MetaCognitionEvaluated
from eliza.core.interface import IMetaCognition
from eliza.core.types import (
    Belief,
    Confidence,
    MetaCognitiveState,
    Plan,
    SubsystemType,
)


class MetaCognitiveEvaluator(IMetaCognition):
    """
    Evaluates ELIZA's own internal cognitive state recursively.
    Identifies knowledge gaps, assesses plan self-confidence, and suggests strategic adjustments.
    """

    def __init__(self) -> None:
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.EXECUTIVE

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def evaluate_cognition(self, plan: Plan, beliefs: List[Belief]) -> MetaCognitiveState:
        gaps: List[str] = []

        if not beliefs:
            gaps.append("Zero background beliefs available in World Model.")

        low_conf_beliefs = [b for b in beliefs if b.confidence.value < 0.60]
        if low_conf_beliefs:
            gaps.append(f"{len(low_conf_beliefs)} beliefs carry confidence under 0.60.")

        plan_confidence_score = max(0.10, 1.0 - plan.estimated_risk - (len(gaps) * 0.15))

        adjustment: Optional[str] = None
        if plan_confidence_score < 0.50:
            adjustment = "Gather more empirical observations before executing action."

        meta_state = MetaCognitiveState(
            target_plan_id=plan.id,
            self_confidence=Confidence(value=round(plan_confidence_score, 4), source="MetaCognitiveEvaluator"),
            perceived_knowledge_gaps=gaps,
            recommended_strategy_adjustment=adjustment,
        )

        if self._event_bus:
            self._event_bus.publish(
                MetaCognitionEvaluated(
                    source_subsystem="MetaCognitiveEvaluator",
                    meta_state=meta_state,
                )
            )

        return meta_state
