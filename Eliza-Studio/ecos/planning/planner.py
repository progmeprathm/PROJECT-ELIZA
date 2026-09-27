"""
Layer 7: Planner implementation responding to PLAN and PRIORITIZE Cognitive Instructions.
"""

from typing import Any, Dict, List, Optional

from ELIZA_INTERFACES import PlannerModule
from ELIZA_OBJECTS import Belief, Goal, Plan, Task
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSPlanner(PlannerModule):
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.PLAN, self._handle_plan)
        self.vm.register_handler(CognitiveOpcode.PRIORITIZE, self._handle_prioritize)

    def _handle_plan(self, ins: CognitiveInstruction) -> Plan:
        goal = ins.operand if isinstance(ins.operand, Goal) else Goal(description=str(ins.operand))
        beliefs = ins.parameters.get("beliefs", [])
        return self.plan(goal, beliefs)

    def _handle_prioritize(self, ins: CognitiveInstruction) -> List[Goal]:
        goals = ins.operand if isinstance(ins.operand, list) else []
        return sorted(goals, key=lambda g: g.priority, reverse=True)

    def plan(self, goal: Goal, beliefs: List[Belief]) -> Plan:
        t = Task(description=f"Task for goal: '{goal.description}'")
        return Plan(goal_id=goal.id, tasks=[t], estimated_cost=1.0, risk=0.10)

    def replan(self, failed_plan_id: str, new_constraints: List[str]) -> Plan:
        return Plan(goal_id="replanned_goal", tasks=[], estimated_cost=2.0, risk=0.20)
