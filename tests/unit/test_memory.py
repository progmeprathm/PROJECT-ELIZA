"""
Unit tests for ELIZA 6-Tier Memory Subsystems (Article V).
"""

import pytest

from eliza.core.events import EventBus
from eliza.memory import (
    EpisodicMemory,
    LongTermMemory,
    ProceduralMemory,
    SemanticMemory,
    ShortTermMemory,
    WorkingMemory,
)


def test_working_memory_bounded_capacity() -> None:
    wm = WorkingMemory(capacity=2)
    wm.store("k1", "v1")
    wm.store("k2", "v2")
    wm.store("k3", "v3")

    results = wm.retrieve("k1")
    assert len(results) == 0  # Evicted

    results3 = wm.retrieve("k3")
    assert len(results3) == 1
    assert results3[0] == "v3"


def test_semantic_memory_revision() -> None:
    sm = SemanticMemory()
    sm.store("gravity_constant", 9.8)
    sm.revise("gravity_constant", 9.80665, reason="Higher precision calibration")

    res = sm.retrieve("gravity")
    assert len(res) == 1
    assert res[0] == 9.80665


def test_episodic_memory_immutable_history() -> None:
    em = EpisodicMemory()
    em.store("episode-1", "Executed plan A")

    with pytest.raises(NotImplementedError):
        em.revise("episode-1", "Executed plan B", reason="Rewriting history")
