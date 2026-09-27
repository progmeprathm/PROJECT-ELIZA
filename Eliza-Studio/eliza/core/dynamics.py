"""
Cognitive Dynamics Module for ELIZA.
Enforces ELIZA_DYNAMICS.md Version 1.0 (Cognitive Health, Lifecycles, and Section XXIX System Invariants).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time

from eliza.core.fcrl import (
    Action,
    Belief,
    Experience,
    FCRLObject,
    Goal,
    MemoryObject,
    Outcome,
    Plan,
    ValidatedLearning,
)


class BeliefStatus(str, Enum):
    """Belief Lifecycle States (Section IX)."""
    NEW = "new"
    SUPPORTED = "supported"
    STRENGTHENED = "strengthened"
    QUESTIONED = "questioned"
    REVISED = "revised"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class GoalStatus(str, Enum):
    """Goal Lifecycle States (Section X)."""
    CREATED = "created"
    QUEUED = "queued"
    ACTIVE = "active"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


@dataclass
class CognitiveHealthReport:
    """System Health metrics (Section XXII & XXV)."""
    memory_pressure: float  # Range [0.0, 1.0]
    reasoning_backlog: int
    planning_backlog: int
    simulation_queue_depth: int
    error_rate: float  # Range [0.0, 1.0]
    resource_exhaustion: float  # Range [0.0, 1.0]
    healthy: bool = True
    timestamp: float = field(default_factory=time.time)


class CognitiveHealthMonitor:
    """Kernel component continuously evaluating system cognitive health."""

    def __init__(self, memory_limit_items: int = 1000) -> None:
        self.memory_limit_items = memory_limit_items

    def evaluate_health(
        self,
        memory_item_count: int,
        reasoning_backlog: int = 0,
        planning_backlog: int = 0,
        simulation_queue_depth: int = 0,
        error_rate: float = 0.0,
    ) -> CognitiveHealthReport:
        mem_pressure = min(1.0, memory_item_count / self.memory_limit_items)
        res_exhaustion = max(mem_pressure, error_rate)
        is_healthy = mem_pressure < 0.95 and error_rate < 0.50

        return CognitiveHealthReport(
            memory_pressure=round(mem_pressure, 4),
            reasoning_backlog=reasoning_backlog,
            planning_backlog=planning_backlog,
            simulation_queue_depth=simulation_queue_depth,
            error_rate=round(error_rate, 4),
            resource_exhaustion=round(res_exhaustion, 4),
            healthy=is_healthy,
        )


class DynamicsSystemInvariantValidator:
    """Enforces Section XXIX System Invariants at all times."""

    @staticmethod
    def validate_dynamics_invariants(
        goals: List[Goal],
        memories: List[MemoryObject],
        beliefs: List[Belief],
        actions: List[Action],
        plans: List[Plan],
        outcomes: List[Outcome],
        learnings: List[ValidatedLearning],
        experiences: List[Experience],
    ) -> Dict[str, bool]:
        results = {
            "No_Orphan_Goals": True,
            "No_Orphan_Memories": True,
            "Every_Belief_Has_Provenance": True,
            "Every_Action_Belongs_To_A_Goal": True,
            "Every_Plan_Belongs_To_A_Goal": True,
            "Every_Outcome_Belongs_To_An_Action": True,
            "Every_Learning_Event_References_Experience": True,
        }

        goal_ids = {g.id for g in goals}
        plan_ids = {p.id for p in plans}
        action_ids = {a.id for a in actions}
        exp_ids = {e.id for e in experiences}

        # 1. No orphan goals (all goals have an owner/description)
        for g in goals:
            if not g.description or not g.owner:
                results["No_Orphan_Goals"] = False

        # 2. No orphan memories (all memories have provenance and valid payload)
        for m in memories:
            if not m.provenance:
                results["No_Orphan_Memories"] = False

        # 3. Every belief has provenance (supporting/contradicting evidence)
        for b in beliefs:
            if not b.supporting_evidence and not b.contradicting_evidence:
                results["Every_Belief_Has_Provenance"] = False

        # 4. Every action belongs to a goal (via plan -> goal_id)
        plan_goal_map = {p.id: p.goal_id for p in plans}
        for a in actions:
            if not a.plan_id or a.plan_id not in plan_goal_map or not plan_goal_map[a.plan_id]:
                results["Every_Action_Belongs_To_A_Goal"] = False

        # 5. Every plan belongs to a goal
        for p in plans:
            if not p.goal_id or p.goal_id not in goal_ids:
                results["Every_Plan_Belongs_To_A_Goal"] = False

        # 6. Every outcome belongs to an action
        for o in outcomes:
            if not o.action_id or o.action_id not in action_ids:
                results["Every_Outcome_Belongs_To_An_Action"] = False

        # 7. Every learning event references experience
        for l in learnings:
            if not l.source_experience_ids:
                results["Every_Learning_Event_References_Experience"] = False

        return results
