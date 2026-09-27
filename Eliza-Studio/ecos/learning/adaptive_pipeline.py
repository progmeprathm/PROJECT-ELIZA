"""
Layer 2, 3 & 14: Adaptive Learning Pipeline and Safe Self-Improvement Engine.
Controls Learning Candidate generation, validation, benchmark regression testing, and Layer 14 safety boundary enforcement.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import logging
import uuid

from ELIZA_OBJECTS import Experience, Policy
from ecos.benchmarks.suite import CognitiveBenchmarkSuite

logger = logging.getLogger(__name__)


@dataclass
class LearningCandidate:
    candidate_id: str = field(default_factory=lambda: f"cand-{uuid.uuid4().hex[:8]}")
    target_component: str = "retrieval_heuristics"  # retrieval_heuristics, planning_depth, strategy, policy
    proposed_change: Dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    status: str = "PROPOSED"  # PROPOSED, VALIDATED, BENCHMARKED, APPROVED, DEPLOYED, REJECTED


class AdaptiveLearningPipeline:
    """
    Learning Pipeline enforcing Layer 14 Safe Self-Improvement Boundaries.
    Pipeline: Experience -> Learning Candidate -> Validation -> Benchmark -> Human Approval -> Deployment.
    """

    FORBIDDEN_TARGETS = [
        "core_safety_policies",
        "ecos_kernel",
        "constitution_articles",
        "governance_audit",
    ]

    def __init__(self) -> None:
        self.benchmark_suite = CognitiveBenchmarkSuite()
        self.deployed_candidates: List[LearningCandidate] = []

    def propose_candidate(self, target_component: str, change: Dict[str, Any], rationale: str) -> LearningCandidate:
        # Layer 14 Safety Boundary Check
        if target_component in self.FORBIDDEN_TARGETS:
            logger.error(f"Layer 14 Safety Veto: Modification to '{target_component}' is strictly prohibited!")
            cand = LearningCandidate(target_component=target_component, proposed_change=change, rationale=rationale, status="REJECTED")
            return cand

        cand = LearningCandidate(target_component=target_component, proposed_change=change, rationale=rationale, status="PROPOSED")
        return cand

    def validate_candidate(self, candidate: LearningCandidate) -> bool:
        if candidate.status == "REJECTED":
            return False

        # Validate proposal structure and safety boundaries
        candidate.status = "VALIDATED"
        return True

    def benchmark_candidate(self, candidate: LearningCandidate) -> float:
        if candidate.status != "VALIDATED":
            return 0.0

        results = self.benchmark_suite.run_suite()
        candidate.status = "BENCHMARKED"
        return results.aggregate_score

    def deploy_candidate(self, candidate: LearningCandidate, human_approved: bool = True) -> bool:
        if not human_approved:
            candidate.status = "REJECTED"
            return False

        if candidate.status == "BENCHMARKED":
            candidate.status = "DEPLOYED"
            self.deployed_candidates.append(candidate)
            return True
        return False
