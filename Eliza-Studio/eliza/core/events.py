"""
Canonical Event System for ELIZA Cognitive Operating System.
Enforces Article XIV, Cognitive Axioms, and Cognitive Communication Protocol (CCP).
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
import logging
import time
import uuid

from eliza.core.types import (
    Action,
    AttentionAllocation,
    Belief,
    Explanation,
    Goal,
    MetaCognitiveState,
    Observation,
    Plan,
    RiskAssessment,
    SimulationResult,
    ValidatedLearning,
)
from eliza.protocol.ccp import (
    CCPHeader,
    CCPMetadata,
    CCPMessage,
    CCPTrace,
    MessagePriority,
    MessageType,
)

logger = logging.getLogger(__name__)


@dataclass
class CognitiveEvent:
    """Base class for all cognitive events in ELIZA."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    source_subsystem: str = "unknown"

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def to_ccp_message(self) -> CCPMessage:
        header = CCPHeader(
            message_type=MessageType.EVENT,
            message_id=self.event_id,
            timestamp=self.timestamp,
            source_module=self.source_subsystem,
            priority=MessagePriority.NORMAL,
        )
        return CCPMessage(
            header=header,
            metadata=CCPMetadata(),
            payload=self,
            trace=CCPTrace(origin=self.source_subsystem),
        )


@dataclass
class ObservationReceived(CognitiveEvent):
    observation: Optional[Observation] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    raw_input: Optional[str] = None


@dataclass
class MemoryRetrieved(CognitiveEvent):
    query: str = ""
    memory_type: str = ""
    retrieved_items: List[Any] = field(default_factory=list)


@dataclass
class BeliefUpdated(CognitiveEvent):
    belief: Optional[Belief] = None
    previous_state: Optional[Dict[str, Any]] = None


@dataclass
class GoalCreated(CognitiveEvent):
    goal: Optional[Goal] = None


@dataclass
class PlanGenerated(CognitiveEvent):
    plan: Optional[Plan] = None


@dataclass
class SimulationCompleted(CognitiveEvent):
    simulation_result: Optional[SimulationResult] = None


@dataclass
class DecisionMade(CognitiveEvent):
    decision_id: str = ""
    chosen_action: Optional[Action] = None
    explanation: Optional[Explanation] = None


@dataclass
class ActionExecuted(CognitiveEvent):
    action: Optional[Action] = None
    success: bool = True
    output: Optional[Dict[str, Any]] = None


@dataclass
class ReflectionCompleted(CognitiveEvent):
    insights: List[str] = field(default_factory=list)
    action_id: Optional[str] = None


@dataclass
class LearningFinished(CognitiveEvent):
    updated_policies: List[str] = field(default_factory=list)
    knowledge_delta: int = 0


@dataclass
class AttentionAllocated(CognitiveEvent):
    allocation: Optional[AttentionAllocation] = None


@dataclass
class MetaCognitionEvaluated(CognitiveEvent):
    meta_state: Optional[MetaCognitiveState] = None


@dataclass
class LearningValidationRequested(CognitiveEvent):
    candidate_learning: Optional[ValidatedLearning] = None


@dataclass
class LearningValidated(CognitiveEvent):
    validated_learning: Optional[ValidatedLearning] = None
    passed: bool = False


E = TypeVar("E", bound=CognitiveEvent)
EventHandler = Callable[[E], None]


class EventBus:
    """
    Central, thread-safe Event Bus for ELIZA.
    Ensures zero direct coupling between subsystems (Article IV & XIV).
    """

    def __init__(self) -> None:
        self._subscribers: Dict[Type[CognitiveEvent], List[Callable[[Any], None]]] = {}
        self._history: List[CognitiveEvent] = []

    def subscribe(self, event_type: Type[E], handler: EventHandler[E]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)  # type: ignore

    def publish(self, event: CognitiveEvent) -> None:
        self._history.append(event)
        event_type = type(event)

        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error handling event {event.name} in {handler}: {e}", exc_info=True)

        if event_type is not CognitiveEvent and CognitiveEvent in self._subscribers:
            for handler in self._subscribers[CognitiveEvent]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error handling base CognitiveEvent in {handler}: {e}", exc_info=True)

    def get_history(self) -> List[CognitiveEvent]:
        return list(self._history)

    def clear(self) -> None:
        self._subscribers.clear()
        self._history.clear()
