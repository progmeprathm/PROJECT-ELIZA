"""
ECOS Kernel Task Scheduler.
Enforces Section IX & X of ELIZA_KERNEL_SPEC.md.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time
import uuid

from eliza.kernel.spec import TaskState


@dataclass
class KernelTask:
    task_id: str = field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    description: str = ""
    priority: int = 1  # Higher value = higher priority
    handler: Optional[Callable[[], Any]] = None
    state: TaskState = TaskState.CREATED
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[Exception] = None


class KernelScheduler:
    """
    Task Scheduler manages task queues, allocation of compute resources, and task state transitions.
    """

    def __init__(self) -> None:
        self._queue: List[KernelTask] = []
        self._history: List[KernelTask] = []

    def submit_task(self, description: str, handler: Callable[[], Any], priority: int = 1) -> KernelTask:
        task = KernelTask(description=description, handler=handler, priority=priority, state=TaskState.QUEUED)
        self._queue.append(task)
        # Sort queue by priority (descending)
        self._queue.sort(key=lambda t: t.priority, reverse=True)
        return task

    def execute_next(self) -> Optional[KernelTask]:
        if not self._queue:
            return None

        task = self._queue.pop(0)
        task.state = TaskState.RUNNING

        try:
            if task.handler:
                task.result = task.handler()
            task.state = TaskState.COMPLETED
        except Exception as e:
            task.error = e
            task.state = TaskState.FAILED

        task.completed_at = time.time()
        self._history.append(task)
        return task

    def execute_all(self) -> List[KernelTask]:
        executed = []
        while self._queue:
            t = self.execute_next()
            if t:
                executed.append(t)
        return executed

    def get_pending_count(self) -> int:
        return len(self._queue)
