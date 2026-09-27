"""
Layer 3 & 8: Distributed World Model and Knowledge Federation.
Multi-tier graph: Local -> Regional -> Domain -> Shared Knowledge.
Private local memories remain private unless explicitly published via the Federation Gateway.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ELIZA_OBJECTS import Belief, Knowledge, WorldModel


class DistributedWorldModel:
    """Multi-tiered knowledge graph hierarchy."""

    def __init__(self) -> None:
        self.local_knowledge: List[Knowledge] = []
        self.regional_knowledge: List[Knowledge] = []
        self.domain_knowledge: List[Knowledge] = []
        self.shared_knowledge: List[Knowledge] = []

    def publish_to_shared(self, knowledge: Knowledge, validation_score: float = 0.90) -> bool:
        if validation_score >= 0.85:
            self.shared_knowledge.append(knowledge)
            return True
        return False


class KnowledgeFederationGateway:
    """Selective knowledge sharing and publishing gateway."""

    def __init__(self, dwm: DistributedWorldModel) -> None:
        self.dwm = dwm
        self.published_catalog: Dict[str, Knowledge] = {}

    def federate_item(self, concept: str, facts: List[str], score: float = 0.92) -> bool:
        kn = Knowledge(concept=concept, facts=facts)
        success = self.dwm.publish_to_shared(kn, validation_score=score)
        if success:
            self.published_catalog[kn.id] = kn
        return success
