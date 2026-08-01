# Python API & Object Reference

> **Single Source of Truth**: [`ELIZA_OBJECTS.py`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_OBJECTS.py) & [`ELIZA_INTERFACES.py`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_INTERFACES.py)

---

## 1. Single Source of Truth Cognitive Objects (`ELIZA_OBJECTS.py`)

- `Observation(id, source, modality, raw_data, confidence, timestamp)`
- `Evidence(id, supports, contradicts, strength, origin_observation_id)`
- `Belief(id, statement, confidence, supporting_evidence, contradicting_evidence, status)`
- `Knowledge(id, concept, associated_belief_ids, facts, rules)`
- `Goal(id, description, priority, deadline, dependencies, constraints, progress, owner, measurable_completion_criteria, status)`
- `Task(id, description, preconditions, resources, completion_criteria, status)`
- `Plan(id, goal_id, tasks, estimated_cost, estimated_duration, risk, dependencies, success_probability)`
- `Decision(id, alternatives, chosen_option, utility, confidence, justification)`
- `Action(id, plan_id, executor, tool, parameters, expected_outcome, observed_outcome)`
- `Outcome(id, action_id, success, metrics, side_effects, unexpected_events)`
- `Experience(id, outcome_id, reflection_notes, lessons_learned)`
- `Policy(id, name, rule, version, active)`
- `Memory(id, memory_type, payload, importance, retrieval_score, last_accessed, provenance)`
- `Entity(id, name, category, attributes)`
- `Relationship(id, source_entity_id, target_entity_id, relation_type, strength)`
- `WorldModel(id, entity_ids, relationship_ids, belief_ids, knowledge_ids)`

---

## 2. Abstract Base Class Contracts (`ELIZA_INTERFACES.py`)

- `MemoryModule`: `store()`, `retrieve()`, `forget()`, `consolidate()`
- `ReasonerModule`: `reason()`, `evaluate()`
- `PlannerModule`: `plan()`, `replan()`
- `SimulatorModule`: `simulate()`
- `SafetyModule`: `evaluate_action()`
- `LearnerModule`: `validate_learning()`

---

## 3. Cognitive ISA & Virtual Machine (`ecos/isa/instructions.py`)

- `CognitiveOpcode`: Enum with 20 primitive instructions.
- `CognitiveInstruction(instruction_id, opcode, operand, parameters, source_subsystem, target_subsystem, timestamp, status, result)`
- `CognitiveISAVirtualMachine`: Registers handlers and executes cognitive instructions.

---

## 4. ECOS Operating System Kernel (`ecos/os/kernel_os.py`)

- `ECOSOperatingSystem`:
  - `boot() -> bool`
  - `run_goal(goal_statement: str, priority: int) -> dict`
