"""
World Model Graph for ELIZA Cognitive Operating System.
Structured representation of reality containing entities, relationships, beliefs, and causal links.
"""

from typing import Dict, List, Optional
import logging

from eliza.core.events import BeliefUpdated, EventBus
from eliza.core.interface import IWorldModel
from eliza.core.types import Belief, Entity, Relationship, SubsystemType

logger = logging.getLogger(__name__)


class WorldModelGraph(IWorldModel):
    """
    Canonical Knowledge Graph representing ELIZA's state of reality.
    Holds Entities, Relationships, and Beliefs with confidence and uncertainty metrics.
    """

    def __init__(self) -> None:
        self._entities: Dict[str, Entity] = {}
        self._relationships: List[Relationship] = []
        self._beliefs: Dict[str, Belief] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.WORLD_MODEL

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def add_entity(self, entity: Entity) -> None:
        self._entities[entity.id] = entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def add_relationship(self, relationship: Relationship) -> None:
        # Check entities exist
        if relationship.source_entity_id not in self._entities:
            logger.warning(f"Source entity {relationship.source_entity_id} not found in WorldModel")
        if relationship.target_entity_id not in self._entities:
            logger.warning(f"Target entity {relationship.target_entity_id} not found in WorldModel")
        self._relationships.append(relationship)

    def update_belief(self, belief: Belief) -> None:
        prev = self._beliefs.get(belief.id)
        self._beliefs[belief.id] = belief

        if self._event_bus:
            prev_dict = {"statement": prev.statement, "confidence": prev.confidence.value} if prev else None
            self._event_bus.publish(
                BeliefUpdated(
                    source_subsystem="WorldModel",
                    belief=belief,
                    previous_state=prev_dict,
                )
            )

    def get_belief(self, belief_id: str) -> Optional[Belief]:
        return self._beliefs.get(belief_id)

    def query_facts(self, query_str: str) -> List[Belief]:
        """Query beliefs matching the search phrase."""
        results = []
        for b in self._beliefs.values():
            if query_str.lower() in b.statement.lower():
                results.append(b)
        return results

    def get_all_beliefs(self) -> List[Belief]:
        return list(self._beliefs.values())

    def get_relationships_for_entity(self, entity_id: str) -> List[Relationship]:
        return [
            r for r in self._relationships
            if r.source_entity_id == entity_id or r.target_entity_id == entity_id
        ]
