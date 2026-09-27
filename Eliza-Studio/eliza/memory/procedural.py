"""
Procedural Memory Tier for ELIZA.
Storage for skills, procedures, subroutines, and cognitive strategies.
"""

from typing import Any, Callable, Dict, List, Optional
import time

from eliza.core.events import EventBus, MemoryRetrieved
from eliza.core.interface import IMemorySubsystem
from eliza.core.types import ProvenanceRecord, SubsystemType


class ProceduralMemory(IMemorySubsystem):
    """
    Procedural Memory manages actionable skills, workflows, and executable routines.
    """

    def __init__(self) -> None:
        self._procedures: Dict[str, Dict[str, Any]] = {}
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.MEMORY

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        prov = ProvenanceRecord(
            source_subsystem="ProceduralMemory",
            method="procedure_registration",
        )
        self._procedures[key] = {
            "value": value,
            "provenance": prov,
            "timestamp": time.time(),
            "meta": provenance_info or {},
        }

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        results = []
        for name, item in self._procedures.items():
            if query.lower() in name.lower() or query.lower() in str(item["meta"]).lower():
                results.append(item["value"])
            if len(results) >= limit:
                break

        if self._event_bus:
            self._event_bus.publish(
                MemoryRetrieved(
                    source_subsystem="ProceduralMemory",
                    query=query,
                    memory_type="procedural",
                    retrieved_items=results,
                )
            )
        return results

    def revise(self, key: str, new_value: Any, reason: str) -> None:
        if key in self._procedures:
            item = self._procedures[key]
            item["value"] = new_value
            item["provenance"].revise()
            item["meta"]["revision_reason"] = reason

    def consolidate(self) -> None:
        pass
