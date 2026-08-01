# =============================================================================
# ELIZA_FORMALISM.md
# Formal Cognitive Representation Language (FCRL)
# Version: 1.0
# Canonical Cognitive Data Model
# =============================================================================

> "A cognitive architecture is only as coherent as the language spoken
> between its cognitive systems."

-------------------------------------------------------------------------------
PURPOSE
-------------------------------------------------------------------------------

This document defines the canonical representation of cognition inside ELIZA.

Every subsystem SHALL communicate using these formal objects.

No subsystem shall invent incompatible internal cognitive structures
without an approved extension.

The formalism is implementation-independent.

Python, Rust, C++, distributed systems, or future implementations
must preserve identical semantics.

-------------------------------------------------------------------------------
FOUNDATIONAL COGNITIVE OBJECTS
-------------------------------------------------------------------------------

Everything inside ELIZA is represented using Cognitive Objects.

The primitive objects are:

Observation

Evidence

Belief

Knowledge

Entity

Relationship

Context

Memory

Goal

Constraint

Hypothesis

Question

Plan

Task

Decision

Action

Outcome

Experience

Policy

Skill

Identity

State

Event

WorldModel

-------------------------------------------------------------------------------
COGNITIVE GRAPH
-------------------------------------------------------------------------------

The complete cognitive state is represented as a directed labeled graph.

Nodes

represent cognitive objects.

Edges

represent semantic relationships.

Example

Observation

↓

Evidence

↓

Belief

↓

Knowledge

↓

Reasoning

↓

Plan

↓

Decision

↓

Action

↓

Outcome

↓

Experience

↓

Memory

↓

Updated Beliefs

This graph is the canonical internal representation.

-------------------------------------------------------------------------------
OBSERVATION
-------------------------------------------------------------------------------

Definition

Raw information received from perception.

Properties

id

timestamp

source

modality

raw_data

confidence

metadata

Observations are immutable.

-------------------------------------------------------------------------------
EVIDENCE
-------------------------------------------------------------------------------

Definition

Validated observations supporting or opposing beliefs.

Properties

supports

contradicts

strength

origin

Evidence never directly creates knowledge.

-------------------------------------------------------------------------------
BELIEF
-------------------------------------------------------------------------------

Definition

A probabilistic interpretation of available evidence.

Properties

belief_id

statement

confidence

supporting_evidence

contradicting_evidence

timestamp

status

Beliefs are revisable.

-------------------------------------------------------------------------------
KNOWLEDGE
-------------------------------------------------------------------------------

Definition

Validated beliefs organized for reasoning.

Knowledge contains

concepts

facts

rules

relationships

Knowledge is structured.

-------------------------------------------------------------------------------
ENTITY
-------------------------------------------------------------------------------

Definition

Anything represented in the world.

Examples

Person

Company

City

Idea

Process

Algorithm

Robot

Each entity possesses

identity

attributes

relationships

history

-------------------------------------------------------------------------------
RELATIONSHIP
-------------------------------------------------------------------------------

Represents semantic connections.

Examples

owns

contains

causes

located_in

depends_on

created_by

part_of

-------------------------------------------------------------------------------
CONTEXT
-------------------------------------------------------------------------------

Context defines interpretation.

Properties

location

time

participants

environment

active goals

available resources

Context modifies reasoning.

-------------------------------------------------------------------------------
MEMORY
-------------------------------------------------------------------------------

Memory stores cognitive objects.

Memory Types

Working

Short-term

Semantic

Episodic

Procedural

Long-term

Every memory stores

importance

retrieval score

last accessed

creation time

source

-------------------------------------------------------------------------------
GOAL
-------------------------------------------------------------------------------

Definition

Desired future world state.

Properties

priority

deadline

dependencies

constraints

progress

owner

Goals may decompose into sub-goals.

-------------------------------------------------------------------------------
CONSTRAINT
-------------------------------------------------------------------------------

Definition

A restriction on planning or action.

Examples

time

budget

ethics

permissions

physical limitations

-------------------------------------------------------------------------------
QUESTION
-------------------------------------------------------------------------------

Definition

Missing knowledge required for progress.

Questions drive exploration.

-------------------------------------------------------------------------------
HYPOTHESIS
-------------------------------------------------------------------------------

Definition

Untested explanatory model.

Properties

confidence

predictions

required evidence

status

Hypotheses become beliefs after validation.

-------------------------------------------------------------------------------
PLAN
-------------------------------------------------------------------------------

Definition

Ordered strategy for satisfying goals.

Properties

tasks

estimated cost

estimated duration

risk

dependencies

success probability

-------------------------------------------------------------------------------
TASK
-------------------------------------------------------------------------------

Atomic executable unit.

Properties

preconditions

resources

completion criteria

status

-------------------------------------------------------------------------------
DECISION
-------------------------------------------------------------------------------

Definition

Selection among competing alternatives.

Properties

alternatives

chosen option

utility

confidence

justification

