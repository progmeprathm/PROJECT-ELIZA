# ELIZA Studio Specification (Version 0.1)

> **Version**: 0.1.0 (ELIZA Studio UI & Control Deck Specification)  
> **Status**: Canonical Studio Reference  
> "Instead of a chat window, users can inspect the system's reasoning, plans, and state."

---

## 🎨 UI Architecture & Design System

- **Design Aesthetic**: Premium Dark Mode with Glassmorphism (`backdrop-filter: blur(16px)`), curated HSL color palette, glowing neon accents (`#6366f1` Indigo, `#10b981` Emerald, `#ec4899` Pink, `#06b6d4` Cyan), sleek borders (`rgba(255, 255, 255, 0.1)`), and smooth micro-animations.
- **Header Status Bar**: System Status indicator (`ECOS Kernel Online`), Active PID Counter, Memory Usage, Clock, and Quick Navigation.
- **Sidebar**: Quick links to all 10 Core Screens.
- **Live Panel (Right Side)**: Signature Live Cognitive State Inspector panel displaying real-time cognitive hierarchy.

---

## 📊 Core Screens (10 Views)

1. **Dashboard**: Task Manager for Cognition (Process PIDs, CPU/Memory gauges, 19-stage reasoning pipeline, active modules).
2. **Memory Explorer**: Interactive 7-Tier memory browser (Attention Register to Long-Term Storage) with search & provenance trace.
3. **World Model Viewer**: Interactive SVG node graph visualizing Entities, Relationships, Beliefs, Evidence, and Confidence scores.
4. **Goal Manager**: Tree hierarchy (`Goal -> Subgoals -> Plans -> Tasks -> Status`) with Pause, Reprioritize, and Cancel controls.
5. **Planner**: Multi-plan comparison matrix (Plan A vs Plan B vs Plan C) detailing estimated time, cost, risk, and confidence metrics.
6. **Simulator**: Counterfactual "what-if" scenario sandbox.
7. **Reasoning Inspector**: Decision provenance breakdown (`Question -> Evidence -> Memory -> Beliefs -> Inference -> Conclusion -> Confidence`).
8. **Reflection Viewer**: Post-task execution reflection viewer detailing wrong assumptions and proposed Learning Candidates.
9. **Benchmark Center**: CI/CD capability performance metrics tracking over time across 6 capability dimensions.
10. **Plugin Marketplace**: Package manager browser for sandboxed cognitive modules (`Planner Pro`, `Memory++`, `Scientific Reasoner`).

---

## 💡 Signature Feature: Live Cognitive State Panel

```
Current Goal
├── Build ECOS Kernel
│
├── Active Thought
│   ├── Retrieving Memory
│   ├── Comparing Designs
│   └── Generating Plan
│
├── Confidence: 82%
├── Assumptions: 5 Active
└── Next Planned Action: Write Scheduler Specification
```
