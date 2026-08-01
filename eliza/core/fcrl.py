"""
Formal Cognitive Representation Language (FCRL) for ELIZA.
Enforces ELIZA_FORMALISM.md Version 1.0 (24 Primitive Cognitive Objects & 10 Cognitive Invariants).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class FCRLObject:
    """Base class for all FCRL Cognitive Objects (Invariant 10: Every cognitive object has a unique id)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)


@dataclass
class Observation(FCRLObject):
    source: str = "perception"
    modality: str = "text"
    raw_data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Evidence(FCRLObject):
    supports: List[str] = field(default_factory=list)  # Target Belief IDs supported
    contradicts: List[str] = field(default_factory=list)  # Target Belief IDs contradicted
    strength: float = 1.0  # Range [0.0, 1.0]
    origin_observation_id: str = ""


@dataclass
class Belief(FCRLObject):
    statement: str = ""
    confidence: float = 0.5  # Range [0.0, 1.0]
    supporting_evidence: List[str] = field(default_factory=list)  # Evidence IDs (Invariant 1)
    contradicting_evidence: List[str] = field(default_factory=list)
    status: str = "active"  # active, revised, rejected


@dataclass
class Knowledge(FCRLObject):
    concept: str = ""
    associated_belief_ids: List[str] = field(default_factory=list)  # Belief IDs (Invariant 7)
    facts: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)


@dataclass
class Entity(FCRLObject):
    name: str = ""
    category: str = "thing"
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship(FCRLObject):
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: str = "relates_to"  # owns, contains, causes, located_in, depends_on, created_by, part_of
    strength: float = 1.0


@dataclass
class Context(FCRLObject):
    location: str = "local"
    time_scope: float = field(default_factory=time.time)
    participants: List[str] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)
    active_goal_ids: List[str] = field(default_factory=list)
    available_resources: Dict[str, float] = field(default_factory=dict)


@dataclass
class MemoryObject(FCRLObject):
    memory_type: str = "working"  # working, short_term, semantic, episodic, procedural, long_term
    payload: Any = None
    importance: float = 0.5
    retrieval_score: float = 0.0
    last_accessed: float = field(default_factory=time.time)
    provenance: str = "unknown"  # Provenance tracking (Invariant 5)


@dataclass
class Goal(FCRLObject):
    description: str = ""
    priority: int = 1
    deadline: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    progress: float = 0.0
    owner: str = "executive"
    measurable_completion_criteria: List[str] = field(default_factory=lambda: ["Goal achieved"])  # Invariant 8


@dataclass
class Constraint(FCRLObject):
    category: str = "time"  # time, budget, ethics, permissions, physical
    rule: str = ""
    strictness: float = 1.0


@dataclass
class Hypothesis(FCRLObject):
    statement: str = ""
    confidence: float = 0.5
    predictions: List[str] = field(default_factory=list)
    required_evidence: List[str] = field(default_factory=list)
    status: str = "untested"


@dataclass
class Question(FCRLObject):
    missing_knowledge_query: str = ""
    target_goal_id: str = ""


@dataclass
class Task(FCRLObject):
    description: str = ""
    preconditions: List[str] = field(default_factory=list)
    resources: Dict[str, float] = field(default_factory=dict)
    completion_criteria: str = "Completed"
    status: str = "pending"


@dataclass
class Plan(FCRLObject):
    goal_id: str = ""  # Reference Goal (Invariant 2)
    tasks: List[Task] = field(default_factory=list)
    estimated_cost: float = 1.0
    estimated_duration: float = 1.0
    risk: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    success_probability: float = 1.0


@dataclass
class Decision(FCRLObject):
    alternatives: List[str] = field(default_factory=list)
    chosen_option: str = ""
    utility: float = 1.0
    confidence: float = 1.0  # Confidence tracking (Invariant 6)
    justification: str = ""


@dataclass
class Action(FCRLObject):
    plan_id: str = ""  # Reference Plan (Invariant 3)
    executor: str = "executive"
    tool: str = "core"
    parameters: Dict[str, Any] = field(default_factory=dict)
    expected_outcome: str = ""
    observed_outcome: Optional[str] = None


@dataclass
class Outcome(FCRLObject):
    action_id: str = ""
    success: bool = True
    metrics: Dict[str, float] = field(default_factory=dict)
    side_effects: List[str] = field(default_factory=list)
    unexpected_events: List[str] = field(default_factory=list)


@dataclass
class Experience(FCRLObject):
    outcome_id: str = ""  # Reference Outcome (Invariant 4)
    reflection_notes: str = ""
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class Policy(FCRLObject):
    name: str = ""
    rule: str = ""
    version: str = "1.0.0"  # Version control (Invariant 9)
    active: bool = True


@dataclass
class Skill(FCRLObject):
    name: str = ""
    proficiency: float = 0.5
    practice_count: int = 0


@dataclass
class Identity(FCRLObject):
    knowledge_profile: Dict[str, Any] = field(default_factory=dict)
    values: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    behavioral_traits: List[str] = field(default_factory=list)


@dataclass
class State(FCRLObject):
    active_goal_ids: List[str] = field(default_factory=list)
    working_memory_ids: List[str] = field(default_factory=list)
    current_plan_ids: List[str] = field(default_factory=list)
    resource_usage: Dict[str, float] = field(default_factory=dict)


class CognitiveInvariantValidator:
    """Automated enforcer for all 10 Formal Cognitive Invariants in ELIZA_FORMALISM.md."""

    @staticmethod
    def validate_invariants(cognitive_objects: List[FCRLObject]) -> Dict[str, bool]:
        results = {f"Invariant_{i}": True for i in range(1, 11)}

        object_map = {obj.id: obj for obj in cognitive_objects}

        for obj in cognitive_objects:
            # Invariant 10: Every cognitive object has a unique identity.
            if not obj.id:
                results["Invariant_10"] = False

            # Invariant 1: Every Belief references Evidence.
            if isinstance(obj, Belief):
                if not obj.supporting_evidence and not obj.contradicting_evidence:
                    results["Invariant_1"] = False

            # Invariant 2: Every Plan references Goals.
            elif isinstance(obj, Plan):
                if not obj.goal_id:
                    results["Invariant_2"] = False

            # Invariant 3: Every Action belongs to a Plan.
            elif isinstance(obj, Action):
                if not obj.plan_id:
                    results["Invariant_3"] = False

            # Invariant 4: Every Experience references an Outcome.
            elif isinstance(obj, Experience):
                if not obj.outcome_id:
                    results["Invariant_4"] = False

            # Invariant 5: Every Memory has provenance.
            elif isinstance(obj, MemoryObject):
                if not obj.provenance:
                    results["Invariant_5"] = False

            # Invariant 6: Every Decision records confidence.
            elif isinstance(obj, Decision):
                if obj.confidence is None or not (0.0 <= obj.confidence <= 1.0):
                    results["Invariant_6"] = False

            # Invariant 7: Every Knowledge object references Beliefs.
            elif isinstance(obj, Knowledge):
                if not obj.associated_belief_ids:
                    results["Invariant_7"] = False

            # Invariant 8: Every Goal has measurable completion criteria.
            elif isinstance(obj, Goal):
                if not obj.measurable_completion_criteria:
                    results["Invariant_8"] = False

            # Invariant 9: Every Policy is version controlled.
            elif isinstance(obj, Policy):
                if not obj.version:
                    results["Invariant_9"] = False

        return results
