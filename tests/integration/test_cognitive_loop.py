"""
Integration test for full ELIZA Cognitive Pipeline.
"""

from eliza.executive.controller import ExecutiveController


def test_full_cognitive_cycle() -> None:
    controller = ExecutiveController()

    result = controller.execute_cognitive_cycle("Optimize memory consolidation parameters")

    assert result["cycle_id"] is not None
    assert result["goal"].description == "Address cognitive stimulus: 'Optimize memory consolidation parameters'"
    assert result["plan"] is not None
    assert result["simulation"] is not None
    assert result["risk_assessment"].compliant is True
    assert result["action"].executed is True
    assert result["explanation"].confidence.value > 0.0

    # Verify event bus history recorded all events
    history = controller.event_bus.get_history()
    event_names = [e.name for e in history]

    assert "ObservationReceived" in event_names
    assert "GoalCreated" in event_names
    assert "PlanGenerated" in event_names
    assert "SimulationCompleted" in event_names
    assert "ActionExecuted" in event_names
    assert "DecisionMade" in event_names
    assert "ReflectionCompleted" in event_names
    assert "LearningFinished" in event_names
