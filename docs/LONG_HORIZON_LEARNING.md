# Long Horizon Learning

## 1. Defining Long Horizon
Instead of evaluating the agent on isolated puzzle instances, the v1.0 benchmark evaluates `ELIZARuntime` across a sequential progression of 25 procedural tasks (`ecos/simulation/long_horizon.py`) sharing memory and knowledge state.

## 2. Experimental Measurement
The core experiment measures `COLD_RUNTIME` vs `PERSISTENT_RUNTIME`. If the persistent architecture is sound, performance should demonstrably improve (or remain highly efficient) on later steps because the runtime can recall coordination strategies and tool nuances established in steps 1-5, rather than recalculating plans from a raw prompt every cycle.

## 3. Negative Transfer Evaluation
As task parameters change across the 25 tasks, older persistent knowledge will become invalid. The system successfully intercepts these using Independent Verification and flags them via `LEARNING_EVENT` updates, resolving conflicts natively instead of trapping the agent in hallucination loops.
