import random
from ecos.simulation.task_environment import Task

class TaskGenerator:
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
            
    def generate_task_a(self, difficulty: int, task_id: str) -> Task:
        # Information Retrieval (Memory Challenge)
        # Goal: Find code in room 0, travel multiple rooms, use code in room 3.
        code = random.randint(1000, 9999)
        rooms = [
            {"desc": "Starting room.", "items": {"note": str(code)}},
            {"desc": "Hallway A."},
            {"desc": "Hallway B."},
            {"desc": "Security door.", "lock_code": code, "unlocks_flag": "door_open"},
            {"desc": "Goal room.", "requires_flag": "door_open", "fail_message": "The door is locked."}
        ]
        if difficulty > 1:
            rooms.insert(2, {"desc": "Storage room."})
            rooms.insert(2, {"desc": "Empty room."})
            
        return Task(task_id, "A", difficulty, {"rooms": rooms, "start_pos": 0})
        
    def generate_task_b(self, difficulty: int, task_id: str) -> Task:
        # Arithmetic Tool Use
        # Goal: Find A and B, calculate A*B+C, use result to unlock.
        a = random.randint(10, 50)
        b = random.randint(2, 9)
        rooms = [
            {"desc": "Library.", "items": {"book": str(a)}},
            {"desc": "Office.", "items": {"terminal": str(b)}},
            {"desc": "Vault.", "lock_code": a * b, "unlocks_flag": "vault_open"},
            {"desc": "Goal room.", "requires_flag": "vault_open", "fail_message": "Vault is closed."}
        ]
        return Task(task_id, "B", difficulty, {"rooms": rooms, "start_pos": 0})
        
    def generate_task_c(self, difficulty: int, task_id: str) -> Task:
        # Navigation
        # Just simple navigation but with a specific sequence of items to observe.
        val = random.randint(1, 100)
        rooms = [
            {"desc": "Cell 1.", "items": {"wall": str(val)}},
            {"desc": "Cell 2."},
            {"desc": "Cell 3."},
            {"desc": "Goal room."}
        ]
        return Task(task_id, "C", difficulty, {"rooms": rooms, "start_pos": 0})
        
    def generate_task_d(self, difficulty: int, task_id: str) -> Task:
        # Dependency Planning
        # Must unlock A to access room with code for B.
        code_a = random.randint(10, 99)
        code_b = random.randint(100, 999)
        rooms = [
            {"desc": "Entrance.", "items": {"hint": str(code_a)}},
            {"desc": "Checkpoint 1.", "lock_code": code_a, "unlocks_flag": "cp1"},
            {"desc": "Secure Area.", "requires_flag": "cp1", "fail_message": "Checkpoint 1 locked.", "items": {"safe": str(code_b)}},
            {"desc": "Checkpoint 2.", "requires_flag": "cp1", "fail_message": "Checkpoint 1 locked.", "lock_code": code_b, "unlocks_flag": "cp2"},
            {"desc": "Goal room.", "requires_flag": "cp2", "fail_message": "Checkpoint 2 locked."}
        ]
        return Task(task_id, "D", difficulty, {"rooms": rooms, "start_pos": 0})
        
    def generate_task_e(self, difficulty: int, task_id: str) -> Task:
        # Recovery (Environmental Change)
        # Multiplier changes on cycle 4.
        a = random.randint(10, 20)
        b_initial = random.randint(2, 4)
        b_changed = random.randint(5, 8)
        
        rooms = [
            {"desc": "Room A.", "items": {"note": str(a)}},
            {"desc": "Room B.", "items": {"board": str(b_initial)}},
            {"desc": "Doorway.", "lock_code": a * b_changed, "unlocks_flag": "door_open"},
            {"desc": "Goal room.", "requires_flag": "door_open", "fail_message": "Door is locked."}
        ]
        
        # When agent is calculating and moving, by cycle 4 the board changes.
        # Actually, in TaskEnvironment, we just change the lock_code dynamically, or change the board item.
        # Let's change the board item and the lock code simultaneously.
        dynamic_events = {
            3: {"type": "change_value", "room": 1, "item": "board", "new_value": str(b_changed)}
        }
        
        return Task(task_id, "E", difficulty, {"rooms": rooms, "start_pos": 0, "dynamic_events": dynamic_events})

    def generate_random_task(self, difficulty: int = 1) -> Task:
        families = ["A", "B", "C", "D", "E"]
        family = random.choice(families)
        task_id = f"task-{random.randint(1000,9999)}"
        if family == "A": return self.generate_task_a(difficulty, task_id)
        elif family == "B": return self.generate_task_b(difficulty, task_id)
        elif family == "C": return self.generate_task_c(difficulty, task_id)
        elif family == "D": return self.generate_task_d(difficulty, task_id)
        elif family == "E": return self.generate_task_e(difficulty, task_id)
