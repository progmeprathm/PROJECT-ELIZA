from typing import Dict, Any

class PlanningWorld:
    """
    A controlled deterministic environment for testing multi-step planning,
    tool use (calculator), and episodic memory.
    """
    def __init__(self):
        self.start_pos = 0
        self.note_pos = 1
        self.wall_pos = 2
        self.door_pos = 3
        self.goal_pos = 4
        
        self.base_code = 12
        self.multiplier = 4
        self.reset()
        
    def reset(self) -> Dict[str, Any]:
        self.agent_pos = self.start_pos
        self.door_locked = True
        self.door_code_changed = False
        return self._get_observation()
        
    def inject_environmental_change(self):
        # Used for Failure C - Environmental Change
        # E.g. multiplier changed, invalidating previous calculation
        self.multiplier = 5
        self.door_code_changed = True

    def _get_observation(self, extra_msg: str = "") -> Dict[str, Any]:
        msg = extra_msg
        
        if not msg:
            if self.agent_pos == self.note_pos:
                msg = "You are in Room A. There is a note on the desk."
            elif self.agent_pos == self.wall_pos:
                msg = "You are in Room B. There is writing on the wall."
                if self.door_code_changed:
                    msg += " You notice the writing has been recently altered."
            elif self.agent_pos == self.door_pos:
                if self.door_locked:
                    msg = "You are facing a locked mechanism requiring a calculated code."
                else:
                    msg = "The mechanism is unlocked. The path is clear."
            elif self.agent_pos == self.goal_pos:
                msg = "You have reached the final destination."
            else:
                msg = f"You are standing in the hallway at position {self.agent_pos}."
                
        return {
            "agent_location": self.agent_pos,
            "door_locked": self.door_locked,
            "message": msg
        }
        
    def step(self, action: str, reasoning: str = "") -> Dict[str, Any]:
        if action == "move_east":
            if self.agent_pos == self.door_pos and self.door_locked:
                return self._get_observation("The locked mechanism prevents you from moving east.")
            if self.agent_pos < self.goal_pos:
                self.agent_pos += 1
            return self._get_observation()
            
        elif action == "move_west":
            if self.agent_pos > 0:
                self.agent_pos -= 1
            return self._get_observation()
            
        elif action == "read_note" and self.agent_pos == self.note_pos:
            return self._get_observation(f"The note reads: 'The base code is {self.base_code}'.")
            
        elif action == "read_wall" and self.agent_pos == self.wall_pos:
            return self._get_observation(f"The wall writing says: 'The multiplier is {self.multiplier}'.")
            
        elif action.startswith("unlock_door_"):
            if self.agent_pos != self.door_pos:
                return self._get_observation("There is no lock here.")
                
            code = action.split("_")[-1]
            try:
                if int(code) == (self.base_code * self.multiplier):
                    self.door_locked = False
                    return self._get_observation("Correct code. The mechanism unlocks.")
                else:
                    return self._get_observation("Incorrect code.")
            except ValueError:
                return self._get_observation("Invalid code format.")
                
        else:
            return self._get_observation("Unknown or invalid action.")
