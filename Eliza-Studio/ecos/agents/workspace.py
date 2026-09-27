from typing import Dict, Any, List
import uuid

class CognitiveWorkspace:
    """
    Shared global workspace for multi-agent coordination.
    Tracks task state, assignments, dependencies, and evidence.
    """
    def __init__(self, task_goal: str):
        self.workspace_id = f"workspace-{uuid.uuid4().hex[:8]}"
        self.task_goal = task_goal
        
        self.subtasks: Dict[str, Dict[str, Any]] = {}
        self.agent_assignments: Dict[str, str] = {} # subtask_id -> agent_id
        
        self.completed_subtasks: List[str] = []
        self.pending_subtasks: List[str] = []
        
        self.evidence: List[Dict[str, Any]] = []
        self.candidate_solutions: List[Any] = []
        self.verification_results: List[Any] = []
        
        self.failures: List[Dict[str, Any]] = []
        self.replanning_events: int = 0
        self.final_result: Any = None
        
    def add_subtask(self, subtask_id: str, description: str, dependencies: List[str] = None):
        self.subtasks[subtask_id] = {
            "id": subtask_id,
            "description": description,
            "dependencies": dependencies or [],
            "status": "PENDING"
        }
        self.pending_subtasks.append(subtask_id)
        
    def assign_agent(self, subtask_id: str, agent_id: str):
        if subtask_id in self.subtasks:
            self.agent_assignments[subtask_id] = agent_id
            
    def complete_subtask(self, subtask_id: str, result: Any):
        if subtask_id in self.subtasks:
            self.subtasks[subtask_id]["status"] = "COMPLETED"
            self.subtasks[subtask_id]["result"] = result
            if subtask_id in self.pending_subtasks:
                self.pending_subtasks.remove(subtask_id)
            self.completed_subtasks.append(subtask_id)
            
    def add_evidence(self, item: Dict[str, Any]):
        self.evidence.append(item)
        
    def record_failure(self, subtask_id: str, error: str):
        self.failures.append({"subtask_id": subtask_id, "error": error})
        if subtask_id in self.subtasks:
            self.subtasks[subtask_id]["status"] = "FAILED"
            
    def get_summary(self) -> Dict[str, Any]:
        return {
            "task_goal": self.task_goal,
            "pending": self.pending_subtasks,
            "completed": self.completed_subtasks,
            "evidence_count": len(self.evidence),
            "failures": self.failures
        }
