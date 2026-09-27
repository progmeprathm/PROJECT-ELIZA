"""
Layer 2: 7-Tier Cognitive Memory Hierarchy.
Attention Register -> Working Memory -> Context Cache -> Episodic Memory -> Semantic Memory -> Knowledge Graph -> Long-Term Storage.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time

from ELIZA_OBJECTS import Memory


@dataclass
class MemoryTierInfo:
    tier_name: str
    latency_ms: float
    capacity_items: int
    current_count: int = 0


class CognitiveMemoryHierarchy:
    """
    7-Tier Cognitive Memory Stack with explicit access latencies, bounded capacities, and consolidation rules.
    """

    def __init__(self) -> None:
        self.tiers: Dict[str, MemoryTierInfo] = {
            "attention_register": MemoryTierInfo("Attention Register", latency_ms=0.1, capacity_items=1),
            "working_memory": MemoryTierInfo("Working Memory", latency_ms=1.0, capacity_items=10),
            "context_cache": MemoryTierInfo("Context Cache", latency_ms=5.0, capacity_items=50),
            "episodic_memory": MemoryTierInfo("Episodic Memory", latency_ms=15.0, capacity_items=500),
            "semantic_memory": MemoryTierInfo("Semantic Memory", latency_ms=25.0, capacity_items=5000),
            "knowledge_graph": MemoryTierInfo("Knowledge Graph", latency_ms=50.0, capacity_items=50000),
            "long_term_storage": MemoryTierInfo("Long-Term Storage", latency_ms=100.0, capacity_items=999999999),
        }

        self._store: Dict[str, Dict[str, Memory]] = {tier: {} for tier in self.tiers}

    def store_tier(self, tier_name: str, key: str, value: Any, importance: float = 0.5) -> bool:
        if tier_name not in self.tiers:
            raise ValueError(f"Unknown memory tier '{tier_name}'")

        tier_info = self.tiers[tier_name]
        store_dict = self._store[tier_name]

        # Enforce capacity
        if len(store_dict) >= tier_info.capacity_items:
            # Evict oldest item
            oldest_key = min(store_dict.keys(), key=lambda k: store_dict[k].last_accessed)
            del store_dict[oldest_key]

        mem = Memory(id=key, memory_type=tier_name, payload=value, importance=importance, provenance="MemoryHierarchy")
        store_dict[key] = mem
        tier_info.current_count = len(store_dict)
        return True

    def retrieve_tier(self, tier_name: str, query: str, limit: int = 10) -> List[Any]:
        if tier_name not in self.tiers:
            return []

        store_dict = self._store[tier_name]
        results = []
        for key, mem in store_dict.items():
            if query.lower() in key.lower() or query.lower() in str(mem.payload).lower():
                mem.last_accessed = time.time()
                results.append(mem.payload)
            if len(results) >= limit:
                break
        return results

    def consolidate_hierarchical(self) -> Dict[str, int]:
        """Consolidates items down the memory stack based on importance and access history."""
        consolidated_counts = {}
        # Working -> Episodic / Long Term
        wm_store = self._store["working_memory"]
        to_promote = [k for k, m in wm_store.items() if m.importance > 0.70]
        for k in to_promote:
            item = wm_store[k]
            self.store_tier("long_term_storage", k, item.payload, item.importance)
        consolidated_counts["promoted_to_long_term"] = len(to_promote)
        return consolidated_counts
