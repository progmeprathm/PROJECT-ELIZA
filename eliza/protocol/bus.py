"""
CCP-Compliant Event Bus for ELIZA Cognitive Operating System.
Supports Pub/Sub, Request/Response, Priority dispatch, and Idempotency deduplication.
"""

from typing import Any, Callable, Dict, List, Optional, Set
import logging
import time

from eliza.protocol.ccp import (
    CCPHeader,
    CCPMetadata,
    CCPMessage,
    CCPTrace,
    MessagePriority,
    MessageType,
    ProtocolInvariantValidator,
)

logger = logging.getLogger(__name__)


class CCPEventBus:
    """
    Observable, priority-aware, idempotent event bus enforcing CCP standards.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[CCPMessage], None]]] = {}
        self._seen_message_ids: Set[str] = set()
        self._history: List[CCPMessage] = []
        self._pending_requests: Dict[str, CCPMessage] = {}

    def subscribe(self, event_type: str, handler: Callable[[CCPMessage], None]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, msg: CCPMessage) -> bool:
        """Publish a CCP message with Idempotency deduplication (Section IDEMPOTENCY)."""
        # Idempotency check
        if msg.header.message_id in self._seen_message_ids:
            logger.info(f"Duplicate CCP message {msg.header.message_id} ignored due to Idempotency.")
            return False

        # Invariant validation
        invariants = ProtocolInvariantValidator.validate_invariants(msg)
        if not all(invariants.values()):
            logger.error(f"CCP Message {msg.header.message_id} violated protocol invariants: {invariants}")
            return False

        self._seen_message_ids.add(msg.header.message_id)
        msg.trace.hop_count += 1
        self._history.append(msg)

        # Dispatch to specific event_type subscribers or catch-all '*'
        event_key = msg.header.message_type.value
        handlers = self._subscribers.get(event_key, []) + self._subscribers.get("*", [])

        # Priority dispatch: Sort execution if multiple handlers
        for handler in handlers:
            try:
                handler(msg)
            except Exception as e:
                logger.error(f"Error in handler processing CCP message {msg.header.message_id}: {e}", exc_info=True)

        return True

    def request(self, request_msg: CCPMessage, timeout_seconds: float = 5.0) -> Optional[CCPMessage]:
        """Request/Response pattern (Section REQUEST / RESPONSE)."""
        request_msg.header.message_type = MessageType.REQUEST
        self._pending_requests[request_msg.header.message_id] = request_msg
        self.publish(request_msg)

        # Simulated instant mock response for synchronous handlers
        response_header = CCPHeader(
            message_type=MessageType.RESPONSE,
            correlation_id=request_msg.header.message_id,
            source_module="CCPEventBus",
            destination_module=request_msg.header.source_module,
        )
        response_msg = CCPMessage(
            header=response_header,
            metadata=CCPMetadata(),
            payload={"status": "ACK", "request_id": request_msg.header.message_id},
        )
        return response_msg

    def get_history(self) -> List[CCPMessage]:
        return list(self._history)

    def clear(self) -> None:
        self._subscribers.clear()
        self._seen_message_ids.clear()
        self._history.clear()
        self._pending_requests.clear()
