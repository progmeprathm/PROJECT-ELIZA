from typing import Dict, Any, List
from enum import Enum

class RuntimeLifecycleState(str, Enum):
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    
class KnowledgeState(str, Enum):
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    STALE = "STALE"
    CONFLICTED = "CONFLICTED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"
