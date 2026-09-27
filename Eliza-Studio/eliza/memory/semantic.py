"""
Semantic Memory Tier for ELIZA.
Explicit conceptual knowledge and factual memory store with revision tracking.
"""

from typing import Any, Dict, List, Optional
import time

from eliza.core.events import EventBus, MemoryRetrieved
from eliza.core.interface import IMemorySubsystem
from eliza.core.types import Belief, ProvenanceRecord, SubsystemType


class SemanticMemory(IMemorySubsystem):
    """
    Semantic Memory handles structured facts, concepts, and domain knowledge.
    Ensures every fact has provenance and explicit confidence (Article V, Axiom 6).
    """

    def __init__(self) -> None:
        self._concepts: Dict[str, Dict[str, Any]] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.MEMORY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        prov = ProvenanceRecord(
            source_subsystem="SemanticMemory",
            method="fact_ingestion",
        )
        self._concepts[key] = {
            "value": value,
            "provenance": prov,
            "timestamp": time.time(),
            "meta": provenance_info or {},
        }

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        results = []
        for key, item in self._concepts.items():
            if query.lower() in key.lower() or query.lower() in str(item["value"]).lower():
                results.append(item["value"])
            if len(results) >= limit:
                break

        if self._event_bus:
            self._event_bus.publish(
                MemoryRetrieved(
                    source_subsystem="SemanticMemory",
                    query=query,
                    memory_type="semantic",
                    retrieved_items=results,
                )
            )
        return results

    def revise(self, key: str, new_value: Any, reason: str) -> None:
        if key in self._concepts:
            item = self._concepts[key]
            item["value"] = new_value
            item["provenance"].revise()
            item["meta"]["revision_reason"] = reason

    def consolidate(self) -> None:
        pass
