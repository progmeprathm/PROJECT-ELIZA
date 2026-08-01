"""
Attention Allocator for ELIZA Executive Control.
Enforces Axiom 13: Computation, memory, and time are finite limited resources.
"""

from typing import Optional

from eliza.core.events import AttentionAllocated, EventBus
from eliza.core.interface import IAttentionAllocator
from eliza.core.types import AttentionAllocation, SubsystemType


class AttentionAllocator(IAttentionAllocator):
    """
    Allocates dynamic focus, compute budgets, and execution timeouts for incoming stimuli based on goal priority.
    """

    def __init__(self, default_compute_budget: float = 1.0, default_memory_mb: float = 256.0) -> None:
        self.default_compute_budget = default_compute_budget
        self.default_memory_mb = default_memory_mb
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.EXECUTIVE

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def allocate_attention(self, stimulus: str, goal_priority: int) -> AttentionAllocation:
        compute_units = self.default_compute_budget * (1.0 + (goal_priority * 0.1))
        memory_limit = self.default_memory_mb * (1.0 + (goal_priority * 0.05))
        timeout = min(30.0, 5.0 + (goal_priority * 1.0))

        allocation = AttentionAllocation(
            focus_topic=stimulus[:50],
            compute_units_allocated=round(compute_units, 2),
            memory_limit_mb=round(memory_limit, 2),
            timeout_seconds=round(timeout, 2),
            priority_level=goal_priority,
        )

        if self._event_bus:
            self._event_bus.publish(
                AttentionAllocated(
                    source_subsystem="AttentionAllocator",
                    allocation=allocation,
                )
            )

        return allocation
