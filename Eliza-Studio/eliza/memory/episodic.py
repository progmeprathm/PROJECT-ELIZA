"""
Episodic Memory Tier for ELIZA.
Temporal record of cognitive experiences, events, and historical traces.
"""

from typing import Any, Dict, List, Optional
import time

from eliza.core.events import CognitiveEvent, EventBus, MemoryRetrieved
from eliza.core.interface import IMemorySubsystem
from eliza.core.types import ProvenanceRecord, SubsystemType


class EpisodicMemory(IMemorySubsystem):
    """
    Episodic Memory stores past episodes (sequences of events and actions).
    Provides temporal indexing and historical query capabilities.
    """

    def __init__(self) -> None:
        self._episodes: List[Dict[str, Any]] = []
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.MEMORY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        prov = ProvenanceRecord(
            source_subsystem="EpisodicMemory",
            method="episode_logging",
        )
        self._episodes.append({
            "key": key,
            "value": value,
            "provenance": prov,
            "timestamp": time.time(),
            "meta": provenance_info or {},
        })

    def record_event(self, event: CognitiveEvent) -> None:
        self.store(key=event.event_id, value=event, provenance_info={"event_type": event.name})

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        results = []
        for ep in reversed(self._episodes):
            if query.lower() in ep["key"].lower() or query.lower() in str(ep["value"]).lower():
                results.append(ep["value"])
            if len(results) >= limit:
                break

        if self._event_bus:
            self._event_bus.publish(
                MemoryRetrieved(
                    source_subsystem="EpisodicMemory",
                    query=query,
                    memory_type="episodic",
                    retrieved_items=results,
                )
            )
        return results

    def revise(self, key: str, new_value: Any, reason: str) -> None:
        """Episodic history is append-only by canon (Article X: Learning does not rewrite history)."""
        raise NotImplementedError("Episodic memory history cannot be rewritten; append a revision episode instead.")

    def consolidate(self) -> None:
        pass
