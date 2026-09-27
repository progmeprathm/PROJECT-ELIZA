import random
from typing import Dict, Any, List
from ecos.simulation.task_environment import Task

class CollectiveTaskGenerator:
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
            
    def generate_task_a(self, difficulty: int, task_id: str) -> Task:
        # A - Decomposition: Independent subtasks
        # Requires parallel extraction
        num_items = difficulty * 2
        rooms = [{"desc": f"Room {i}", "items": {f"part_{i}": str(random.randint(1, 99))}} for i in range(num_items)]
        rooms.append({"desc": "Goal room.", "lock_code": 999, "unlocks_flag": "goal"})
        return Task(task_id, "A", difficulty, {"rooms": rooms, "start_pos": 0})
        
    def generate_task_b(self, difficulty: int, task_id: str) -> Task:
        # B - Dependency: Subtasks have dependencies
        code_a = random.randint(10, 99)
        code_b = random.randint(100, 999)
        rooms = [
            {"desc": "Entrance.", "items": {"hint": str(code_a)}},
            {"desc": "Checkpoint 1.", "lock_code": code_a, "unlocks_flag": "cp1"},
            {"desc": "Secure Area.", "requires_flag": "cp1", "items": {"safe": str(code_b)}},
            {"desc": "Goal room.", "lock_code": code_b, "unlocks_flag": "cp2", "requires_flag": "cp1"}
        ]
        return Task(task_id, "B", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_c(self, difficulty: int, task_id: str) -> Task:
        # C - Verification: One generates, another validates.
        val1 = random.randint(10, 20)
        val2 = random.randint(2, 5)
        # The agent must correctly verify val1 * val2
        rooms = [
            {"desc": "Workstation.", "items": {"a": str(val1), "b": str(val2)}},
            {"desc": "Goal room.", "lock_code": val1 * val2, "unlocks_flag": "door"}
        ]
        return Task(task_id, "C", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_d(self, difficulty: int, task_id: str) -> Task:
        # D - Failure Recovery
        rooms = [
            {"desc": "Terminal.", "items": {"pass": "4444"}},
            {"desc": "Goal room.", "lock_code": 4444, "unlocks_flag": "door"}
        ]
        # In mock benchmark, we inject failure on the first execution.
        return Task(task_id, "D", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_e(self, difficulty: int, task_id: str) -> Task:
        # E - Collective Memory: Episode helps B
        code = random.randint(1000, 9999)
        rooms = [
            {"desc": "Archive.", "items": {"secret": str(code)}},
            {"desc": "Goal room.", "lock_code": code, "unlocks_flag": "door"}
        ]
        return Task(task_id, "E", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_f(self, difficulty: int, task_id: str) -> Task:
        # F - Coordination Transfer
        rooms = [
            {"desc": "Room 1.", "items": {"v1": "10", "v2": "5"}},
            {"desc": "Goal room.", "lock_code": 50, "unlocks_flag": "door"}
        ]
        return Task(task_id, "F", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_g(self, difficulty: int, task_id: str) -> Task:
        # G - Conflict Resolution
        rooms = [
            {"desc": "Room 1.", "items": {"hint": "99"}},
            {"desc": "Room 2.", "items": {"hint": "88"}},
            {"desc": "Goal room.", "lock_code": 88, "unlocks_flag": "door"}
        ]
        return Task(task_id, "G", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_task_h(self, difficulty: int, task_id: str) -> Task:
        # H - Adaptive Delegation
        # Difficulty scales number of subtasks
        rooms = [{"desc": f"Room {i}", "items": {"val": str(i)}} for i in range(difficulty * 3)]
        rooms.append({"desc": "Goal room."})
        return Task(task_id, "H", difficulty, {"rooms": rooms, "start_pos": 0})

    def generate_random_task(self, difficulty: int = 1) -> Task:
        families = ["A", "B", "C", "D", "E", "F", "G", "H"]
        family = random.choice(families)
        task_id = f"task-{random.randint(1000,9999)}"
        method = getattr(self, f"generate_task_{family.lower()}")
        return method(difficulty, task_id)
