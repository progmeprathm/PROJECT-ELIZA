"""
Layer 6: Reasoning Engine implementation responding to INFER and QUESTION Cognitive Instructions.
"""

from typing import Any, Dict, List, Optional

from ELIZA_INTERFACES import ReasonerModule
from ELIZA_OBJECTS import Belief
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSReasoner(ReasonerModule):
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.INFER, self._handle_infer)
        self.vm.register_handler(CognitiveOpcode.QUESTION, self._handle_question)

    def _handle_infer(self, ins: CognitiveInstruction) -> List[Belief]:
        beliefs = ins.operand if isinstance(ins.operand, list) else []
        style = ins.parameters.get("style", "deductive")
        return self.reason(beliefs, style)

    def _handle_question(self, ins: CognitiveInstruction) -> Dict[str, Any]:
        return {"question": str(ins.operand), "status": "QUESTIONED"}

    def reason(self, beliefs: List[Belief], style: str = "deductive") -> List[Belief]:
        inferred = Belief(
            statement=f"Inferred belief via {style} style from {len(beliefs)} premises",
            confidence=0.90,
            status="supported",
        )
        return [inferred]

    def evaluate(self, statement: str, evidence_ids: List[str]) -> float:
        return 0.85
