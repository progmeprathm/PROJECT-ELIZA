"""
Layer 10: ECOS Cognitive Operating System.
Orchestrates Compiler, CVM CPU, Memory Hierarchy, CFS, Process Scheduler, and Security.
"""

from typing import Any, Dict, List, Optional

from ecos.cfs.filesystem import CognitiveFilesystem
from ecos.compiler.compiler import CognitiveBytecodeProgram, CognitiveCompiler
from ecos.cvm.vm import CognitiveCPU
from ecos.memory.hierarchy import CognitiveMemoryHierarchy
from ecos.process.process import CognitiveProcess, ProcessScheduler


from llms.router import ModelRouter, TaskIntent


import uuid
from eliza.kernel.event_bus import RuntimeEventBus

class ECOSOperatingSystem:
    """
    ECOS Cognitive Operating System.
    "Everything runs here."
    """

    def __init__(self) -> None:
        self.runtime_id = f"runtime_{uuid.uuid4().hex[:8]}"
        self.event_bus = RuntimeEventBus(self.runtime_id)
        
        self.compiler = CognitiveCompiler()
        self.cpu = CognitiveCPU()
        self.memory_hierarchy = CognitiveMemoryHierarchy()
        self.cfs = CognitiveFilesystem()
        self.process_scheduler = ProcessScheduler()
        self.active_processes: Dict[int, CognitiveProcess] = {}
        self.model_router = ModelRouter(event_bus=self.event_bus, runtime_id=self.runtime_id)

    def boot(self) -> bool:
        self.cpu.isa_vm.clear()
        return True

    def run_goal(self, goal_statement: str, priority: int = 10) -> Dict[str, Any]:
        """
        Executes a high-level goal statement on the ECOS Operating System:
        Goal -> Cognitive Compiler -> Cognitive ISA Bytecode -> CVM CPU -> Memory & CFS.
        """
        # 1. Compile Goal to Bytecode
        program = self.compiler.compile_goal(goal_statement, priority)

        # 2. Create Process & Process Control Block
        goal_obj = program.instructions[4].operand if len(program.instructions) > 4 else None
        proc = self.process_scheduler.create_process(name=f"Proc-{program.program_id}", goal=goal_obj, priority=priority)

        # 3. Write to Cognitive Filesystem
        self.cfs.write(f"/goals/{proc.goal.id if proc.goal else 'goal'}", goal_statement)
        self.cfs.write(f"/plans/plan-{program.program_id}", program)

        # 4. Execute Program on Cognitive CPU
        cpu_result = self.cpu.execute_program(program)

        # 5. Store to Memory Hierarchy
        self.memory_hierarchy.store_tier("working_memory", key=f"run-{proc.pid}", value=cpu_result, importance=0.85)

        return {
            "pid": proc.pid,
            "program_id": program.program_id,
            "cpu_execution": cpu_result,
            "cfs_tree": self.cfs.get_full_tree(),
            "memory_summary": {k: v.current_count for k, v in self.memory_hierarchy.tiers.items()},
        }
