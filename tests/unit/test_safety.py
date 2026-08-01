"""
Unit tests for ELIZA Safety Guard (Article XII & Axiom 8).
"""

from eliza.core.types import Action
from eliza.safety.guard import SafetyGuard


def test_safety_veto_forbidden_action() -> None:
    guard = SafetyGuard()

    forbidden_action = Action(
        id="act-1",
        plan_id="plan-1",
        step_index=0,
        action_type="BYPASS_SAFETY",
        parameters={},
        target="Bypass system restrictions",
    )

    assessment = guard.evaluate_action(forbidden_action, context={})

    assert assessment.compliant is False
    assert assessment.vetoed is True
    assert "Forbidden action type" in assessment.reason


def test_safety_veto_high_risk() -> None:
    guard = SafetyGuard(max_risk_threshold=0.50)

    risky_action = Action(
        id="act-2",
        plan_id="plan-1",
        step_index=0,
        action_type="HIGH_COMPUTE_STRESS",
        parameters={"estimated_risk": 0.85},
        target="Stress test CPU",
    )

    assessment = guard.evaluate_action(risky_action, context={})

    assert assessment.compliant is False
    assert assessment.vetoed is True
    assert "exceeds maximum threshold" in assessment.reason
