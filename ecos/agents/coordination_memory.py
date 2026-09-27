from typing import Dict, Any, List
import uuid
import time

class CollectiveLearningEvent:
    def __init__(self, source_agent: str, recipient_agent: str, task_id: str, pattern: str, outcome_before: str, outcome_after: str):
        self.event_id = f"cl-{uuid.uuid4().hex[:8]}"
        self.timestamp = time.time()
        self.source_agent = source_agent
        self.recipient_agent = recipient_agent
        self.task_id = task_id
        self.pattern = pattern
        self.outcome_before = outcome_before
        self.outcome_after = outcome_after
        self.type = "COLLECTIVE_LEARNING_EVENT"

class CoordinationMemory:
    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.learning_events: List[CollectiveLearningEvent] = []
        self.conflicts: List[Dict[str, Any]] = []
        
    def record_pattern(self, pattern_id: str, description: str, applicable_tasks: List[str], success: bool):
        if pattern_id not in self.patterns:
            self.patterns[pattern_id] = {
                "id": pattern_id,
                "description": description,
                "applicable_tasks": applicable_tasks,
                "success_count": 0,
                "failure_count": 0,
                "state": "ACTIVE"
            }
        
        if success:
            self.patterns[pattern_id]["success_count"] += 1
        else:
            self.patterns[pattern_id]["failure_count"] += 1
            
    def record_learning_event(self, event: CollectiveLearningEvent):
        self.learning_events.append(event)
        
    def record_conflict(self, pattern_a: str, pattern_b: str, context: str):
        self.conflicts.append({
            "timestamp": time.time(),
            "pattern_a": pattern_a,
            "pattern_b": pattern_b,
            "context": context
        })
        
    def record_negative_transfer(self, pattern_id: str, context: str):
        if pattern_id in self.patterns:
            self.patterns[pattern_id]["state"] = "CONFLICTED"
            self.conflicts.append({
                "timestamp": time.time(),
                "pattern_id": pattern_id,
                "context": context,
                "type": "NEGATIVE_TRANSFER"
            })
