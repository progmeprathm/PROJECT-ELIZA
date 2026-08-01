# E.L.I.Z.A Architecture Diagrams

> **Status**: Canonical System Architecture Maps & Sequence Flows

---

## 1. System High-Level Architecture (The 11 Layers)

```mermaid
graph TD
    Goal["Goal Statement"] --> Compiler["Cognitive Compiler (Layer 9)"]
    Compiler --> Bytecode["Cognitive ISA Bytecode"]
    Bytecode --> CPU["Cognitive CPU & CVM (Layer 1 & 8)"]

    CPU --> Mem["7-Tier Memory Hierarchy (Layer 2)"]
    CPU --> Bus["CCP Event Bus (Layer 3)"]
    CPU --> CFS["Cognitive Filesystem /cfs/ (Layer 7)"]
    CPU --> OS["ECOS Kernel OS (Layer 10)"]
    CPU --> Market["Cognitive Marketplace (Layer 12)"]
    CPU --> Science["Scientific Engine (Layer 13)"]
```

---

## 2. The 19-Stage Cognitive Pipeline

```mermaid
sequenceDiagram
    autonumber
    participant P as Perception
    participant M as Memory (7-Tier)
    participant W as World Model Graph
    participant R as Reasoner
    participant G as Goal Planner
    participant S as Simulator
    participant E as Executive & Safety
    participant A as Action Execution
    participant L as Reflector & Learner

    P->>M: 1. Observe & 2. Normalize
    M->>W: 3. Attend & 4. Interpret
    W->>R: 5. Retrieve Memory & 6. Update World Model
    R->>G: 7. Reason & 8. Generate Goals
    G->>S: 9. Prioritize Goals & 10. Plan
    S->>E: 11. Simulate & 12. Evaluate Risk
    E->>A: 13. Decide & 14. Execute Action
    A->>L: 15. Observe Outcome & 16. Reflect
    L->>M: 17. Learn & 18. Consolidate Memory
```

---

## 3. Cognitive Civilization P2P Network Architecture

```mermaid
graph LR
    subgraph Mind Nodes
        Sci["ELIZA Scientist"]
        Plan["ELIZA Planner"]
        Eng["ELIZA Engineer"]
        Sim["ELIZA Simulator"]
    end

    subgraph Network Layer
        CCP["CCP Event Bus Router"]
        Gov["Cognitive Governance"]
        Rep["Reputation Engine"]
    end

    Sci <-->|CCP Message| CCP
    Plan <-->|CCP Message| CCP
    Eng <-->|CCP Message| CCP
    Sim <-->|CCP Message| CCP

    CCP --> Gov
    Gov --> Rep
```

---

## 4. ELIZA Studio v0.1 Control Deck Architecture

```mermaid
graph TB
    User["User Browser"] <-->|HTTP/REST & Telemetry| StudioServer["studio/server.py"]
    StudioServer <--> Kernel["ECOS Kernel OS"]
    StudioServer <--> Memory["7-Tier Memory Hierarchy"]
    StudioServer <--> WM["World Model Reality Graph"]
    StudioServer <--> Bench["Benchmark Center"]
```
