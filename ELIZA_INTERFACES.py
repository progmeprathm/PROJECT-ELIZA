"""
ELIZA Interfaces (Python Abstract Base Classes)
Phase 2 Executable Architecture - ELIZA v0.1
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ELIZA_OBJECTS import Action, Belief, Goal, Memory, Outcome, Plan, Policy


class MemoryModule(ABC):
    @abstractmethod
    def store(self, key: str, value: Any, importance: float = 0.5) -> None: pass

    @abstractmethod
    def retrieve(self, query: str, limit: int = 10) -> List[Any]: pass

    @abstractmethod
    def forget(self, key: str) -> bool: pass

    @abstractmethod
    def consolidate(self) -> None: pass


class ReasonerModule(ABC):
    @abstractmethod
    def reason(self, beliefs: List[Belief], style: str = "deductive") -> List[Belief]: pass

    @abstractmethod
    def evaluate(self, statement: str, evidence_ids: List[str]) -> float: pass


class PlannerModule(ABC):
    @abstractmethod
    def plan(self, goal: Goal, beliefs: List[Belief]) -> Plan: pass

    @abstractmethod
    def replan(self, failed_plan_id: str, new_constraints: List[str]) -> Plan: pass


class SimulatorModule(ABC):
    @abstractmethod
    def simulate(self, plan: Plan, world_state: List[Belief]) -> Dict[str, Any]: pass


class SafetyModule(ABC):
    @abstractmethod
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> Dict[str, Any]: pass


class LearnerModule(ABC):
    @abstractmethod
    def validate_learning(self, candidate_policy: Policy) -> bool: pass
