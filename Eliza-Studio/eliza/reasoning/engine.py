"""
Reasoning Engine for ELIZA Cognitive Operating System.
Evaluates beliefs and derives inferences across multiple reasoning styles without state mutation.
"""

from typing import List, Optional
import uuid

from eliza.core.events import EventBus
from eliza.core.interface import IReasoningEngine
from eliza.core.types import (
    Belief,
    Confidence,
    ProvenanceRecord,
    ReasoningStyle,
    SubsystemType,
)


class ReasoningEngine(IReasoningEngine):
    """
    Reasoning Engine evaluates structured beliefs and produces derived inferences.
    Never modifies reality directly.
    """

    def __init__(self) -> None:
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.REASONING

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def reason(
        self,
        beliefs: List[Belief],
        style: ReasoningStyle = ReasoningStyle.DEDUCTIVE,
        target_hypothesis: Optional[str] = None,
    ) -> List[Belief]:
        """
        Evaluate given input beliefs under the specified reasoning style.
        Returns newly inferred Belief objects with calculated confidence and provenance.
        """
        inferred_beliefs: List[Belief] = []

        if style == ReasoningStyle.DEDUCTIVE:
            inferred_beliefs = self._reason_deductive(beliefs, target_hypothesis)
        elif style == ReasoningStyle.INDUCTIVE:
            inferred_beliefs = self._reason_inductive(beliefs, target_hypothesis)
        elif style == ReasoningStyle.ABDUCTIVE:
            inferred_beliefs = self._reason_abductive(beliefs, target_hypothesis)
        elif style == ReasoningStyle.COUNTERFACTUAL:
            inferred_beliefs = self._reason_counterfactual(beliefs, target_hypothesis)
        elif style == ReasoningStyle.ANALOGICAL:
            inferred_beliefs = self._reason_analogical(beliefs, target_hypothesis)
        elif style == ReasoningStyle.PROBABILISTIC:
            inferred_beliefs = self._reason_probabilistic(beliefs, target_hypothesis)

        return inferred_beliefs

    def _reason_deductive(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Deductive reasoning: derives logical conclusions from premises with high confidence."""
        if not beliefs:
            return []
        
        # Combine evidence and calculate premise confidence
        combined_confidence = min(b.confidence.value for b in beliefs) if beliefs else 0.5
        evidence_ids = [b.id for b in beliefs]
        statement = target_hypothesis or f"Deductive inference derived from {len(beliefs)} premises"

        derived_belief = Belief(
            id=f"belief-ded-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=combined_confidence, source="ReasoningEngine:Deductive"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="deductive_inference", evidence_ids=evidence_ids),
            uncertainty=1.0 - combined_confidence,
            evidence=evidence_ids,
        )
        return [derived_belief]

    def _reason_inductive(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Inductive reasoning: generalizes from specific observations."""
        evidence_ids = [b.id for b in beliefs]
        avg_confidence = (sum(b.confidence.value for b in beliefs) / len(beliefs)) * 0.85 if beliefs else 0.5
        statement = target_hypothesis or f"Inductive pattern generalized from {len(beliefs)} observations"

        derived_belief = Belief(
            id=f"belief-ind-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=avg_confidence, source="ReasoningEngine:Inductive"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="inductive_generalization", evidence_ids=evidence_ids),
            uncertainty=1.0 - avg_confidence,
            evidence=evidence_ids,
        )
        return [derived_belief]

    def _reason_abductive(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Abductive reasoning: proposes plausible explanations for observations."""
        evidence_ids = [b.id for b in beliefs]
        est_confidence = 0.70  # Abductive inferences carry moderate confidence
        statement = target_hypothesis or f"Abductive best-explanation for {len(beliefs)} evidence items"

        derived_belief = Belief(
            id=f"belief-abd-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=est_confidence, source="ReasoningEngine:Abductive"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="abductive_explanation", evidence_ids=evidence_ids),
            uncertainty=0.30,
            evidence=evidence_ids,
        )
        return [derived_belief]

    def _reason_counterfactual(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Counterfactual reasoning: evaluates 'What if premise P were false?'."""
        evidence_ids = [b.id for b in beliefs]
        statement = target_hypothesis or "Counterfactual state hypothesis"

        derived_belief = Belief(
            id=f"belief-cf-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=0.60, source="ReasoningEngine:Counterfactual"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="counterfactual_evaluation", evidence_ids=evidence_ids),
            uncertainty=0.40,
            evidence=evidence_ids,
        )
        return [derived_belief]

    def _reason_analogical(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Analogical reasoning: maps structure from reference domain to target domain."""
        evidence_ids = [b.id for b in beliefs]
        statement = target_hypothesis or "Analogical domain mapping"

        derived_belief = Belief(
            id=f"belief-ana-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=0.65, source="ReasoningEngine:Analogical"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="analogical_mapping", evidence_ids=evidence_ids),
            uncertainty=0.35,
            evidence=evidence_ids,
        )
        return [derived_belief]

    def _reason_probabilistic(self, beliefs: List[Belief], target_hypothesis: Optional[str]) -> List[Belief]:
        """Probabilistic reasoning: Bayesian updating over belief confidence."""
        if not beliefs:
            return []
        
        prior = 0.5
        for b in beliefs:
            # Simple Bayesian likelihood update
            likelihood = b.confidence.value
            prior = (prior * likelihood) / ((prior * likelihood) + ((1 - prior) * (1 - likelihood) + 1e-6))

        evidence_ids = [b.id for b in beliefs]
        statement = target_hypothesis or f"Probabilistic posterior state ({prior:.2f})"

        derived_belief = Belief(
            id=f"belief-prob-inf-{uuid.uuid4().hex[:8]}",
            statement=statement,
            entity_ids=list({e for b in beliefs for e in b.entity_ids}),
            confidence=Confidence(value=round(prior, 4), source="ReasoningEngine:Probabilistic"),
            provenance=ProvenanceRecord(source_subsystem="ReasoningEngine", method="bayesian_update", evidence_ids=evidence_ids),
            uncertainty=round(1.0 - prior, 4),
            evidence=evidence_ids,
        )
        return [derived_belief]
