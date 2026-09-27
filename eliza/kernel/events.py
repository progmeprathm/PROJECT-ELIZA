from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import datetime
import uuid

class EventType(str, Enum):
    AgentStateChanged = "AgentStateChanged"
    ToolCalled = "ToolCalled"
    ToolExecuted = "ToolExecuted"
    ToolFailed = "ToolFailed"
    MemoryRetrieved = "MemoryRetrieved"
    MemoryStored = "MemoryStored"
    MemoryInvalidated = "MemoryInvalidated"
    KnowledgeApplied = "KnowledgeApplied"
    KnowledgeCreated = "KnowledgeCreated"
    KnowledgeConflictDetected = "KnowledgeConflictDetected"
    GoalCreated = "GoalCreated"
    GoalTreeUpdated = "GoalTreeUpdated"
    TaskDelegated = "TaskDelegated"
    TaskReassigned = "TaskReassigned"
    CoordinationCompleted = "CoordinationCompleted"
    ModelRequested = "ModelRequested"
    ModelResponded = "ModelResponded"
    ModelFailed = "ModelFailed"
    ModelRouterFailover = "ModelRouterFailover"
    LatencyMetric = "LatencyMetric"
    VerificationStarted = "VerificationStarted"
    VerificationCompleted = "VerificationCompleted"
    VerificationFailed = "VerificationFailed"
    ReplanTriggered = "ReplanTriggered"
    PlanUpdated = "PlanUpdated"
    HumanOverride = "HumanOverride"
    WorldModelUpdated = "WorldModelUpdated"
    GraphNodeAdded = "GraphNodeAdded"
    GraphEdgeAdded = "GraphEdgeAdded"
    GraphEdgeUpdated = "GraphEdgeUpdated"

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    event_type: EventType
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    runtime_id: str
    goal_id: Optional[str] = None
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    source: str
    payload: Dict[str, Any]
    provenance: Optional[Dict[str, Any]] = None
    schema_version: int = 1
