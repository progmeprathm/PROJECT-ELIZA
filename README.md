# E.L.I.Z.A (Evolutionary Learning Intelligence & Zero-shot Architecture)

> **"Architecture before Intelligence. Intelligence before Capability. Capability before Optimization."**

ELIZA is an open Cognitive Operating System built on explicit architectural principles, modular subsystem cooperation, event-driven communication, deterministic safety guardrails, total decision inspectability, and model-agnostic LLM execution engine routing.

---

## 🔀 Model-Agnostic LLM Routing Architecture

```
                    ELIZA Companion
                           │
                    Conversation Layer
                           │
                   Executive Controller
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     Memory          World Model         Goal Manager
        │                  │                  │
        ├──────────────────┼──────────────────┤
        │                  │                  │
   Reasoning         Planning          Simulation
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    Model Router
                           │
      ┌────────────┬────────────┬────────────┐
      │            │            │            │
   Llama 3.x     Qwen        DeepSeek      Mistral
      │            │            │            │
      └────────────┴────────────┴────────────┘
                           │
                     Local GPU / API
```

> **"The LLM is a CPU: a replaceable execution engine behind a stable cognitive operating system architecture."**

- **Model Abstraction Layer**: Standardized [`LanguageModel`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/llms/base.py) ABC (`generate`, `embed`, `tokenize`, `stream`).
- **Model Adapters Suite**: `OllamaAdapter` (local CPU/GPU), `VLLMAdapter` (high-throughput local serving), `CloudAPIAdapter` (OpenAI/Anthropic/Custom APIs), `DeepSeekAdapter`, `QwenAdapter`, `LlamaAdapter`, `GemmaAdapter`, `MistralAdapter`.
- **Task-Based Routing Matrix**:
  - 💻 `coding` -> **DeepSeek Coder**
  - 🧠 `long_reasoning` -> **Qwen 2.5 72B**
  - 💬 `conversation` -> **Llama 3.1 8B**
  - ⚡ `summarization` -> **Gemma 2 9B**
  - 🌐 `multilingual / analysis` -> **Mistral Large**

---

## 🎯 Three Products Built on One ECOS Kernel

```
                    ECOS Kernel
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Chat Assistant   Visual Studio    Automation API
  (ELIZA Companion) (ELIZA Studio)  (companion/client.py)
```

1. **ELIZA Companion**: Conversational assistant with memory, goals, planning, reasoning, and simulations.
2. **ELIZA Studio**: Visual control deck & workspace for research, development, and system inspection.
3. **ECOS Automation API**: Python SDK ([`companion/client.py`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/companion/client.py)) enabling external software integration.

---

## 📜 Canonical Specifications (The 12 Master Documents)

1. 🏛️ [`ELIZA_CANON.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_CANON.md) - Immutable Constitution
2. 🔬 [`ELIZA_AXIOMS.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_AXIOMS.md) - 25 Fundamental Cognitive Axioms
3. 📐 [`ELIZA_FORMALISM.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_FORMALISM.md) - Formal Cognitive Representation Language (FCRL)
4. ⚡ [`ELIZA_DYNAMICS.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_DYNAMICS.md) - Cognitive Dynamics Specification
5. ⚙️ [`ELIZA_KERNEL_SPEC.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_KERNEL_SPEC.md) - ECOS Kernel Specification
6. 📡 [`ELIZA_PROTOCOL.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_PROTOCOL.md) - Cognitive Communication Protocol (CCP)
7. 💻 [`ELIZA_COGNITIVE_RUNTIME.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_COGNITIVE_RUNTIME.md) - Phase 3 ECOS Runtime & 20 Cognitive ISA Instructions
8. 🔄 [`ELIZA_ADAPTIVE_COGNITION.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_ADAPTIVE_COGNITION.md) - Phase 4 Adaptive Cognition & Hypothesis H1
9. 🌐 [`ELIZA_COGNITIVE_CIVILIZATION.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_COGNITIVE_CIVILIZATION.md) - Phase 5 Cognitive Civilization & Multiple Minds
10. 🖥️ [`ELIZA_STUDIO_SPEC.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_STUDIO_SPEC.md) - ELIZA Studio Control Deck Specification
11. 🤖 [`ELIZA_COMPANION_SPEC.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_COMPANION_SPEC.md) - ELIZA Companion Specification
12. 🔀 [`ELIZA_MODEL_ROUTER_SPEC.md`](file:///c:/aNTIGRAVITY/E.L.I.Z.A/ELIZA_MODEL_ROUTER_SPEC.md) - Model-Agnostic LLM Routing Specification

---

## 🛠️ Quickstarts & Execution

Launch ELIZA Companion & Studio UI:
```bash
python run_eliza_companion.py
```

Run Model Router Milestone:
```bash
python run_ecos_model_router.py
```

Run Master Verification Suite:
```bash
python run_tests.py
```
