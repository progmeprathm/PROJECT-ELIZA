import time
from typing import Dict, Any, List

class RuntimeMetrics:
    def __init__(self):
        self.counters = {}
        self.timers = {}
        self.gauges = {}
        
    def increment(self, metric: str, amount: int = 1):
        self.counters[metric] = self.counters.get(metric, 0) + amount
        
    def start_timer(self, metric: str):
        self.timers[f"{metric}_start"] = time.time()
        
    def stop_timer(self, metric: str):
        if f"{metric}_start" in self.timers:
            duration = time.time() - self.timers[f"{metric}_start"]
            self.gauges[f"{metric}_duration"] = duration
            
    def set_gauge(self, metric: str, value: float):
        self.gauges[metric] = value
        
    def get_summary(self) -> Dict[str, Any]:
        return {
            "counters": self.counters,
            "gauges": self.gauges
        }

class RuntimeDiagnostics:
    def __init__(self, metrics: RuntimeMetrics):
        self.metrics = metrics
        
    def identify_bottlenecks(self) -> List[str]:
        issues = []
        if self.metrics.counters.get("replans", 0) > 3:
            issues.append("Excessive replanning detected.")
        if self.metrics.counters.get("memory_pollution_events", 0) > 5:
            issues.append("High memory pollution.")
        if self.metrics.gauges.get("context_tokens", 0) > 10000:
            issues.append("Context token limit approaching threshold.")
        return issues
