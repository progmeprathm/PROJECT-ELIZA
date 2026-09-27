"""
ECOS Kernel State Manager and Checkpointer.
Enforces Section XI, XIII, and XIV of ELIZA_KERNEL_SPEC.md.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import copy
import time
import uuid


@dataclass
class KernelCheckpoint:
    checkpoint_id: str = field(default_factory=lambda: f"chk-{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)
    global_state: Dict[str, Any] = field(default_factory=dict)
    module_states: Dict[str, Any] = field(default_factory=dict)
    working_memory_state: Dict[str, Any] = field(default_factory=dict)
    recovery_metadata: Dict[str, Any] = field(default_factory=dict)


class StateManager:
    """
    Manages global state, module state, and periodic checkpoint creation/restoration (Section XIV).
    State updates are transactional.
    """

    def __init__(self) -> None:
        self._global_state: Dict[str, Any] = {}
        self._module_states: Dict[str, Dict[str, Any]] = {}
        self._checkpoints: Dict[str, KernelCheckpoint] = {}

    def set_global(self, key: str, value: Any) -> None:
        self._global_state[key] = value

    def get_global(self, key: str, default: Any = None) -> Any:
        return self._global_state.get(key, default)

    def set_module_state(self, module_id: str, state_dict: Dict[str, Any]) -> None:
        self._module_states[module_id] = copy.deepcopy(state_dict)

    def create_checkpoint(self, metadata: Optional[Dict[str, Any]] = None) -> KernelCheckpoint:
        chk = KernelCheckpoint(
            global_state=copy.deepcopy(self._global_state),
            module_states=copy.deepcopy(self._module_states),
            recovery_metadata=metadata or {},
        )
        self._checkpoints[chk.checkpoint_id] = chk
        return chk

    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        chk = self._checkpoints.get(checkpoint_id)
        if not chk:
            return False
        self._global_state = copy.deepcopy(chk.global_state)
        self._module_states = copy.deepcopy(chk.module_states)
        return True
