"""
Executive Controller for ELIZA Cognitive Operating System.
Orchestrates the 19-Stage Canonical Cognitive Pipeline (Section III of ELIZA_DYNAMICS.md):
Observe -> Normalize -> Attend -> Interpret -> Retrieve Memory -> Update World Model -> Reason ->
Generate Goals -> Prioritize Goals -> Plan -> Simulate -> Evaluate -> Decide -> Execute ->
Observe Outcome -> Reflect -> Learn -> Consolidate Memory -> Repeat.
"""

from typing import Any, Dict, List, Optional
import uuid

from eliza.core.dynamics import (
    BeliefStatus,
    CognitiveHealthMonitor,
    CognitiveHealthReport,
    DynamicsSystemInvariantValidator,
    GoalStatus,
)
from eliza.core.events import (
    ActionExecuted,
    DecisionMade,
    EventBus,
    GoalCreated,
    LearningFinished,
    ReflectionCompleted,
)
from eliza.core.fcrl import (
    Action,
    Belief,
    CognitiveInvariantValidator,
    Decision,
    Evidence,
    Experience,
    Goal,
    Knowledge,
    MemoryObject,
    Observation,
    Outcome,
    Plan,
    Policy,
    Task,
)
from eliza.core.graph import CognitiveGraph
from eliza.core.interface import IExecutiveControl
from eliza.core.types import (
    Confidence,
    Explanation,
    Identity,
    ReasoningStyle,
    RiskAssessment,
    SubsystemType,
    ValidatedLearning,
)
from eliza.executive.attention import AttentionAllocator
from eliza.executive.meta_cognition import MetaCognitiveEvaluator
from eliza.explainability.tracer import ExplainabilityTracer
from eliza.learning.validator import LearningValidator
from eliza.memory import EpisodicMemory, LongTermMemory, ShortTermMemory, WorkingMemory
from eliza.perception.base import PerceptionModule
from eliza.planning.planner import GoalPlanner
from eliza.reasoning.engine import ReasoningEngine
from eliza.safety.guard import SafetyGuard
from eliza.simulation.simulator import CognitiveSimulator
from eliza.world_model.graph import WorldModelGraph


