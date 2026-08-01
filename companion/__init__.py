"""
ELIZA Companion Package.
"""

from companion.client import ECOSClient
from companion.manager import AssistantProfile, ConversationManager, DecisionReasoningTrace
from companion.shell import CognitiveShell

__all__ = [
    "ConversationManager",
    "AssistantProfile",
    "DecisionReasoningTrace",
    "CognitiveShell",
    "ECOSClient",
]
