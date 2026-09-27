# Collective Intelligence Validation

## 1. Defining Collective Intelligence
For E.L.I.Z.A., collective intelligence is strictly defined as measurable behavioral improvement in a multi-agent cluster exceeding a single E.L.I.Z.A. baseline, generated from shared experience and verified independently.

## 2. Hypothesis Matrix
- **H1-H4**: Focus on specialized role coordination improving task latency and reliability. Evaluated by comparing `SINGLE_ELIZA` vs `MULTI_ADAPTIVE`.
- **H5-H7**: Focus on knowledge accumulation. Evaluated by triggering `COLLECTIVE_LEARNING_EVENT` on early tasks and measuring subsequent tasks for cold vs warm start improvements.
- **H8-H10**: Focus on negative externalities (overhead, context pollution, negative transfer). Evaluated by running `FULL_COLLECTIVE` on conflict-injected variants.

## 3. The Validation Protocol
Rather than creating subjective AGI claims, the `run_v09_benchmark.py` isolates task variants and ensures the `CoordinatorAgent` only succeeds if the specialized agents actually resolve the explicit dependencies (Family B, D, F, G tasks) better than the baseline.
