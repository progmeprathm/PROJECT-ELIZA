from enum import Enum
from typing import Dict, Any, List, Optional
import uuid
import time

class MessageType(str, Enum):
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    TASK_RESULT = "TASK_RESULT"
    EVIDENCE = "EVIDENCE"
    PLAN_PROPOSAL = "PLAN_PROPOSAL"
    PLAN_REVISION = "PLAN_REVISION"
    VERIFICATION_REQUEST = "VERIFICATION_REQUEST"
    VERIFICATION_RESULT = "VERIFICATION_RESULT"
    FAILURE_REPORT = "FAILURE_REPORT"
    CLARIFICATION_REQUEST = "CLARIFICATION_REQUEST"
    KNOWLEDGE_REQUEST = "KNOWLEDGE_REQUEST"
    KNOWLEDGE_RESPONSE = "KNOWLEDGE_RESPONSE"
    FINAL_RESULT = "FINAL_RESULT"

class Message:
    def __init__(self, sender: str, recipient: str, message_type: MessageType, task_id: str, payload: Dict[str, Any], evidence: List[Any] = None, provenance: List[str] = None):
        self.message_id = f"msg-{uuid.uuid4().hex[:8]}"
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type
        self.task_id = task_id
        self.payload = payload
        self.evidence = evidence or []
        self.timestamp = time.time()
        self.provenance = provenance or []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "task_id": self.task_id,
            "payload": self.payload,
            "evidence": self.evidence,
            "timestamp": self.timestamp,
            "provenance": self.provenance
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        msg = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            message_type=MessageType(data["message_type"]),
            task_id=data["task_id"],
            payload=data["payload"],
            evidence=data.get("evidence", []),
            provenance=data.get("provenance", [])
        )
        msg.message_id = data.get("message_id", msg.message_id)
        msg.timestamp = data.get("timestamp", msg.timestamp)
        return msg
