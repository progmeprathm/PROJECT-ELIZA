# Generalization

## 1. Train / Test Separation
The LLM prompt is never exposed to the underlying `TaskGenerator` logic, metadata, or expected solution.

## 2. Unseen Task Variants
Because every trial uses random generation (`seed`), the live model sees a uniquely instantiated variant every time. It cannot memorize "the code is 12 and multiplier is 4". It must dynamically call `read_note` -> observe `a` -> call `read_wall` -> observe `b` -> call `calculator` with `a * b` -> `unlock`.

## 3. Cognitive Generalization Proof
If `MODEL_ONLY` fails but `F - Full v0.6` succeeds, we have empirical proof that the E.L.I.Z.A. runtime architecture provides generalized multi-step reasoning capabilities to an underlying foundational model, independent of benchmark overfitting.
