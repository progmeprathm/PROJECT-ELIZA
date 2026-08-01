"""
Layer 10 & 13: Experiment Framework and Human Collaboration Gateway.
Every cognitive architecture improvement is an experiment.
Humans retain final review, approval, annotation, and deployment sign-off.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class Experiment:
    experiment_id: str = field(default_factory=lambda: f"exp-{uuid.uuid4().hex[:8]}")
    hypothesis_statement: str = ""
    implementation_details: Dict[str, Any] = field(default_factory=dict)
    benchmark_baseline: float = 0.80
    benchmark_result: float = 0.0
    status: str = "PROPOSED"  # PROPOSED, RUNNING, CONCLUDED, ACCEPTED, REJECTED
    analysis_notes: str = ""


class ExperimentFramework:
    """Layer 10: Scientific Experiment Framework."""

    def run_experiment(self, hypothesis: str, benchmark_func: Any) -> Experiment:
        exp = Experiment(hypothesis_statement=hypothesis, status="RUNNING")
        res_score = benchmark_func()
        exp.benchmark_result = res_score

        if res_score > exp.benchmark_baseline:
            exp.status = "CONCLUDED"
            exp.analysis_notes = f"Hypothesis validated! Score improved from {exp.benchmark_baseline} to {res_score}."
        else:
            exp.status = "REJECTED"
            exp.analysis_notes = f"Hypothesis falsified. Score {res_score} did not exceed baseline {exp.benchmark_baseline}."

        return exp


class HumanCollaborationGateway:
    """Layer 13: Human Collaboration Gateway for review and approval."""

    def review_experiment(self, exp: Experiment, human_approver: str) -> bool:
        if exp.status == "CONCLUDED":
            exp.status = "ACCEPTED"
            exp.analysis_notes += f" (Approved by human: {human_approver})"
            return True
        return False
