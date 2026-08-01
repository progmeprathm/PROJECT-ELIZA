"""
Layer 9: Reflector implementation responding to REFLECT Cognitive Instruction.
"""

from typing import Any, Dict, Optional

from ELIZA_OBJECTS import Experience, Outcome
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSReflector:
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.REFLECT, self._handle_reflect)

    def _handle_reflect(self, ins: CognitiveInstruction) -> Experience:
        outcome = ins.operand if isinstance(ins.operand, Outcome) else Outcome()
        return Experience(
            outcome_id=outcome.id,
            reflection_notes=f"Reflected on outcome {outcome.id}",
            lessons_learned=["Execution succeeded as expected"],
        )
