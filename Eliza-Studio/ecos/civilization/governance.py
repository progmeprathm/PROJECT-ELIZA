"""
Layer 4 & 5: Cognitive Governance and Reputation Engine.
Permissions, trust, identity, audit logs, conflict resolution, and reputation-based task routing.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

from ecos.civilization.minds import SpecializedMind


@dataclass
class AuditLogEntry:
    timestamp: float = field(default_factory=time.time)
    actor_id: str = "system"
    action: str = ""
    target: str = ""
    status: str = "PERMITTED"


class CognitiveGovernanceEngine:
    """Enforces permissions, identity verification, and conflict resolution across the ecosystem."""

    def __init__(self) -> None:
        self.audit_log: List[AuditLogEntry] = []
        self.trusted_identities: Dict[str, str] = {}

    def register_mind_identity(self, mind_id: str, role: str) -> None:
        self.trusted_identities[mind_id] = role
        self.log_audit(actor_id=mind_id, action="REGISTER_IDENTITY", target=role)

    def log_audit(self, actor_id: str, action: str, target: str, status: str = "PERMITTED") -> None:
        self.audit_log.append(AuditLogEntry(actor_id=actor_id, action=action, target=target, status=status))


class ReputationEngine:
    """
    Computes reputation scores (planning quality, prediction score, compliance) and routes tasks to top-ranked mind specialists.
    """

    def __init__(self) -> None:
        self._scores: Dict[str, float] = {}

    def update_reputation(self, mind_id: str, performance_score: float) -> float:
        current = self._scores.get(mind_id, 0.85)
        new_score = round(0.7 * current + 0.3 * performance_score, 4)
        self._scores[mind_id] = new_score
        return new_score

    def select_best_specialist(self, minds: List[SpecializedMind], required_role: str) -> Optional[SpecializedMind]:
        candidates = [m for m in minds if m.role.lower() == required_role.lower()]
        if not candidates:
            return None
        return max(candidates, key=lambda m: self._scores.get(m.mind_id, m.reputation_score))
