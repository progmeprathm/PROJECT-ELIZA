import random
from typing import Dict, Any, List

class Task:
    def __init__(self, task_id: str, family: str, difficulty: int, parameters: Dict[str, Any]):
        self.task_id = task_id
        self.family = family
        self.difficulty = difficulty
        self.parameters = parameters

class TaskEnvironment:
    def __init__(self, task: Task):
        self.task = task
        self.agent_pos = 0
        self.inventory = []
        self.flags = {}
        self.cycle_count = 0
        self.goal_completed = False
        self._setup_from_task()
        
    def _setup_from_task(self):
        p = self.task.parameters
        self.rooms = p.get("rooms", [])  # List of dicts with 'id', 'desc', 'items', 'requires', 'fail_message'
        self.goal_pos = len(self.rooms) - 1
        self.agent_pos = p.get("start_pos", 0)
        self.dynamic_events = p.get("dynamic_events", {}) # e.g. { cycle: { "type": "change_code", "room": 2, "new_code": 99 } }
        
    def get_observation(self, extra_msg: str = "") -> Dict[str, Any]:
        room = self.rooms[self.agent_pos]
        msg = extra_msg
        if not msg:
            msg = room.get("desc", f"You are in room {self.agent_pos}.")
            if "items" in room and room["items"]:
                items_str = ", ".join(room["items"].keys())
                msg += f" You see: {items_str}."
        
        return {
            "agent_location": self.agent_pos,
            "message": msg
        }
        
    def step(self, action: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        self.cycle_count += 1
        
        # Trigger dynamic events
        if self.cycle_count in self.dynamic_events:
            event = self.dynamic_events[self.cycle_count]
            if event["type"] == "change_value":
                room = self.rooms[event["room"]]
                room["items"][event["item"]] = event["new_value"]
                
        # Parse action
        if action == "move_east":
            return self._move(1)
        elif action == "move_west":
            return self._move(-1)
        elif action.startswith("interact_"):
            item_name = action.replace("interact_", "")
            return self._interact(item_name, arguments)
        elif action.startswith("unlock_"):
            code = action.replace("unlock_", "")
            return self._unlock(code)
        else:
            return self.get_observation("Unknown action.")
            
    def _move(self, delta: int) -> Dict[str, Any]:
        new_pos = self.agent_pos + delta
        if 0 <= new_pos < len(self.rooms):
            target_room = self.rooms[new_pos]
            if "requires_flag" in target_room and not self.flags.get(target_room["requires_flag"]):
                return self.get_observation(target_room.get("fail_message", "Access denied."))
            self.agent_pos = new_pos
            if self.agent_pos == self.goal_pos:
                self.goal_completed = True
                return self.get_observation("You have reached the goal!")
            return self.get_observation()
        return self.get_observation("You cannot move that way.")
        
    def _interact(self, item_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        room = self.rooms[self.agent_pos]
        if "items" in room and item_name in room["items"]:
            val = room["items"][item_name]
            return self.get_observation(f"The {item_name} reads: {val}")
        return self.get_observation(f"No {item_name} here.")
        
    def _unlock(self, code: str) -> Dict[str, Any]:
        room = self.rooms[self.agent_pos]
        if "lock_code" in room:
            try:
                # Can be dynamic code or static
                expected = room["lock_code"]
                if code == str(expected):
                    self.flags[room["unlocks_flag"]] = True
                    return self.get_observation("Mechanism unlocked!")
                else:
                    return self.get_observation("Incorrect code.")
            except Exception:
                return self.get_observation("Invalid code format.")
        return self.get_observation("Nothing to unlock here.")
