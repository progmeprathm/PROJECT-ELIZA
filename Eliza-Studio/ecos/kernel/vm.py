"""
Layer 1: ECOS Kernel VM for ELIZA v0.1.
Executes cognition by dispatching Cognitive ISA Instructions across registered subsystem handlers.
"The Kernel does not think. The Kernel makes thinking possible."
"""

from typing import Any, Dict, List, Optional

from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSVMKernel:
    def __init__(self) -> None:
        self.isa_vm = CognitiveISAVirtualMachine()
        self._booted = False

    def boot(self) -> bool:
        self._booted = True
        return True

    def dispatch_instruction(self, opcode: CognitiveOpcode, operand: Any = None, parameters: Optional[Dict[str, Any]] = None, source: str = "kernel") -> CognitiveInstruction:
        instruction = CognitiveInstruction(
            opcode=opcode,
            operand=operand,
            parameters=parameters or {},
            source_subsystem=source,
        )
        return self.isa_vm.execute_instruction(instruction)
