"""
Layer 10: Learner implementation responding to LEARN Cognitive Instruction.
"""

from typing import Optional

from ELIZA_INTERFACES import LearnerModule
from ELIZA_OBJECTS import Experience, Policy
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSLearner(LearnerModule):
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.LEARN, self._handle_learn)

    def _handle_learn(self, ins: CognitiveInstruction) -> Policy:
        exp = ins.operand if isinstance(ins.operand, Experience) else Experience()
        policy = Policy(
            name="LearnedPolicy",
            rule=f"Updated rule based on experience {exp.id}",
            version="1.0.1",
        )
        return policy

    def validate_learning(self, candidate_policy: Policy) -> bool:
        return candidate_policy.version != ""

    def update_policy(self, policy: Policy) -> None:
        pass
