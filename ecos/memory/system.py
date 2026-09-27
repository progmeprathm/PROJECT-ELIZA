"""
Layer 4: Memory System implementation responding to RECALL, STORE, and FORGET Cognitive Instructions.
Upgraded to support Semantic Vector Retrieval for v0.2.
"""

from typing import Any, Dict, List, Optional
import time
import math

from ELIZA_INTERFACES import MemoryModule
from ELIZA_OBJECTS import Memory
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode


import json
import urllib.request
import urllib.error
import os

class EmbeddingProvider:
    def embed(self, text: str) -> List[float]:
        raise NotImplementedError

class DeterministicPseudoEmbedding(EmbeddingProvider):
    def embed(self, text: str) -> List[float]:
        text = text.lower()
        vec = [0.0] * 128
        for c in text:
            idx = ord(c) % 128
            vec[idx] += 1.0
        norm = math.sqrt(sum(v*v for v in vec))
        if norm > 0:
            vec = [v/norm for v in vec]
        return vec

class RealEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.fallback = DeterministicPseudoEmbedding()
        self.fallback_used = False
        self.fallback_reason = ""
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.endpoint = os.environ.get("ELIZA_EMBEDDING_ENDPOINT", "https://api.openai.com/v1/embeddings")
        self.model = os.environ.get("ELIZA_EMBEDDING_MODEL", "text-embedding-3-small")

    def embed(self, text: str) -> List[float]:
        if not self.api_key:
            self.fallback_used = True
            self.fallback_reason = "No API key"
            return self.fallback.embed(text)
            
        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps({"input": text, "model": self.model}).encode("utf-8"),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                return res_body["data"][0]["embedding"]
        except Exception as e:
            self.fallback_used = True
            self.fallback_reason = str(e)
            return self.fallback.embed(text)

def get_embedding_provider() -> EmbeddingProvider:
    provider = os.environ.get("ELIZA_EMBEDDING_PROVIDER", "deterministic")
    if provider == "cloud":
        return RealEmbeddingProvider()
    return DeterministicPseudoEmbedding()

class ECOSMemorySystem(MemoryModule):
    def __init__(self, vm: Optional[CognitiveISAVirtualMachine] = None, router: Optional[Any] = None, embedding_provider: Optional[EmbeddingProvider] = None) -> None:
        self._store_dict: Dict[str, Memory] = {}
        self._vectors: Dict[str, List[float]] = {}
        self.vm = vm
        self.router = router
        self.embedding_provider = embedding_provider or get_embedding_provider()
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

    def _get_embedding(self, text: str) -> List[float]:
        return self.embedding_provider.embed(text)

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        if len(vec1) != len(vec2):
            return 0.0
        return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

    def store(self, key: str, value: Any, importance: float = 0.5) -> None:
        mem = Memory(id=key, payload=value, importance=importance, provenance="MemorySystem")
        self._store_dict[key] = mem
        embed_text = str(value)
        if isinstance(value, dict) and "observation" in value:
            embed_text = str(value["observation"])
        self._vectors[key] = self._get_embedding(embed_text)

    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        query_vec = self._get_embedding(query)
        
        # Calculate similarities
        scored_mems = []
        for key, mem in self._store_dict.items():
            vec = self._vectors.get(key, [0.0]*128)
            sim = self._cosine_similarity(query_vec, vec)
            scored_mems.append((sim, key, mem))
            
        # Sort by similarity descending
        scored_mems.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for sim, key, mem in scored_mems:
            if sim > 0.05: # Minimum threshold
                mem.last_accessed = time.time()
                results.append(mem.payload)
            if len(results) >= limit:
                break
                
        return results

    def forget(self, key: str) -> bool:
        if key in self._store_dict:
            del self._store_dict[key]
            if key in self._vectors:
                del self._vectors[key]
            return True
        return False

    def consolidate(self) -> None:
        pass
