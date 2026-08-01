# ELIZA API Contracts Specification

> **Version**: 1.0.0 (Phase 2 Executable Architecture)  
> **Status**: Canonical API Contracts

This document defines abstract interface contracts across ELIZA's cognitive subsystems.

---

## 1. MemoryAPI
```python
class MemoryAPI(ABC):
    @abstractmethod
    def store(self, key: str, value: Any, importance: float = 0.5) -> None: pass
    @abstractmethod
    def retrieve(self, query: str, limit: int = 10) -> List[Any]: pass
    @abstractmethod
    def forget(self, key: str) -> bool: pass
    @abstractmethod
    def consolidate(self) -> None: pass
    @abstractmethod
    def search(self, filter_params: Dict[str, Any]) -> List[Any]: pass
```

## 2. ReasonerAPI
```python
class ReasonerAPI(ABC):
    @abstractmethod
    def reason(self, beliefs: List[Belief], style: str = "deductive") -> List[Belief]: pass
    @abstractmethod
    def evaluate(self, hypothesis: Hypothesis, evidence: List[Evidence]) -> float: pass
    @abstractmethod
    def compare(self, alternative_a: Any, alternative_b: Any) -> Dict[str, Any]: pass
    @abstractmethod
    def explain(self, decision_id: str) -> Explanation: pass
```

## 3. PlannerAPI
```python
class PlannerAPI(ABC):
    @abstractmethod
    def plan(self, goal: Goal, beliefs: List[Belief]) -> Plan: pass
    @abstractmethod
    def replan(self, failed_plan_id: str, new_constraints: List[str]) -> Plan: pass
    @abstractmethod
    def estimate(self, plan: Plan) -> Dict[str, float]: pass
```

## 4. SimulatorAPI
```python
class SimulatorAPI(ABC):
    @abstractmethod
    def simulate(self, plan: Plan, world_state: List[Belief]) -> SimulationResult: pass
    @abstractmethod
    def evaluate(self, simulation_id: str) -> float: pass
    @abstractmethod
    def rollback(self, simulation_id: str) -> None: pass
```

## 5. SafetyAPI
```python
class SafetyAPI(ABC):
    @abstractmethod
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> RiskAssessment: pass
    @abstractmethod
    def veto_action(self, action_id: str, reason: str) -> None: pass
```

## 6. LearnerAPI
```python
class LearnerAPI(ABC):
    @abstractmethod
    def validate_learning(self, candidate: ValidatedLearning) -> bool: pass
    @abstractmethod
    def update_policy(self, policy: Policy) -> None: pass
```
