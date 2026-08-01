"""
Core Data Types for ELIZA Cognitive Operating System.
Dataclasses and Enums representing fundamental cognitive structures, canonical axioms, and FCRL primitives.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid

# Import canonical FCRL primitive classes
from eliza.core.fcrl import (
    Action,
    Belief,
    Constraint,
    Context,
    Decision,
    Entity,
    Event,
    Evidence,
    Experience,
    FCRLObject,
    Goal,
    Hypothesis,
    Identity as FCRLIdentity,
    Knowledge,
    MemoryObject,
    Observation,
    Outcome,
    Plan,
    Policy,
    Question,
    Relationship,
    Skill,
    State,
    Task,
)


class ReasoningStyle(str, Enum):
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    COUNTERFACTUAL = "counterfactual"
    ANALOGICAL = "analogical"
    PROBABILISTIC = "probabilistic"


class SubsystemType(str, Enum):
    PERCEPTION = "perception"
    MEMORY = "memory"
    WORLD_MODEL = "world_model"
    REASONING = "reasoning"
    PLANNING = "planning"
    SIMULATION = "simulation"
    EXECUTIVE = "executive"
    SAFETY = "safety"
    EXPLAINABILITY = "explainability"
    LEARNING = "learning"


@dataclass
class Confidence:
    value: float  # Range: [0.0, 1.0]
    source: str
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Confidence value must be in range [0.0, 1.0], got {self.value}")


@dataclass
class ProvenanceRecord:
    source_subsystem: str
    method: str
    created_at: float = field(default_factory=time.time)
    revised_at: Optional[float] = None
    evidence_ids: List[str] = field(default_factory=list)
    version: int = 1

    def revise(self) -> None:
        self.revised_at = time.time()
        self.version += 1


@dataclass
class PlanStep:
    step_index: int
    description: str
    action_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    estimated_risk: float = 0.0


@dataclass
class RiskAssessment:
    action_id: str
    risk_score: float  # Range: [0.0, 1.0]
    policy_violations: List[str] = field(default_factory=list)
    compliant: bool = True
    vetoed: bool = False
    reason: str = "Clearance granted"


@dataclass
class SimulationResult:
    simulation_id: str
    plan_id: str
    predicted_outcome: str
    confidence: Confidence
    evidence: List[str]
    side_effects: List[str] = field(default_factory=list)


@dataclass
class Explanation:
    decision_id: str
    why: str
    evidence: List[str]
    beliefs_used: List[str]
    assumptions: List[str]
    alternatives_considered: List[str]
    confidence: Confidence
    timestamp: float = field(default_factory=time.time)


@dataclass
class AttentionAllocation:
    focus_topic: str
    compute_units_allocated: float
    memory_limit_mb: float
    timeout_seconds: float
    priority_level: int = 1


@dataclass
class MetaCognitiveState:
    target_plan_id: str
    self_confidence: Confidence
    perceived_knowledge_gaps: List[str] = field(default_factory=list)
    recommended_strategy_adjustment: Optional[str] = None


@dataclass
class ValidatedLearning:
    learning_id: str
    source_experience_ids: List[str]
    proposed_policy_update: str
    validation_score: float  # Range: [0.0, 1.0]
    accepted: bool = False
    timestamp: float = field(default_factory=time.time)


@dataclass
class Identity:
    system_name: str = "ELIZA"
    version: str = "1.0.0"
    core_values: List[str] = field(default_factory=lambda: [
        "Modular Architecture",
        "Transparent Reasoning",
        "Absolute Safety Veto",
        "Inspectable Provenance",
        "FCRL Graph Alignment",
    ])
    active_goals_count: int = 0
    total_cycles_executed: int = 0