-------------------------------------------------------------------------------
ACTION
-------------------------------------------------------------------------------

Definition

Operation affecting the environment.

Properties

executor

tool

parameters

expected outcome

observed outcome

-------------------------------------------------------------------------------
OUTCOME
-------------------------------------------------------------------------------

Observed consequences of actions.

Contains

success

failure

metrics

side effects

unexpected events

-------------------------------------------------------------------------------
EXPERIENCE
-------------------------------------------------------------------------------

Definition

Outcome interpreted through reflection.

Experiences generate learning.

-------------------------------------------------------------------------------
POLICY
-------------------------------------------------------------------------------

Persistent behavioral rule.

Policies guide decisions.

Policies are versioned.

-------------------------------------------------------------------------------
SKILL
-------------------------------------------------------------------------------

Reusable capability.

Examples

planning

coding

translation

diagnosis

optimization

Skills improve through practice.

-------------------------------------------------------------------------------
IDENTITY
-------------------------------------------------------------------------------

Definition

Persistent organization of

knowledge

values

goals

behavior

Identity evolves.

-------------------------------------------------------------------------------
STATE
-------------------------------------------------------------------------------

Represents current internal condition.

Contains

active goals

working memory

attention

current plans

resource usage

-------------------------------------------------------------------------------
EVENT
-------------------------------------------------------------------------------

Everything changes through events.

Examples

ObservationReceived

BeliefUpdated

GoalCreated

PlanGenerated

ActionExecuted

MemoryConsolidated

ReflectionCompleted

-------------------------------------------------------------------------------
WORLD MODEL
-------------------------------------------------------------------------------

The World Model is a continuously evolving graph consisting of

Entities

Relationships

Beliefs

Knowledge

Context

Temporal history

Every subsystem interacts through this model.

-------------------------------------------------------------------------------
COGNITIVE STATE MACHINE
-------------------------------------------------------------------------------

Canonical transition

Observe

↓

Interpret

↓

Generate Beliefs

↓

Update World Model

↓

Retrieve Memory

↓

Reason

↓

Generate Goals

↓

Plan

↓

Simulate

↓

Decide

↓

Act

↓

Observe Outcome

↓

Reflect

↓

Learn

↓

Update Memory

Repeat

-------------------------------------------------------------------------------
BELIEF UPDATE RULE
-------------------------------------------------------------------------------

Beliefs change only through

new evidence

contradictory evidence

reflection

validated learning

Beliefs never change arbitrarily.

-------------------------------------------------------------------------------
MEMORY CONSOLIDATION RULE
-------------------------------------------------------------------------------

Working Memory

↓

Short-Term Memory

↓

Long-Term Memory

Importance determines retention.

-------------------------------------------------------------------------------
PLANNING RULE
-------------------------------------------------------------------------------

Every plan must define

Goal

Resources

Constraints

Tasks

Dependencies

Success metrics

-------------------------------------------------------------------------------
DECISION RULE
-------------------------------------------------------------------------------

Every decision records

Evidence used

Beliefs consulted

Alternatives

Utility estimate

Confidence

-------------------------------------------------------------------------------
LEARNING RULE
-------------------------------------------------------------------------------

Learning requires

Experience

Validation

Persistent update

Benchmark improvement

-------------------------------------------------------------------------------
FORMAL COGNITIVE INVARIANTS
-------------------------------------------------------------------------------

Invariant 1

Every Belief references Evidence.

Invariant 2

Every Plan references Goals.

Invariant 3

Every Action belongs to a Plan.

Invariant 4

Every Experience references an Outcome.

Invariant 5

Every Memory has provenance.

Invariant 6

Every Decision records confidence.

Invariant 7

Every Knowledge object references Beliefs.

Invariant 8

Every Goal has measurable completion criteria.

Invariant 9

Every Policy is version controlled.

Invariant 10

Every cognitive object has a unique identity.

-------------------------------------------------------------------------------
EXTENSIBILITY
-------------------------------------------------------------------------------

New cognitive objects may be introduced only if they:

have explicit semantics

fit the cognitive graph

preserve invariants

remain benchmarkable

-------------------------------------------------------------------------------
MATHEMATICAL VIEW
-------------------------------------------------------------------------------

ELIZA is formally modeled as

C = (O, E, B, K, G, P, D, A, M, W)

Where

O = Observations

E = Evidence

B = Beliefs

K = Knowledge

G = Goals

P = Plans

D = Decisions

A = Actions

M = Memory

W = World Model

Every cognitive cycle transforms C(t)
into C(t+1).

-------------------------------------------------------------------------------
FINAL STATEMENT
-------------------------------------------------------------------------------

This formalism is the common language of ELIZA.

Every subsystem reasons over the same cognitive objects.

Every implementation must preserve these semantics,
regardless of programming language or execution environment.

The architecture evolves.

The formal language remains stable.

# =============================================================================
# END OF ELIZA FORMALISM
# =============================================================================
