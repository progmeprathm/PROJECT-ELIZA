import random
from typing import Dict, Any, Tuple

class Grid2DEnvironment:
    """
    A 2D GridWorld Environment for testing semantic memory generalization.
    Supports basic x/y movement, natural language variations, and a locked door puzzle.
    """
    def __init__(self, width: int = 4, height: int = 4):
        self.width = width
        self.height = height
        self.start_pos = (0, 0)
        self.note_pos = (1, 1)
        self.door_pos = (2, 2)
        self.goal_pos = (3, 3)
        self.password = "8592"
        self.reset()
        
    def reset(self) -> Dict[str, Any]:
        self.agent_pos = self.start_pos
        self.door_locked = True
        self.note_read = False
        return self._get_observation()
        
    def _get_observation(self, extra_msg: str = "") -> Dict[str, Any]:
        msg = extra_msg
        
        # Room context variations
        if not msg:
            if self.agent_pos == self.note_pos:
                msg = "You are in a room with a desk. There is a piece of paper here."
            elif self.agent_pos == self.door_pos:
                if self.door_locked:
                    msg = "You are facing a heavy steel door with a digital keypad. It is locked."
                else:
                    msg = "You are facing an open doorway leading towards the exit."
            elif self.agent_pos == self.goal_pos:
                msg = "You have reached the final destination."
            else:
                msg = f"You are standing in an empty corridor at coordinates {self.agent_pos}."
                
        return {
            "agent_location": self.agent_pos,
            "door_locked": self.door_locked,
            "message": msg
        }
        
    def step(self, action: str, reasoning: str = "") -> Dict[str, Any]:
        if action == "move_north" and self.agent_pos[1] < self.height - 1:
            if self.agent_pos == (self.door_pos[0], self.door_pos[1]-1) and self.door_locked:
                return self._get_observation("You bumped into the locked door. You cannot pass.")
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] + 1)
            return self._get_observation()
            
        elif action == "move_south" and self.agent_pos[1] > 0:
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] - 1)
            return self._get_observation()
            
        elif action == "move_east" and self.agent_pos[0] < self.width - 1:
            if self.agent_pos == (self.door_pos[0]-1, self.door_pos[1]) and self.door_locked:
                return self._get_observation("You bumped into the locked door. You cannot pass.")
            self.agent_pos = (self.agent_pos[0] + 1, self.agent_pos[1])
            return self._get_observation()
            
        elif action == "move_west" and self.agent_pos[0] > 0:
            self.agent_pos = (self.agent_pos[0] - 1, self.agent_pos[1])
            return self._get_observation()
            
        elif action == "read_note" and self.agent_pos == self.note_pos:
            self.note_read = True
            variations = [
                f"You notice a small note containing the access code {self.password}.",
                f"The paper beside you says the entry number is {self.password}.",
                f"Written on the card is the credential: {self.password}."
            ]
            return self._get_observation(random.choice(variations))
            
        elif action.startswith("unlock_door_"):
            if self.agent_pos != self.door_pos and self.agent_pos not in [(self.door_pos[0]-1, self.door_pos[1]), (self.door_pos[0], self.door_pos[1]-1)]:
                return self._get_observation("There is no door here to unlock.")
                
            code = action.split("_")[-1]
            if code == self.password:
                self.door_locked = False
                return self._get_observation("Correct password. The heavy steel door clicks open.")
            else:
                return self._get_observation("Incorrect password. The door remains locked.")
                
        else:
            return self._get_observation("Unknown or invalid action.")
