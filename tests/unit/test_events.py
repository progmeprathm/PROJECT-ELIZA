"""
Unit tests for ELIZA Canonical Event System (Article XIV).
"""

from eliza.core.events import (
    BeliefUpdated,
    CognitiveEvent,
    EventBus,
    ObservationReceived,
)
from eliza.core.types import Belief, Confidence, ProvenanceRecord


def test_event_bus_publish_subscribe() -> None:
    bus = EventBus()
    received_events = []

    def handler(event: ObservationReceived) -> None:
        received_events.append(event)

    bus.subscribe(ObservationReceived, handler)

    obs = ObservationReceived(source_subsystem="TestPerception", raw_input="Hello world")
    bus.publish(obs)

    assert len(received_events) == 1
    assert received_events[0].raw_input == "Hello world"
    assert len(bus.get_history()) == 1


def test_generic_event_subscription() -> None:
    bus = EventBus()
    all_events = []

    def generic_handler(event: CognitiveEvent) -> None:
        all_events.append(event)

    bus.subscribe(CognitiveEvent, generic_handler)

    obs = ObservationReceived(source_subsystem="TestPerception", raw_input="Stimulus A")
    bus.publish(obs)

    assert len(all_events) == 1
    assert all_events[0].name == "ObservationReceived"
