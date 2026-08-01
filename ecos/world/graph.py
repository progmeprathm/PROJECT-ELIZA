"""
Layer 5: World Model Graph implementation responding to BELIEVE and REVISE Cognitive Instructions.
"""

from typing import Any, Dict, List, Optional

from ELIZA_OBJECTS import Belief, Entity, Relationship, WorldModel
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSWorldModel:
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self.world_model = WorldModel()
        self._beliefs: Dict[str, Belief] = {}
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.BELIEVE, self._handle_believe)
        self.vm.register_handler(CognitiveOpcode.REVISE, self._handle_revise)

    def _handle_believe(self, ins: CognitiveInstruction) -> Belief:
        b = ins.operand if isinstance(ins.operand, Belief) else Belief(statement=str(ins.operand), confidence=ins.parameters.get("confidence", 0.85))
        self._beliefs[b.id] = b
        self.world_model.belief_ids.append(b.id)
        return b

    def _handle_revise(self, ins: CognitiveInstruction) -> Optional[Belief]:
        belief_id = ins.parameters.get("belief_id")
        if belief_id in self._beliefs:
            b = self._beliefs[belief_id]
            b.confidence = ins.parameters.get("new_confidence", b.confidence)
            b.status = ins.parameters.get("new_status", b.status)
            return b
        return None

    def get_beliefs(self) -> List[Belief]:
        return list(self._beliefs.values())
