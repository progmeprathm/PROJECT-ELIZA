"""
Layer 5 & 6: Cognitive Process & Thread Control.
Processes have PIDs, goals, priorities, resources, and independent multi-threaded subroutines.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time
import uuid

from ELIZA_OBJECTS import Goal


@dataclass
class CognitiveThread:
    thread_id: str = field(default_factory=lambda: f"th-{uuid.uuid4().hex[:6]}")
    name: str = "subroutine"
    task: Optional[Callable[[], Any]] = None
    status: str = "CREATED"  # CREATED, RUNNING, COMPLETED, FAILED
    result: Optional[Any] = None


@dataclass
class CognitiveProcess:
    pid: int
    name: str
    goal: Goal
    priority: int = 10
    state: str = "RUNNING"  # RUNNING, PAUSED, SUSPENDED, TERMINATED
    threads: List[CognitiveThread] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def spawn_thread(self, name: str, task: Callable[[], Any]) -> CognitiveThread:
        th = CognitiveThread(name=name, task=task)
        self.threads.append(th)
        return th

    def execute_threads(self) -> List[Any]:
        results = []
        for th in self.threads:
            if th.task:
                th.status = "RUNNING"
                try:
                    th.result = th.task()
                    th.status = "COMPLETED"
                except Exception as e:
                    th.status = "FAILED"
                    th.result = {"error": str(e)}
                results.append(th.result)
        return results


class ProcessScheduler:
    """Schedules and manages cognitive processes by PID."""

    def __init__(self) -> None:
        self._processes: Dict[int, CognitiveProcess] = {}
        self._next_pid = 100

    def create_process(self, name: str, goal: Goal, priority: int = 10) -> CognitiveProcess:
        pid = self._next_pid
        self._next_pid += 1
        proc = CognitiveProcess(pid=pid, name=name, goal=goal, priority=priority)
        self._processes[pid] = proc
        return proc

    def get_process(self, pid: int) -> Optional[CognitiveProcess]:
        return self._processes.get(pid)

    def list_processes(self) -> List[CognitiveProcess]:
        return list(self._processes.values())
