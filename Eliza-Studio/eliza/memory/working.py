"""
Working Memory Tier for ELIZA.
Bounded capacity active context buffer.
"""

from typing import Any, Dict, List, Optional
import time

from eliza.core.events import EventBus, MemoryRetrieved
from eliza.core.interface import IMemorySubsystem
from eliza.core.types import ProvenanceRecord, SubsystemType


class WorkingMemory(IMemorySubsystem):
    """
    Working Memory maintains the active cognitive workspace for current operations.
    Capacity is explicitly bounded to maintain focus and prevent memory bloat.
    """

    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self._buffer: Dict[str, Dict[str, Any]] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.MEMORY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        if len(self._buffer) >= self.capacity:
            # Evict oldest entry
            oldest_key = min(self._buffer.keys(), key=lambda k: self._buffer[k]["timestamp"])
            del self._buffer[oldest_key]

        prov = ProvenanceRecord(
            source_subsystem="WorkingMemory",
            method="direct_store",
        )
        self._buffer[key] = {
            "value": value,
            "timestamp": time.time(),
            "provenance": prov,
            "meta": provenance_info or {},
        }

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        results = []
        for key, item in self._buffer.items():
            if query.lower() in key.lower() or query.lower() in str(item["value"]).lower():
                results.append(item["value"])
            if len(results) >= limit:
                break

        if self._event_bus:
            self._event_bus.publish(
                MemoryRetrieved(
                    source_subsystem="WorkingMemory",
                    query=query,
                    memory_type="working",
                    retrieved_items=results,
                )
            )
        return results

    def revise(self, key: str, new_value: Any, reason: str) -> None:
        if key in self._buffer:
            item = self._buffer[key]
            item["value"] = new_value
            item["provenance"].revise()
            item["meta"]["revision_reason"] = reason

    def consolidate(self) -> None:
        """Working memory does not consolidate directly; hands off to ShortTerm / LongTerm."""
        pass

    def clear(self) -> None:
        self._buffer.clear()
