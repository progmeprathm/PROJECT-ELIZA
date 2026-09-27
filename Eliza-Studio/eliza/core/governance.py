"""
Governance and Decision Provenance for ELIZA Cognitive Operating System.
Ensures every decision is inspectable and traceable (Article XIII, Axiom 6, Axiom 8).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

from eliza.core.types import Explanation, ProvenanceRecord


@dataclass
class DecisionAuditTrail:
    decision_id: str
    subsystem_provenance: List[ProvenanceRecord] = field(default_factory=list)
    explanation: Optional[Explanation] = None
    created_at: float = field(default_factory=time.time)


class GovernanceEngine:
    """Manages system governance, architecture ADR compliance, and decision auditing."""

    def __init__(self) -> None:
        self._audit_trails: Dict[str, DecisionAuditTrail] = {}

    def log_decision(self, decision_id: str, explanation: Explanation, provenance: List[ProvenanceRecord]) -> DecisionAuditTrail:
        trail = DecisionAuditTrail(
            decision_id=decision_id,
            subsystem_provenance=provenance,
            explanation=explanation,
        )
        self._audit_trails[decision_id] = trail
        return trail

    def get_audit_trail(self, decision_id: str) -> Optional[DecisionAuditTrail]:
        return self._audit_trails.get(decision_id)

    def verify_provenance(self, decision_id: str) -> bool:
        """Verifies that a decision has a complete, inspectable provenance record."""
        trail = self.get_audit_trail(decision_id)
        if not trail or not trail.explanation:
            return False
        return len(trail.subsystem_provenance) > 0 and len(trail.explanation.evidence) > 0
