# ELIZA Schema Specification (Single Source of Truth)

> **Version**: 1.0.0 (Phase 2 Executable Architecture)  
> **Status**: Canonical Schema Reference

This document is the conceptual single source of truth for every cognitive object in ELIZA. Every Python class in `ELIZA_OBJECTS.py` and `ecos/schemas/objects.py` directly mirrors these schemas.

---

## 1. Observation
Raw information received from perception.
- `id`: `str` (UUID)
- `source`: `str`
- `modality`: `str`
- `raw_data`: `dict`
- `confidence`: `float` (0.0 to 1.0)
- `timestamp`: `float`

## 2. Evidence
Validated observations supporting or contradicting beliefs.
- `id`: `str`
- `supports`: `list[str]` (Belief IDs)
- `contradicts`: `list[str]` (Belief IDs)
- `strength`: `float` (0.0 to 1.0)
- `origin_observation_id`: `str`

## 3. Belief
Probabilistic interpretation of available evidence.
- `id`: `str`
- `statement`: `str`
- `confidence`: `float`
- `supporting_evidence`: `list[str]`
- `contradicting_evidence`: `list[str]`
- `status`: `str` ("new", "supported", "strengthened", "questioned", "revised", "rejected", "archived")

## 4. Knowledge
Validated beliefs organized for reasoning.
- `id`: `str`
- `concept`: `str`
- `associated_belief_ids`: `list[str]`
- `facts`: `list[str]`
- `rules`: `list[str]`

## 5. Goal
Desired future world state.
- `id`: `str`
- `description`: `str`
- `priority`: `int`
- `deadline`: `optional[float]`
- `dependencies`: `list[str]`
- `constraints`: `list[str]`
- `progress`: `float`
- `owner`: `str`
- `measurable_completion_criteria`: `list[str]`
- `status`: `str` ("created", "queued", "active", "blocked", "suspended", "completed", "cancelled", "archived")

## 6. Task
Atomic executable unit of a plan.
- `id`: `str`
- `description`: `str`
- `preconditions`: `list[str]`
- `resources`: `dict[str, float]`
- `completion_criteria`: `str`
- `status`: `str` ("created", "queued", "running", "waiting", "blocked", "completed", "failed", "cancelled")

## 7. Plan
Ordered strategy for satisfying goals.
- `id`: `str`
- `goal_id`: `str`
- `tasks`: `list[Task]`
- `estimated_cost`: `float`
- `estimated_duration`: `float`
- `risk`: `float`
- `dependencies`: `list[str]`
- `success_probability`: `float`

## 8. Decision
Selection among competing alternatives under constraints.
- `id`: `str`
- `alternatives`: `list[str]`
- `chosen_option`: `str`
- `utility`: `float`
- `confidence`: `float`
- `justification`: `str`

## 9. Action
Operation affecting the environment or internal state.
- `id`: `str`
- `plan_id`: `str`
- `executor`: `str`
- `tool`: `str`
- `parameters`: `dict`
- `expected_outcome`: `str`
- `observed_outcome`: `optional[str]`

## 10. Outcome
Observed consequences of action execution.
- `id`: `str`
- `action_id`: `str`
- `success`: `bool`
- `metrics`: `dict[str, float]`
- `side_effects`: `list[str]`
- `unexpected_events`: `list[str]`

## 11. Experience
Outcome interpreted through reflection.
- `id`: `str`
- `outcome_id`: `str`
- `reflection_notes`: `str`
- `lessons_learned`: `list[str]`

## 12. Policy
Persistent behavioral rule.
- `id`: `str`
- `name`: `str`
- `rule`: `str`
- `version`: `str`
- `active`: `bool`

## 13. Memory
Container for memory objects across the 6 tiers.
- `id`: `str`
- `memory_type`: `str` ("working", "short_term", "semantic", "episodic", "procedural", "long_term")
- `payload`: `any`
- `importance`: `float`
- `retrieval_score`: `float`
- `last_accessed`: `float`
- `provenance`: `str`

## 14. Entity
Representation of things in reality.
- `id`: `str`
- `name`: `str`
- `category`: `str`
- `attributes`: `dict`

## 15. Relationship
Semantic connection between entities.
- `id`: `str`
- `source_entity_id`: `str`
- `target_entity_id`: `str`
- `relation_type`: `str`
- `strength`: `float`

## 16. Context
Contextual interpretation frame.
- `id`: `str`
- `location`: `str`
- `time_scope`: `float`
- `participants`: `list[str]`
- `environment`: `dict`
- `active_goal_ids`: `list[str]`
- `available_resources`: `dict[str, float]`

## 17. WorldModel
State graph representing reality.
- `id`: `str`
- `entity_ids`: `list[str]`
- `relationship_ids`: `list[str]`
- `belief_ids`: `list[str]`
- `knowledge_ids`: `list[str]`

## 18. State
Current internal cognitive snapshot.
- `id`: `str`
- `active_goal_ids`: `list[str]`
- `working_memory_ids`: `list[str]`
- `current_plan_ids`: `list[str]`
- `resource_usage`: `dict[str, float]`

## 19. Event
Event envelope for cognitive communications.
- `id`: `str`
- `event_type`: `str`
- `source_subsystem`: `str`
- `payload`: `dict`
- `timestamp`: `float`
