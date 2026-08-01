"""
Cognitive Simulator for ELIZA.
Evaluates plans in a sandbox to project side-effects and outcomes before real-world execution.
"""

from typing import List, Optional
import uuid

from eliza.core.events import EventBus, SimulationCompleted
from eliza.core.interface import ISimulator
from eliza.core.types import Belief, Confidence, Plan, SimulationResult, SubsystemType


class CognitiveSimulator(ISimulator):
    """
    Simulates plan execution in an isolated hypothetical sandbox.
    Produces evidence and side-effect predictions without modifying real world state.
    """

    def __init__(self) -> None:
        self._event_bus: Optional[EventBus] = None

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.SIMULATION

    def initialize(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def simulate(self, plan: Plan, world_state: List[Belief]) -> SimulationResult:
        sim_id = f"sim-{uuid.uuid4().hex[:8]}"

        # Project side-effects based on plan steps and current world beliefs
        predicted_side_effects = []
        if plan.estimated_risk > 0.15:
            predicted_side_effects.append("Moderate resource consumption spike detected")
        if any("ANALYZE" in step.action_type for step in plan.steps):
            predicted_side_effects.append("Read-only context buffer overhead")

        outcome_confidence = 1.0 - (plan.estimated_risk * 0.5)
        evidence = [f"Step {s.step_index}: {s.description}" for s in plan.steps]

        res = SimulationResult(
            simulation_id=sim_id,
            plan_id=plan.id,
            predicted_outcome=f"Plan '{plan.id}' projected to succeed with risk {plan.estimated_risk}",
            confidence=Confidence(value=round(outcome_confidence, 4), source="CognitiveSimulator"),
            evidence=evidence,
            side_effects=predicted_side_effects,
        )

        if self._event_bus:
            self._event_bus.publish(
                SimulationCompleted(
                    source_subsystem="CognitiveSimulator",
                    simulation_result=res,
                )
            )

        return res
