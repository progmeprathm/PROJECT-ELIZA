# ELIZA Companion Specification

> **Version**: 1.0.0 (Inverted Cognitive Companion Specification)  
> **Status**: Canonical Companion Reference  
> "The chatbot becomes just one client of the cognitive operating system."

---

## 🏛️ Inverted Architecture Pipeline

```
                    User
                      │
                Chat Interface (ELIZA Companion)
                      │
               Conversation Manager
                      │
              Executive Controller
                      │
        ┌─────────────┼─────────────┐
        │             │             │
     Memory      World Model    Goal Manager
        │             │             │
        ├─────────────┼─────────────┤
        │             │             │
   Reasoning      Planning     Simulation
        │             │             │
        └─────────────┼─────────────┘
                      │
                Cognitive Kernel
                      │
          Foundation Model(s) (optional)
```

---

## 💬 Three Interaction Modes

### Mode 1 — Conversation
Natural dialogue interface with ELIZA Companion.

### Mode 2 — Cognitive Workspace
Dual-pane workspace pairing conversation with live structured state:
- Goal description & progress (%)
- Current activity subroutine
- Confidence score meter
- Active memory count & running simulations

### Mode 3 — Engineering Console (Cognitive Shell)
CLI shell for system developers:
- `> /memory search <query>`
- `> /goal create <description>`
- `> /simulate <scenario>`
- `> /events`
- `> /trace last`
- `> /benchmark planning`

---

## 🤖 Specialized Assistant Profiles

| Assistant | Specialized Role |
|---|---|
| **Architect** | System architecture, modular design, and kernel specs |
| **Researcher** | Scientific literature review, hypothesis generation, and evidence synthesis |
| **Engineer** | Code generation, refactoring, debugging, and verification |
| **Planner** | Strategic goal decomposition and task planning |
| **Analyst** | Quantitative data interpretation, metrics, and reporting |
| **Teacher** | Explanations, conceptual tutoring, and documentation |

---

## 🔍 Decision Reasoning Trace ("Why did you recommend this?")

Exposes explicit cognitive artifacts created during execution:
- **Goal**: Target cognitive objective.
- **Evidence**: Supporting observations and benchmark results.
- **Alternatives**: Evaluated options with chosen selection checkmark.
- **Confidence**: Quantitative confidence score.
- **Assumptions**: Active underlying assumptions.
