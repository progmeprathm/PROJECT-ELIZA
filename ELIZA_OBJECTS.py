"""
ELIZA Objects (Single Source of Truth for Cognitive Objects)
Phase 2 Executable Architecture - ELIZA v0.1
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class Observation:
    id: str = field(default_factory=lambda: f"obs-{uuid.uuid4().hex[:8]}")
    source: str = "perception"
    modality: str = "text"
    raw_data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class Evidence:
    id: str = field(default_factory=lambda: f"ev-{uuid.uuid4().hex[:8]}")
    supports: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    strength: float = 1.0
    origin_observation_id: str = ""


@dataclass
class Hypothesis:
    id: str = field(default_factory=lambda: f"hyp-{uuid.uuid4().hex[:8]}")
    statement: str = ""
    confidence: float = 0.5
    predictions: List[str] = field(default_factory=list)
    required_evidence: List[str] = field(default_factory=list)


@dataclass
class Belief:
    id: str = field(default_factory=lambda: f"bel-{uuid.uuid4().hex[:8]}")
    statement: str = ""
    confidence: float = 0.5
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    status: str = "new"


@dataclass
class Knowledge:
    id: str = field(default_factory=lambda: f"kn-{uuid.uuid4().hex[:8]}")
    concept: str = ""
    associated_belief_ids: List[str] = field(default_factory=list)
    facts: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)


@dataclass
class Goal:
    id: str = field(default_factory=lambda: f"goal-{uuid.uuid4().hex[:8]}")
    description: str = ""
    priority: int = 1
    deadline: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    progress: float = 0.0
    owner: str = "executive"
    measurable_completion_criteria: List[str] = field(default_factory=lambda: ["Goal achieved"])
    status: str = "created"


@dataclass
class Task:
    id: str = field(default_factory=lambda: f"tsk-{uuid.uuid4().hex[:8]}")
    description: str = ""
    preconditions: List[str] = field(default_factory=list)
    resources: Dict[str, float] = field(default_factory=dict)
    completion_criteria: str = "Completed"
    status: str = "created"


@dataclass
class Plan:
    id: str = field(default_factory=lambda: f"plan-{uuid.uuid4().hex[:8]}")
    goal_id: str = ""
    tasks: List[Task] = field(default_factory=list)
    estimated_cost: float = 1.0
    estimated_duration: float = 1.0
    risk: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    success_probability: float = 1.0


@dataclass
class Decision:
    id: str = field(default_factory=lambda: f"dec-{uuid.uuid4().hex[:8]}")
    alternatives: List[str] = field(default_factory=list)
    chosen_option: str = ""
    utility: float = 1.0
    confidence: float = 1.0
    justification: str = ""


@dataclass
class Action:
    id: str = field(default_factory=lambda: f"act-{uuid.uuid4().hex[:8]}")
    plan_id: str = ""
    executor: str = "executive"
    tool: str = "core"
    parameters: Dict[str, Any] = field(default_factory=dict)
    expected_outcome: str = ""
    observed_outcome: Optional[str] = None


@dataclass
class Outcome:
    id: str = field(default_factory=lambda: f"out-{uuid.uuid4().hex[:8]}")
    action_id: str = ""
    success: bool = True
    metrics: Dict[str, float] = field(default_factory=dict)
    side_effects: List[str] = field(default_factory=list)
    unexpected_events: List[str] = field(default_factory=list)


@dataclass
class Experience:
    id: str = field(default_factory=lambda: f"exp-{uuid.uuid4().hex[:8]}")
    outcome_id: str = ""
    reflection_notes: str = ""
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class Policy:
    id: str = field(default_factory=lambda: f"pol-{uuid.uuid4().hex[:8]}")
    name: str = ""
    rule: str = ""
    version: str = "1.0.0"
    active: bool = True


@dataclass
class Memory:
    id: str = field(default_factory=lambda: f"mem-{uuid.uuid4().hex[:8]}")
    memory_type: str = "working"
    payload: Any = None
    importance: float = 0.5
    retrieval_score: float = 0.0
    last_accessed: float = field(default_factory=time.time)
    provenance: str = "unknown"


@dataclass
class Entity:
    id: str = field(default_factory=lambda: f"ent-{uuid.uuid4().hex[:8]}")
    name: str = ""
    category: str = "thing"
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    id: str = field(default_factory=lambda: f"rel-{uuid.uuid4().hex[:8]}")
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: str = "relates_to"
    strength: float = 1.0


@dataclass
class Context:
    id: str = field(default_factory=lambda: f"ctx-{uuid.uuid4().hex[:8]}")
    location: str = "local"
    time_scope: float = field(default_factory=time.time)
    participants: List[str] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)
    active_goal_ids: List[str] = field(default_factory=list)
    available_resources: Dict[str, float] = field(default_factory=dict)


@dataclass
class WorldModel:
    id: str = field(default_factory=lambda: f"wm-{uuid.uuid4().hex[:8]}")
    entity_ids: List[str] = field(default_factory=list)
    relationship_ids: List[str] = field(default_factory=list)
    belief_ids: List[str] = field(default_factory=list)
    knowledge_ids: List[str] = field(default_factory=list)


@dataclass
class State:
    id: str = field(default_factory=lambda: f"st-{uuid.uuid4().hex[:8]}")
    active_goal_ids: List[str] = field(default_factory=list)
    working_memory_ids: List[str] = field(default_factory=list)
    current_plan_ids: List[str] = field(default_factory=list)
    resource_usage: Dict[str, float] = field(default_factory=dict)


@dataclass
class Event:
    id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:8]}")
    event_type: str = "generic"
    source_subsystem: str = "unknown"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
