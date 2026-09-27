"""
Layer 8: Cognitive Bytecode representation format.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid

from ecos.isa import CognitiveOpcode


@dataclass
class BytecodeInstruction:
    opcode: CognitiveOpcode
    operand: Any = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompiledCognitiveProgram:
    program_id: str = field(default_factory=lambda: f"prog-{uuid.uuid4().hex[:8]}")
    bytecode: List[BytecodeInstruction] = field(default_factory=list)
