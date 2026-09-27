# Adaptive Delegation

## 1. Core Abstraction
The `DynamicDelegator` (`ecos/agents/delegation.py`) handles assignment decisions on behalf of the `CoordinatorAgent`.

## 2. Policies
- **FIXED**: Takes the first available matching capability. Used for regression.
- **CAPABILITY**: Scans the `AgentRegistry` for specific required capability strings (e.g., `execute_action`).
- **ADAPTIVE**: Retrieves the active `AgentPerformanceTracker` profile, calculating historical `success_rate` = `S / (S + F)`. It dynamically limits the maximum number of agents based on difficulty/complexity, preventing over-allocation and unnecessary token cost.

## 3. Delegation Decision Record
Every delegation produces a record explicitly tracking candidates, required capabilities, and policy used, ensuring complete transparency for benchmark analysis.
