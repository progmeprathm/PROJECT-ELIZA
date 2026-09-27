"""
Short-Term Memory Tier for ELIZA.
Transient memory buffer with decay and consolidation triggers.
"""

from typing import Any, Dict, List, Optional
import time

from eliza.core.events import EventBus, MemoryRetrieved
from eliza.core.interface import IMemorySubsystem
from eliza.core.types import ProvenanceRecord, SubsystemType


class ShortTermMemory(IMemorySubsystem):
    """
    Short-Term Memory stores recent experiences with timestamps and decay factors.
    Supports consolidation into Long-Term/Episodic Memory.
    """

    def __init__(self, ttl_seconds: float = 3600.0) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.MEMORY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        prov = ProvenanceRecord(
            source_subsystem="ShortTermMemory",
            method="temporal_intake",
        )
        self._store[key] = {
            "value": value,
            "timestamp": time.time(),
            "provenance": prov,
            "access_count": 0,
            "meta": provenance_info or {},
        }

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        self.purge_expired()
        results = []
        for key, item in self._store.items():
            if query.lower() in key.lower() or query.lower() in str(item["value"]).lower():
                item["access_count"] += 1
                results.append(item["value"])
            if len(results) >= limit:
                break

        if self._event_bus:
            self._event_bus.publish(
                MemoryRetrieved(
                    source_subsystem="ShortTermMemory",
                    query=query,
                    memory_type="short_term",
                    retrieved_items=results,
                )
            )
        return results

    def revise(self, key: str, new_value: Any, reason: str) -> None:
        if key in self._store:
            item = self._store[key]
            item["value"] = new_value
            item["provenance"].revise()
            item["meta"]["revision_reason"] = reason

    def purge_expired(self) -> None:
        now = time.time()
        expired = [k for k, v in self._store.items() if (now - v["timestamp"]) > self.ttl_seconds]
        for k in expired:
            del self._store[k]

    def consolidate(self) -> None:
        """Purge stale unreferenced items."""
        self.purge_expired()
