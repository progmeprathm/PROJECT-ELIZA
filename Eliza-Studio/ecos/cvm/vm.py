"""
Layer 1 & 8: Cognitive CPU & CVM Execution Engine.
Instruction Decoder -> Scheduler -> Memory Manager -> Reasoning Unit -> Planner -> Simulator -> Action Unit.
"""

from typing import Any, Dict, List, Optional

from ecos.compiler.compiler import CognitiveBytecodeProgram
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class CognitiveCPU:
    """
    Software CPU that decodes and executes Cognitive ISA Bytecode programs.
    Contains Instruction Decoder, Registers, and unit routing.
    """

    def __init__(self) -> None:
        self.isa_vm = CognitiveISAVirtualMachine()
        self.attention_register: Optional[Any] = None
        self.working_register: Optional[Any] = None
        self.pc = 0  # Program counter

    def execute_program(self, program: CognitiveBytecodeProgram) -> Dict[str, Any]:
        """Execute a compiled CognitiveBytecodeProgram sequentially on the Cognitive CPU."""
        self.pc = 0
        executed_results = []

        for ins in program.instructions:
            self.pc += 1

            # Update registers on specific opcodes
            if ins.opcode == CognitiveOpcode.ATTEND:
                self.attention_register = ins.operand
            elif ins.opcode == CognitiveOpcode.STORE:
                self.working_register = ins.operand

            res = self.isa_vm.execute_instruction(ins)
            executed_results.append({
                "pc": self.pc,
                "opcode": ins.opcode.value,
                "status": res.status,
                "result": res.result,
            })

        return {
            "program_id": program.program_id,
            "instructions_executed": len(executed_results),
            "trace": executed_results,
        }
