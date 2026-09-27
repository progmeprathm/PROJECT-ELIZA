"""
Subsystem Abstract Interfaces for ELIZA Cognitive Operating System.
Enforces Article IV & Canonical Axioms: Modularity, explicit interfaces, and low coupling.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from eliza.core.events import EventBus
from eliza.core.types import (
    Action,
    AttentionAllocation,
    Belief,
    Entity,
    Explanation,
    Goal,
    MetaCognitiveState,
    Observation,
    Plan,
    ReasoningStyle,
    Relationship,
    RiskAssessment,
    SimulationResult,
    SubsystemType,
    ValidatedLearning,
)


class ICognitiveSubsystem(ABC):
    """Base interface for all ELIZA cognitive subsystems."""

    @property
    @abstractmethod
    def subsystem_type(self) -> SubsystemType:
        """Unique subsystem identifier."""
        pass

    @abstractmethod
    def initialize(self, event_bus: EventBus) -> None:
        """Initialize the subsystem with the central event bus."""
        pass


class IMemorySubsystem(ICognitiveSubsystem):
    """Interface for Memory Tiers (Working, Short-Term, Semantic, Episodic, Procedural, Long-Term)."""

    @abstractmethod
    def store(self, key: str, value: Any, provenance_info: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        pass

    @abstractmethod
    def revise(self, key: str, new_value: Any, reason: str) -> None:
        pass

    @abstractmethod
    def consolidate(self) -> None:
        pass


class IWorldModel(ICognitiveSubsystem):
    """Canonical representation of reality (Entities, Relationships, Beliefs, Confidence)."""

    @abstractmethod
    def add_entity(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def add_relationship(self, relationship: Relationship) -> None:
        pass

    @abstractmethod
    def update_belief(self, belief: Belief) -> None:
        pass

    @abstractmethod
    def get_belief(self, belief_id: str) -> Optional[Belief]:
        pass

    @abstractmethod
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        pass

    @abstractmethod
    def query_facts(self, query_str: str) -> List[Belief]:
        pass


class IReasoningEngine(ICognitiveSubsystem):
    """Evaluates beliefs and proposes explanations without modifying reality."""

    @abstractmethod
    def reason(
        self,
        beliefs: List[Belief],
        style: ReasoningStyle = ReasoningStyle.DEDUCTIVE,
        target_hypothesis: Optional[str] = None,
    ) -> List[Belief]:
        pass


class IPlanner(ICognitiveSubsystem):
    """Converts goals into executable strategies considering resources, constraints, and risk."""

    @abstractmethod
    def create_plan(
        self,
        goal: Goal,
        beliefs: List[Belief],
        available_resources: Dict[str, float],
    ) -> Plan:
        pass


class ISimulator(ICognitiveSubsystem):
    """Evaluates plan outcomes ('What happens if...') without altering real-world state."""

    @abstractmethod
    def simulate(self, plan: Plan, world_state: List[Belief]) -> SimulationResult:
        pass


class ISafetyGuard(ICognitiveSubsystem):
    """Independent safety evaluation engine with absolute veto authority."""

    @abstractmethod
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> RiskAssessment:
        pass


class IExecutiveControl(ICognitiveSubsystem):
    """Orchestrates cognitive pipeline, goal arbitration, and resource allocation."""

    @abstractmethod
    def arbitrate_goals(self, goals: List[Goal]) -> List[Goal]:
        pass

    @abstractmethod
    def execute_cognitive_cycle(self, input_stimulus: str) -> Dict[str, Any]:
        pass


class IExplainabilityTracer(ICognitiveSubsystem):
    """Constructs structured explanations for cognitive decisions."""

    @abstractmethod
    def record_decision(self, explanation: Explanation) -> None:
        pass

    @abstractmethod
    def get_explanation(self, decision_id: str) -> Optional[Explanation]:
        pass


class IAttentionAllocator(ICognitiveSubsystem):
    """Dynamically manages finite compute, memory, and time resources (Axiom 13)."""

    @abstractmethod
    def allocate_attention(self, stimulus: str, goal_priority: int) -> AttentionAllocation:
        pass


class IMetaCognition(ICognitiveSubsystem):
    """Evaluates the system's own plans, knowledge gaps, and confidence recursively (Axiom 17, 18)."""

    @abstractmethod
    def evaluate_cognition(self, plan: Plan, beliefs: List[Belief]) -> MetaCognitiveState:
        pass


class ILearningValidator(ICognitiveSubsystem):
    """Validates proposed learning updates before persistent system changes are accepted (Axiom 23)."""

    @abstractmethod
    def validate_learning(self, candidate: ValidatedLearning) -> bool:
        pass
