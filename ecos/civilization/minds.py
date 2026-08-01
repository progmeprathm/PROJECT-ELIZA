"""
Layer 1: Multiple Minds Implementation.
Specialized mind profiles with dedicated memory, skills, policies, goals, and world models.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid

from ELIZA_OBJECTS import Belief, Goal, Memory, Policy
from ecos.memory.system import ECOSMemorySystem
from ecos.world.graph import ECOSWorldModel


@dataclass
class SpecializedMind:
    mind_id: str = field(default_factory=lambda: f"mind-{uuid.uuid4().hex[:6]}")
    name: str = "SpecializedMind"
    role: str = "Generalist"  # Scientist, Engineer, Planner, Researcher, Teacher, Analyst, Simulator
    specialization_skills: List[str] = field(default_factory=list)
    memory_system: ECOSMemorySystem = field(default_factory=ECOSMemorySystem)
    world_model: ECOSWorldModel = field(default_factory=ECOSWorldModel)
    active_policies: List[Policy] = field(default_factory=list)
    reputation_score: float = 0.90

    def process_task(self, task_description: str) -> Dict[str, Any]:
        """Executes a specialized task according to the mind's role."""
        # Store in local memory
        self.memory_system.store(key=f"task-{self.mind_id}", value=task_description)

        # Form specialized belief
        b = Belief(statement=f"[{self.role}] Formulated response for: '{task_description}'", confidence=self.reputation_score)
        self.world_model.world_model.belief_ids.append(b.id)

        return {
            "mind_id": self.mind_id,
            "role": self.role,
            "reputation": self.reputation_score,
            "result": b.statement,
        }
