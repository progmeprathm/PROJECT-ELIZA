import random
from typing import Dict, Any, List
from ecos.simulation.task_environment import Task
from ecos.simulation.collective_task_generator import CollectiveTaskGenerator

class LongHorizonSimulation:
    def __init__(self, seed: int = 42, num_tasks: int = 25):
        self.generator = CollectiveTaskGenerator(seed)
        self.num_tasks = num_tasks
        
    def generate_sequence(self) -> List[Task]:
        tasks = []
        for i in range(self.num_tasks):
            # Increase difficulty over time, inject failures randomly
            difficulty = min(5, (i // 5) + 1)
            task = self.generator.generate_random_task(difficulty=difficulty)
            task.task_id = f"lh-task-{i:02d}"
            tasks.append(task)
        return tasks
