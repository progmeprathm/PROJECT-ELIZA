from typing import Any, Dict

class SimpleEnvironment:
    """
    A simple deterministic environment for the minimum cognitive loop experiment.
    Agent exists in a 1D grid. To unlock the door at location 3, it must first 
    discover the password at location 1.
    """
    def __init__(self) -> None:
        self.state = {
            "agent_location": 0,
            "target_location": 4,
            "objects": ["note_at_1", "locked_door_at_3"],
            "password_discovered": False
        }

    def reset(self) -> Dict[str, Any]:
        self.state = {
            "agent_location": 0,
            "target_location": 4,
            "objects": ["note_at_1", "locked_door_at_3"],
            "password_discovered": False
        }
        return self._get_observation()

    def step(self, action: str, action_target: str = "") -> Dict[str, Any]:
        """
        Executes action and returns an observation.
        Valid actions: 'move_forward', 'move_backward', 'read_note', 'unlock_door_XXXX'
        """
        if action == "move_forward":
            if self.state["agent_location"] == 3 and "locked_door_at_3" in self.state["objects"]:
                obs = "Door is locked. Cannot move forward. Requires password."
            else:
                self.state["agent_location"] += 1
                obs = f"Moved to location {self.state['agent_location']}."
        elif action == "move_backward":
            self.state["agent_location"] -= 1
            obs = f"Moved to location {self.state['agent_location']}."
        elif action == "read_note":
            if self.state["agent_location"] == 1 and "note_at_1" in self.state["objects"]:
                obs = "You read the note. It says: 'The password for the door is 8592'."
                self.state["password_discovered"] = True
            else:
                obs = "No note here to read."
        elif action.startswith("unlock_door_"):
            if self.state["agent_location"] == 3:
                if "locked_door_at_3" in self.state["objects"]:
                    pwd = action.split("_")[-1]
                    if pwd == "8592":
                        self.state["objects"].remove("locked_door_at_3")
                        obs = "Correct password. Unlocked the door."
                    else:
                        obs = f"Incorrect password '{pwd}'. Door remains locked."
                else:
                    obs = "Door already unlocked."
            else:
                obs = "Not at the door."
        else:
            obs = f"Unknown action: {action}"
            
        return self._get_observation(message=obs)

    def _get_observation(self, message: str = "Environment initialized.") -> Dict[str, Any]:
        return {
            "message": message,
            "agent_location": self.state["agent_location"],
            "target_location": self.state["target_location"],
            "door_locked": "locked_door_at_3" in self.state["objects"]
        }
