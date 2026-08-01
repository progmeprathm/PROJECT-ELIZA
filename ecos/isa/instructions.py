"""
Cognitive Instruction Set Architecture (ISA) for ELIZA v1.0.
Phase 3 ECOS Runtime - 20 Primitive Opcodes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging
import time
import uuid

logger = logging.getLogger(__name__)


class CognitiveOpcode(str, Enum):
    """The 20 Primitive Cognitive Instruction Opcodes (Cognitive ISA)."""
    OBSERVE = "OBSERVE"
    ATTEND = "ATTEND"
    RECALL = "RECALL"
    STORE = "STORE"
    BELIEVE = "BELIEVE"
    QUESTION = "QUESTION"
    INFER = "INFER"
    PLAN = "PLAN"
    SIMULATE = "SIMULATE"
    DECIDE = "DECIDE"
    EXECUTE = "EXECUTE"
    REFLECT = "REFLECT"
    LEARN = "LEARN"
    REVISE = "REVISE"
    FORGET = "FORGET"
    PRIORITIZE = "PRIORITIZE"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    SUSPEND = "SUSPEND"
    RESUME = "RESUME"


@dataclass
class CognitiveInstruction:
    """Cognitive Instruction Envelope emitted and executed on the Cognitive ISA VM."""
    instruction_id: str = field(default_factory=lambda: f"ins-{uuid.uuid4().hex[:8]}")
    opcode: CognitiveOpcode = CognitiveOpcode.OBSERVE
    operand: Any = None  # Cognitive Object payload
    parameters: Dict[str, Any] = field(default_factory=dict)
    source_subsystem: str = "unknown"
    target_subsystem: str = "broadcast"
    timestamp: float = field(default_factory=time.time)
    status: str = "EMITTED"  # EMITTED, EXECUTED, FAILED
    result: Optional[Any] = None


class CognitiveISAVirtualMachine:
    """
    Virtual Machine that dispatches and executes Cognitive ISA Instructions across registered handlers.
    """

    def __init__(self) -> None:
        self._handlers: Dict[CognitiveOpcode, List[Callable[[CognitiveInstruction], Any]]] = {}
        self._instruction_history: List[CognitiveInstruction] = []

    def register_handler(self, opcode: CognitiveOpcode, handler: Callable[[CognitiveInstruction], Any]) -> None:
        if opcode not in self._handlers:
            self._handlers[opcode] = []
        self._handlers[opcode].append(handler)

    def execute_instruction(self, instruction: CognitiveInstruction) -> CognitiveInstruction:
        self._instruction_history.append(instruction)
        handlers = self._handlers.get(instruction.opcode, [])

        if not handlers:
            logger.warning(f"No handler registered for Cognitive ISA Opcode {instruction.opcode}")
            instruction.status = "NO_HANDLER"
            return instruction

        results = []
        for handler in handlers:
            try:
                res = handler(instruction)
                results.append(res)
            except Exception as e:
                logger.error(f"Error executing instruction {instruction.opcode}: {e}", exc_info=True)
                instruction.status = "FAILED"
                instruction.result = {"error": str(e)}
                return instruction

        instruction.status = "EXECUTED"
        instruction.result = results[0] if len(results) == 1 else results
        return instruction

    def get_history(self) -> List[CognitiveInstruction]:
        return list(self._instruction_history)

    def clear(self) -> None:
        self._handlers.clear()
        self._instruction_history.clear()
