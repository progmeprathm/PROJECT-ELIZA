import logging
import threading
import queue
from typing import Callable, List, Optional
from eliza.kernel.events import Event, EventType

logger = logging.getLogger(__name__)

class EventSubscriber:
    def __init__(self, callback: Callable[[Event], None], filter_types: Optional[List[EventType]] = None):
        self.callback = callback
        self.filter_types = filter_types or list(EventType)
        self.id = id(self)

class RuntimeEventBus:
    """
    A runtime-scoped event bus for E.L.I.Z.A. Observability.
    Handles synchronous/non-blocking subscribers, bounded queues, and subscriber failure isolation.
    Uses threading to integrate cleanly with ThreadingHTTPServer.
    """
    def __init__(self, runtime_id: str):
        self.runtime_id = runtime_id
        self._subscribers: List[EventSubscriber] = []
        self._queue: queue.Queue = queue.Queue(maxsize=1000)
        self._is_running = False
        self._worker_thread: Optional[threading.Thread] = None

    def start(self):
        """Starts the event dispatch background thread."""
        if not self._is_running:
            self._is_running = True
            self._worker_thread = threading.Thread(target=self._process_events, daemon=True)
            self._worker_thread.start()

    def stop(self):
        """Stops the event bus."""
        self._is_running = False
        if self._worker_thread:
            self._queue.put(None) # Sentinel to wake up blocking get
            self._worker_thread.join(timeout=2.0)

    def subscribe(self, callback: Callable[[Event], None], filter_types: Optional[List[EventType]] = None) -> int:
        """Subscribe to events. Returns subscription ID."""
        sub = EventSubscriber(callback, filter_types)
        self._subscribers.append(sub)
        return sub.id
        
    def unsubscribe(self, sub_id: int):
        """Remove a subscriber by its ID."""
        self._subscribers = [s for s in self._subscribers if s.id != sub_id]

    def emit(self, event: Event):
        """Fire and forget an event into the bus. Drops if queue is completely full."""
        try:
            self._queue.put_nowait(event)
        except queue.Full:
            logger.warning(f"EventBus for runtime {self.runtime_id} queue full! Dropping event {event.event_id}")

    def _process_events(self):
        while self._is_running:
            try:
                event = self._queue.get(timeout=1.0)
                if event is None:
                    break
                
                # Dispatch to subscribers
                for sub in self._subscribers:
                    if event.event_type in sub.filter_types:
                        self._safe_invoke(sub, event)
                        
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"EventBus core loop error: {str(e)}")

    def _safe_invoke(self, sub: EventSubscriber, event: Event):
        try:
            sub.callback(event)
        except Exception as e:
            logger.error(f"Subscriber {sub.id} failed processing event {event.event_id}: {str(e)}")
