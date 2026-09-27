"""
Perception Module for ELIZA.
Translates external raw input into structured ObservationReceived events.
"""

from typing import Any, Dict, Optional

from eliza.core.events import EventBus, ObservationReceived
from eliza.core.interface import ICognitiveSubsystem
from eliza.core.types import SubsystemType


class PerceptionModule(ICognitiveSubsystem):
    """
    Perception Module converts raw environment inputs into structured ObservationReceived events.
    """

    def __init__(self) -> None:
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.PERCEPTION

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def ingest_input(self, raw_input: str, metadata: Optional[Dict[str, Any]] = None) -> ObservationReceived:
        obs = ObservationReceived(
            source_subsystem="PerceptionModule",
            payload=metadata or {},
            raw_input=raw_input,
        )
        if self._event_bus:
            self._event_bus.publish(obs)
        return obs
