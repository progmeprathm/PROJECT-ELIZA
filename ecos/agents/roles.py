from enum import Enum

class AgentRole(str, Enum):
    PLANNER = "PLANNER"
    RESEARCHER = "RESEARCHER"
    EXECUTOR = "EXECUTOR"
    VERIFIER = "VERIFIER"
    COORDINATOR = "COORDINATOR"
