# ELIZA Model-Agnostic LLM Routing Specification

> **Version**: 1.0.0 (Model Abstraction & Router Specification)  
> **Status**: Canonical Model Architecture Reference  
> "The LLM is a CPU: a replaceable execution engine behind a stable cognitive operating system architecture."

---

## 🏛️ Model-Agnostic Architecture

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

---

## 🔑 Key Architectural Principles

1. **Model Abstraction Layer (`LanguageModel` ABC)**:
   ELIZA never imports model-specific APIs directly outside this layer (`generate`, `embed`, `tokenize`, `stream`).

2. **Model Adapters Suite**:
   Standardized adapters for local inference (Ollama / llama.cpp), high-throughput local serving (vLLM), cloud providers (OpenAI / Anthropic / Custom endpoints), and specialized open-weights models (DeepSeek, Qwen, Llama, Gemma, Mistral).

3. **Capability Registry**:
   Maintains quantitative capability ratings per model:
   - `reasoning`: low / medium / high / very_high
   - `coding`: low / medium / high / very_high
   - `speed`: low / medium / high / very_high
   - `cost`: free / low / medium / high
   - `context_window`: e.g. 8k, 32k, 128k
   - `local_vs_cloud`: local / cloud

4. **Dynamic Task-Based Routing**:
   - `coding` -> DeepSeek
   - `long_reasoning` -> Qwen
   - `conversation` -> Llama
   - `fast_summarization` -> Gemma
   - `vision` -> Vision-language adapter

5. **Structured Outputs**:
   Models populate FCRL cognitive object schemas rather than generating free-form unparseable text. Memory, planning, and persistent state remain outside the model in ECOS Kernel.
