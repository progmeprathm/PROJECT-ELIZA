"""
Layer 3: Canonical State Machine Implementation.
IDLE -> PERCEIVING -> REASONING -> PLANNING -> SIMULATING -> EXECUTING -> LEARNING -> IDLE
"""

from enum import Enum
from typing import List


class StateStage(str, Enum):
    IDLE = "IDLE"
    PERCEIVING = "PERCEIVING"
    REASONING = "REASONING"
    PLANNING = "PLANNING"
    SIMULATING = "SIMULATING"
    EXECUTING = "EXECUTING"
    LEARNING = "LEARNING"


class CognitiveStateMachine:
    def __init__(self) -> None:
        self.current_state = StateStage.IDLE
        self._history: List[StateStage] = [StateStage.IDLE]

    def transition_to(self, target_state: StateStage) -> StateStage:
        self.current_state = target_state
        self._history.append(target_state)
        return self.current_state

    def get_history(self) -> List[StateStage]:
        return list(self._history)
