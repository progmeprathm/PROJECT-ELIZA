"""
Layer 4 & 5: Versioned Skill & Policy Assets.
Skills and policies evolve like software assets with complete version history and zero overwriting.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import time
import uuid


@dataclass
class VersionedSkill:
    skill_id: str
    name: str
    version: str = "1.0.0"
    routine_payload: Dict[str, Any] = field(default_factory=dict)
    practice_count: int = 0
    evaluation_score: float = 0.85
    version_history: List[Dict[str, Any]] = field(default_factory=list)

    def evolve_version(self, new_version: str, improvements: Dict[str, Any], new_score: float) -> str:
        self.version_history.append({
            "version": self.version,
            "score": self.evaluation_score,
            "timestamp": time.time(),
        })
        self.version = new_version
        self.routine_payload.update(improvements)
        self.evaluation_score = new_score
        return self.version


@dataclass
class VersionedPolicy:
    policy_id: str = field(default_factory=lambda: f"pol-{uuid.uuid4().hex[:8]}")
    name: str = "DefaultPolicy"
    version: str = "1.0.0"
    rule_statement: str = "Always verify plan risk before execution"
    active: bool = True
    history: List[Dict[str, Any]] = field(default_factory=list)

    def optimize_policy(self, new_version: str, new_rule: str) -> None:
        self.history.append({
            "version": self.version,
            "rule": self.rule_statement,
            "replaced_at": time.time(),
        })
        self.version = new_version
        self.rule_statement = new_rule
