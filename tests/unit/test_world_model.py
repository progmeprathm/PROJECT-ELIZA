"""
Unit tests for ELIZA World Model Graph (Article VI).
"""

from eliza.core.events import EventBus
from eliza.core.types import Belief, Confidence, Entity, ProvenanceRecord, Relationship
from eliza.world_model.graph import WorldModelGraph


def test_world_model_entities_and_beliefs() -> None:
    wm = WorldModelGraph()
    bus = EventBus()
    wm.initialize(bus)

    e1 = Entity(id="entity-1", name="Agent Alpha", category="Agent")
    e2 = Entity(id="entity-2", name="Resource Beta", category="Resource")
    wm.add_entity(e1)
    wm.add_entity(e2)

    rel = Relationship(
        source_entity_id="entity-1",
        target_entity_id="entity-2",
        relation_type="CONTROLS",
        confidence=Confidence(value=0.95, source="TestSensor"),
    )
    wm.add_relationship(rel)

    b = Belief(
        id="belief-1",
        statement="Agent Alpha controls Resource Beta",
        entity_ids=["entity-1", "entity-2"],
        confidence=Confidence(value=0.95, source="TestSensor"),
        provenance=ProvenanceRecord(source_subsystem="Test", method="direct"),
    )
    wm.update_belief(b)

    assert wm.get_entity("entity-1").name == "Agent Alpha"
    assert len(wm.get_relationships_for_entity("entity-1")) == 1
    assert len(wm.query_facts("Agent Alpha")) == 1
