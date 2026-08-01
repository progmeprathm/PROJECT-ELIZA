# ELIZA Cognitive Runtime (ECOS Phase 3 Specification)

> **Version**: 1.0.0 (Phase 3 Executable Runtime Architecture)  
> **Status**: Canonical Runtime Reference  
> "The LLM is an interchangeable execution unit, not the operating system architecture itself."

---

## 🏛️ Phase 3 Layer Overview (Layers 0 to 14)

```
Goal Statement
    │
    ▼
[Layer 9: Cognitive Compiler] ──► Compiles to Cognitive ISA Bytecode
    │
    ▼
[Layer 1 & 8: Cognitive CPU & CVM] ──► Decodes & executes instructions
    │
    ├────────► [Layer 2: 7-Tier Memory Hierarchy]
    ├────────► [Layer 3: Cognitive Bus / CCP]
    ├────────► [Layer 4, 5, 6: Process Scheduler & Threads (PIDs)]
    ├────────► [Layer 7: Cognitive Filesystem (CFS)]
    ├────────► [Layer 10: ECOS Kernel Operating System]
    ├────────► [Layer 12: Cognitive Marketplace]
    └────────► [Layer 13: Scientific Engine]
```

---

## ⚡ Layer 0: Cognitive ISA (20 Opcodes)

| Opcode | Category | Description |
|---|---|---|
| `OBSERVE` | Perception | Input raw sensor evidence |
| `ATTEND` | Executive | Allocate dynamic compute/memory budget |
| `RECALL` | Memory | Retrieve items from memory hierarchy |
| `STORE` | Memory | Persist item to memory hierarchy |
| `BELIEVE` | World Model | Establish probabilistic belief from evidence |
| `QUESTION` | Reasoning | Flag missing knowledge / uncertainty |
| `INFER` | Reasoning | Derive logical inferences |
| `PLAN` | Planning | Decompose goal into execution strategy |
| `SIMULATE` | Simulation | Evaluate counterfactual sandbox |
| `DECIDE` | Executive | Select optimal alternative option |
| `EXECUTE` | Action | Execute action payload |
| `REFLECT` | Reflection | Analyze outcome & extract lessons |
| `LEARN` | Learning | Validate & commit persistent policy update |
| `REVISE` | World Model | Revise belief confidence or state |
| `FORGET` | Memory | Expire stale memory items |
| `PRIORITIZE` | Executive | Reorder goal priority queue |
| `MERGE` | World Model | Combine consistent knowledge items |
| `SPLIT` | World Model | Separate conflicting belief graphs |
| `SUSPEND` | Process | Suspend active cognitive process |
| `RESUME` | Process | Resume suspended cognitive process |

---

## 🧠 Layer 2: 7-Tier Cognitive Memory Hierarchy

1. **Attention Register**: Immediate execution register (latency: 0.1ms, capacity: 1 item)
2. **Working Memory**: Active workspace context (latency: 1ms, capacity: 10 items)
3. **Context Cache**: Transient environment cache (latency: 5ms, capacity: 50 items)
4. **Episodic Memory**: Temporal experience log (latency: 15ms, capacity: 500 items)
5. **Semantic Memory**: Fact & concept store (latency: 25ms, capacity: 5,000 items)
6. **Knowledge Graph**: Entity-relationship belief graph (latency: 50ms, capacity: 50,000 items)
7. **Long-Term Storage**: Persistent consolidated archive (latency: 100ms, capacity: unlimited)

---

## 📂 Layer 7: Cognitive Filesystem (CFS)

Inspectable virtual filesystem hierarchy:
- `/memory/` (Active memory objects)
- `/beliefs/` (World model beliefs)
- `/goals/` (System goals)
- `/plans/` (Execution plans)
- `/policies/` (Behavioral rules)
- `/experiences/` (Reflected experiences)
- `/skills/` (Reusable routines)
- `/world/` (Entity-relationship graph)
- `/agents/` (Registered cognitive sub-agents)

---

## 🔬 Layer 13: Scientific Engine

Automated scientific discovery loop:
`Intake Literature / Evidence -> Extract Knowledge -> Detect Contradictions -> Generate Hypotheses -> Simulate Counterfactuals -> Rank Options -> Suggest Verification Experiments`.
