"""
Learning Validator for ELIZA Cognitive Operating System.
Evaluates and validates proposed learning updates prior to persistent state mutation.
"""

from typing import Optional

from eliza.core.events import (
    EventBus,
    LearningValidated,
    LearningValidationRequested,
)
from eliza.core.interface import ILearningValidator
from eliza.core.types import SubsystemType, ValidatedLearning


class LearningValidator(ILearningValidator):
    """
    Evaluates learning updates against validation criteria (minimum threshold score, empirical proof).
    Rejects unverified learning proposals (Axiom 23).
    """

    def __init__(self, min_validation_score: float = 0.75) -> None:
        self.min_validation_score = min_validation_score
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.LEARNING

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def validate_learning(self, candidate: ValidatedLearning) -> bool:
        if self._event_bus:
            self._event_bus.publish(
                LearningValidationRequested(
                    source_subsystem="LearningValidator",
                    candidate_learning=candidate,
                )
            )

        passed = candidate.validation_score >= self.min_validation_score and len(candidate.source_experience_ids) > 0
        candidate.accepted = passed

        if self._event_bus:
            self._event_bus.publish(
                LearningValidated(
                    source_subsystem="LearningValidator",
                    validated_learning=candidate,
                    passed=passed,
                )
            )

        return passed