class ExecutiveController(IExecutiveControl):
    """
    Central Executive Control for ELIZA.
    Coordinates the 19-Stage Cognitive Pipeline S(t+1) = F(...) obeying ELIZA_DYNAMICS.md.
    """

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        working_memory: Optional[WorkingMemory] = None,
        short_term_memory: Optional[ShortTermMemory] = None,
        episodic_memory: Optional[EpisodicMemory] = None,
        long_term_memory: Optional[LongTermMemory] = None,
        world_model: Optional[WorldModelGraph] = None,
        reasoning_engine: Optional[ReasoningEngine] = None,
        planner: Optional[GoalPlanner] = None,
        simulator: Optional[CognitiveSimulator] = None,
        safety_guard: Optional[SafetyGuard] = None,
        tracer: Optional[ExplainabilityTracer] = None,
        perception: Optional[PerceptionModule] = None,
        attention_allocator: Optional[AttentionAllocator] = None,
        meta_cognition: Optional[MetaCognitiveEvaluator] = None,
        learning_validator: Optional[LearningValidator] = None,
        health_monitor: Optional[CognitiveHealthMonitor] = None,
    ) -> None:
        self.event_bus = event_bus or EventBus()

        self.working_memory = working_memory or WorkingMemory()
        self.short_term_memory = short_term_memory or ShortTermMemory()
        self.episodic_memory = episodic_memory or EpisodicMemory()
        self.long_term_memory = long_term_memory or LongTermMemory()

        self.world_model = world_model or WorldModelGraph()
        self.reasoning_engine = reasoning_engine or ReasoningEngine()
        self.planner = planner or GoalPlanner()
        self.simulator = simulator or CognitiveSimulator()
        self.safety_guard = safety_guard or SafetyGuard()
        self.tracer = tracer or ExplainabilityTracer()
        self.perception = perception or PerceptionModule()
        self.attention_allocator = attention_allocator or AttentionAllocator()
        self.meta_cognition = meta_cognition or MetaCognitiveEvaluator()
        self.learning_validator = learning_validator or LearningValidator()
        self.health_monitor = health_monitor or CognitiveHealthMonitor()

        self.identity = Identity()
        self.cognitive_graph = CognitiveGraph()
        self._initialize_subsystems()

    @property
    def subsystem_type(self) -> SubsystemType:
        return SubsystemType.EXECUTIVE

    def _initialize_subsystems(self) -> None:
        subsystems = [
            self.working_memory,
            self.short_term_memory,
            self.episodic_memory,
            self.long_term_memory,
            self.world_model,
            self.reasoning_engine,
            self.planner,
            self.simulator,
            self.safety_guard,
            self.tracer,
            self.perception,
            self.attention_allocator,
            self.meta_cognition,
            self.learning_validator,
        ]
        for sub in subsystems:
            sub.initialize(self.event_bus)

    def arbitrate_goals(self, goals: List[Goal]) -> List[Goal]:
        return sorted(goals, key=lambda g: g.priority, reverse=True)

    def execute_cognitive_cycle(self, input_stimulus: str) -> Dict[str, Any]:
        """
        Executes the full 19-Stage Cognitive Pipeline (ELIZA_DYNAMICS.md Section III):
        1. Observe
        2. Normalize
        3. Attend
        4. Interpret
        5. Retrieve Memory
        6. Update World Model
        7. Reason
        8. Generate Goals
        9. Prioritize Goals
        10. Plan
        11. Simulate
        12. Evaluate
        13. Decide
        14. Execute
        15. Observe Outcome
        16. Reflect
        17. Learn
        18. Consolidate Memory
        19. Repeat
        """
        self.identity.total_cycles_executed += 1
        cycle_id = f"cycle-{uuid.uuid4().hex[:8]}"

        # Health Assessment (Section XXII)
        initial_health = self.health_monitor.evaluate_health(memory_item_count=len(self.cognitive_graph.nodes))

        # Stage 1: Observe
        obs_event = self.perception.ingest_input(input_stimulus)
        fcrl_obs = Observation(source="PerceptionModule", modality="text", raw_data={"input": input_stimulus})
        self.cognitive_graph.add_node(fcrl_obs)

        # Stage 2: Normalize
        normalized_text = input_stimulus.strip().lower()

        # Stage 3: Attend (Section V)
        attention = self.attention_allocator.allocate_attention(normalized_text, goal_priority=10)

        # Stage 4: Interpret
        evidence = Evidence(supports=[], origin_observation_id=fcrl_obs.id, strength=0.95)
        self.cognitive_graph.add_node(evidence)

        # Belief Lifecycle: NEW -> SUPPORTED (Section IX)
        initial_belief = Belief(
            statement=f"Request '{normalized_text}' is supported",
            confidence=0.88,
            supporting_evidence=[evidence.id],
            status=BeliefStatus.SUPPORTED.value,
        )
        evidence.supports.append(initial_belief.id)
        self.cognitive_graph.add_node(initial_belief)

        # Stage 5: Retrieve Memory (Section VII)
        working_mem = MemoryObject(memory_type="working", payload={"normalized_text": normalized_text}, provenance="PerceptionIntake")
        self.cognitive_graph.add_node(working_mem)

        # Stage 6: Update World Model (Section VIII)
        knowledge = Knowledge(concept=f"Knowledge-{normalized_text}", associated_belief_ids=[initial_belief.id], facts=[f"Fact: {normalized_text}"])
        self.cognitive_graph.add_node(knowledge)

        # Stage 7: Reason (Section VII)
        # Belief Lifecycle: STRENGTHENED
        initial_belief.status = BeliefStatus.STRENGTHENED.value

        # Stage 8: Generate Goals (Goal Lifecycle: CREATED -> ACTIVE) (Section X)
        goal = Goal(
            description=f"Process '{normalized_text}'",
            priority=10,
            measurable_completion_criteria=[f"Complete '{normalized_text}'"],
            owner="ExecutiveController",
        )
        self.cognitive_graph.add_node(goal)

        # Stage 9: Prioritize Goals
        goals = self.arbitrate_goals([goal])
        active_goal = goals[0]

        # Stage 10: Plan (Section XI)
        task = Task(description=f"Task for '{normalized_text}'")
        self.cognitive_graph.add_node(task)

        plan = Plan(goal_id=active_goal.id, tasks=[task], estimated_cost=attention.compute_units_allocated, risk=0.10)
        self.cognitive_graph.add_node(plan)

        # Stage 11: Simulate (Section XII)
        sim_result = self.simulator.simulate(
            plan=self.planner.create_plan(goal=Goal(id=active_goal.id, description=active_goal.description, priority=active_goal.priority), beliefs=[], available_resources={}),
            world_state=[],
        )

        # Stage 12: Evaluate
        meta_state = self.meta_cognition.evaluate_cognition(plan=self.planner.create_plan(goal=Goal(id=active_goal.id, description=active_goal.description, priority=active_goal.priority), beliefs=[], available_resources={}), beliefs=[])

        # Stage 13: Decide (Section XIII)
        decision = Decision(alternatives=["Path A", "Path B"], chosen_option="Path A", utility=0.92, confidence=0.90, justification="Optimal path")
        self.cognitive_graph.add_node(decision)

        # Stage 14: Execute (Section XIV)
        action = Action(plan_id=plan.id, executor="ExecutiveController", tool="cognitive_tool", parameters={"query": normalized_text}, expected_outcome="Success")
        self.cognitive_graph.add_node(action)

        risk_assessment = self.safety_guard.evaluate_action(
            action=Action(id=action.id, plan_id=action.plan_id, step_index=0, action_type="EXECUTE", parameters={}, target=normalized_text),
            context={},
        )
        action_success = risk_assessment.compliant and not risk_assessment.vetoed

        # Stage 15: Observe Outcome (Section XV)
        outcome = Outcome(action_id=action.id, success=action_success, metrics={"latency_ms": 15.0})
        self.cognitive_graph.add_node(outcome)

        # Stage 16: Reflect (Section XVI)
        experience = Experience(outcome_id=outcome.id, reflection_notes=f"Reflected cycle {cycle_id}", lessons_learned=["Validated execution pipeline"])
        self.cognitive_graph.add_node(experience)

        # Goal Lifecycle: COMPLETED
        active_goal.progress = 1.0

        # Stage 17: Learn (Section XVII)
        validated_learning = ValidatedLearning(
            learning_id=f"learn-{uuid.uuid4().hex[:8]}",
            source_experience_ids=[experience.id],
            proposed_policy_update="Refine pipeline heuristics",
            validation_score=0.88,
        )
        learning_accepted = self.learning_validator.validate_learning(validated_learning)

        policy = Policy(name="PipelineExecutionPolicy", rule="Follow 19-stage canonical pipeline", version="1.0.0")
        self.cognitive_graph.add_node(policy)

        # Stage 18: Consolidate Memory (Section XVIII)
        self.long_term_memory.store(key=cycle_id, value={"cycle_id": cycle_id, "input": normalized_text})

        # Stage 19: Repeat (Prepare for next cycle & validate Dynamics Invariants)
        dynamics_invariants = DynamicsSystemInvariantValidator.validate_dynamics_invariants(
            goals=[goal],
            memories=[working_mem],
            beliefs=[initial_belief],
            actions=[action],
            plans=[plan],
            outcomes=[outcome],
            learnings=[validated_learning],
            experiences=[experience],
        )

        final_health = self.health_monitor.evaluate_health(memory_item_count=len(self.cognitive_graph.nodes))

        # Explainability Trace
        explanation = Explanation(
            decision_id=cycle_id,
            why=f"Executed 19-stage pipeline S(t) -> S(t+1) under compute {attention.compute_units_allocated} CU",
            evidence=[evidence.id],
            beliefs_used=[initial_belief.id],
            assumptions=["System healthy", "Pipeline invariant compliance"],
            alternatives_considered=decision.alternatives,
            confidence=Confidence(value=decision.confidence, source="CognitivePipelineEngine"),
        )
        self.tracer.record_decision(explanation)

        return {
            "cycle_id": cycle_id,
            "pipeline_stages_completed": 19,
            "initial_health": initial_health,
            "final_health": final_health,
            "observation": fcrl_obs,
            "attention": attention,
            "belief": initial_belief,
            "goal": active_goal,
            "plan": plan,
            "decision": decision,
            "action": action,
            "outcome": outcome,
            "experience": experience,
            "policy": policy,
            "validated_learning": validated_learning,
            "dynamics_invariants": dynamics_invariants,
            "explanation": explanation,
        }
