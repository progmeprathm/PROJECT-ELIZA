"""
Unit tests for ELIZA Reasoning Engine (Article VII).
"""

from eliza.core.types import Belief, Confidence, ProvenanceRecord, ReasoningStyle
from eliza.reasoning.engine import ReasoningEngine


def test_deductive_reasoning() -> None:
    engine = ReasoningEngine()

    b1 = Belief(
        id="b1",
        statement="All systems are operating within nominal parameters",
        entity_ids=["sys1"],
        confidence=Confidence(value=0.90, source="Sensors"),
        provenance=ProvenanceRecord(source_subsystem="Sensors", method="direct"),
    )
    b2 = Belief(
        id="b2",
        statement="System1 is an active system",
        entity_ids=["sys1"],
        confidence=Confidence(value=0.95, source="Sensors"),
        provenance=ProvenanceRecord(source_subsystem="Sensors", method="direct"),
    )

    inferred = engine.reason(
        beliefs=[b1, b2],
        style=ReasoningStyle.DEDUCTIVE,
        target_hypothesis="System1 is nominal",
    )

    assert len(inferred) == 1
    assert inferred[0].confidence.value == 0.90
    assert "System1 is nominal" in inferred[0].statement
