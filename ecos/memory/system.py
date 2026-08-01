"""
Layer 4: Memory System implementation responding to RECALL, STORE, and FORGET Cognitive Instructions.
"""

from typing import Any, Dict, List, Optional
import time

from ELIZA_INTERFACES import MemoryModule
from ELIZA_OBJECTS import Memory
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


class ECOSMemorySystem(MemoryModule):
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None) -> None:
        self._store_dict: Dict[str, Memory] = {}
        self.vm = vm
        if self.vm:
            self._bind_isa_handlers()

    def _bind_isa_handlers(self) -> None:
        if not self.vm:
            return
        self.vm.register_handler(CognitiveOpcode.STORE, self._handle_store)
        self.vm.register_handler(CognitiveOpcode.RECALL, self._handle_recall)
        self.vm.register_handler(CognitiveOpcode.FORGET, self._handle_forget)

    def _handle_store(self, ins: CognitiveInstruction) -> Any:
        mem = ins.operand if isinstance(ins.operand, Memory) else Memory(payload=ins.operand, provenance=ins.source_subsystem)
        key = ins.parameters.get("key", mem.id)
        self.store(key=key, value=mem.payload, importance=mem.importance)
        return mem

    def _handle_recall(self, ins: CognitiveInstruction) -> List[Any]:
        query = str(ins.parameters.get("query", ins.operand or ""))
        limit = ins.parameters.get("limit", 10)
        return self.retrieve(query, limit)

    def _handle_forget(self, ins: CognitiveInstruction) -> bool:
        key = str(ins.operand or ins.parameters.get("key", ""))
        return self.forget(key)

    def store(self, key: str, value: Any, importance: float = 0.5) -> None:
        mem = Memory(id=key, payload=value, importance=importance, provenance="MemorySystem")
        self._store_dict[key] = mem

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        results = []
        for key, mem in self._store_dict.items():
            if query.lower() in key.lower() or query.lower() in str(mem.payload).lower():
                mem.last_accessed = time.time()
                results.append(mem.payload)
            if len(results) >= limit:
                break
        return results

    def forget(self, key: str) -> bool:
        if key in self._store_dict:
            del self._store_dict[key]
            return True
        return False

    def consolidate(self) -> None:
        pass
