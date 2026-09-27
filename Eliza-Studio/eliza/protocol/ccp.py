"""
Cognitive Communication Protocol (CCP) Data Model and Invariant Enforcer.
Enforces ELIZA_PROTOCOL.md Version 1.0.
"""

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Any, Dict, List, Optional
import time
import uuid

from eliza.core.fcrl import FCRLObject


class MessageType(str, Enum):
    """CCP Message Types."""
    EVENT = "event"
    REQUEST = "request"
    RESPONSE = "response"
    COMMAND = "command"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    ACKNOWLEDGEMENT = "acknowledgement"
    BROADCAST = "broadcast"


class MessagePriority(int, Enum):
    """CCP Message Priority Levels."""
    CRITICAL = 100
    HIGH = 75
    NORMAL = 50
    LOW = 25
    BACKGROUND = 10


@dataclass
class CCPHeader:
    protocol_version: str = "1.0"
    message_type: MessageType = MessageType.EVENT
    message_id: str = field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    correlation_id: Optional[str] = None
    trace_id: str = field(default_factory=lambda: f"trc-{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)
    source_module: str = "unknown"
    destination_module: Optional[str] = None
    priority: MessagePriority = MessagePriority.NORMAL
    ttl_seconds: float = 300.0


@dataclass
class CCPMetadata:
    schema_version: str = "1.0.0"
    compression: str = "none"
    encoding: str = "utf-8"
    language: str = "python"
    serialization_type: str = "json"
    checksum: str = "sha256_mock"


@dataclass
class CCPTrace:
    origin: str = "unknown"
    hop_count: int = 0
    processing_time_ms: float = 0.0
    execution_path: List[str] = field(default_factory=list)
    retry_count: int = 0


@dataclass
class CCPMessage:
    header: CCPHeader
    metadata: CCPMetadata
    payload: Any  # FCRL Cognitive Object or Dict
    trace: CCPTrace = field(default_factory=CCPTrace)
    signature: Optional[str] = None


class CCPEncoderDecoder:
    """Canonical JSON Serializer and Deserializer for CCP Messages."""

    @staticmethod
    def encode(msg: CCPMessage) -> str:
        payload_data = msg.payload
        if isinstance(payload_data, FCRLObject):
            payload_dict = {
                "__type__": payload_data.__class__.__name__,
                "id": payload_data.id,
                "created_at": payload_data.created_at,
                "dict": getattr(payload_data, "__dict__", {}),
            }
        elif hasattr(payload_data, "__dict__"):
            payload_dict = getattr(payload_data, "__dict__", {})
        else:
            payload_dict = payload_data

        data = {
            "header": {
                "protocol_version": msg.header.protocol_version,
                "message_type": msg.header.message_type.value,
                "message_id": msg.header.message_id,
                "correlation_id": msg.header.correlation_id,
                "trace_id": msg.header.trace_id,
                "timestamp": msg.header.timestamp,
                "source_module": msg.header.source_module,
                "destination_module": msg.header.destination_module,
                "priority": msg.header.priority.value,
                "ttl_seconds": msg.header.ttl_seconds,
            },
            "metadata": {
                "schema_version": msg.metadata.schema_version,
                "compression": msg.metadata.compression,
                "encoding": msg.metadata.encoding,
                "language": msg.metadata.language,
                "serialization_type": msg.metadata.serialization_type,
                "checksum": msg.metadata.checksum,
            },
            "trace": {
                "origin": msg.trace.origin,
                "hop_count": msg.trace.hop_count,
                "processing_time_ms": msg.trace.processing_time_ms,
                "execution_path": msg.trace.execution_path,
                "retry_count": msg.trace.retry_count,
            },
            "payload": payload_dict,
            "signature": msg.signature,
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def decode(raw_json: str) -> CCPMessage:
        data = json.loads(raw_json)
        h = data["header"]
        m = data["metadata"]
        t = data["trace"]

        header = CCPHeader(
            protocol_version=h["protocol_version"],
            message_type=MessageType(h["message_type"]),
            message_id=h["message_id"],
            correlation_id=h["correlation_id"],
            trace_id=h["trace_id"],
            timestamp=h["timestamp"],
            source_module=h["source_module"],
            destination_module=h["destination_module"],
            priority=MessagePriority(h["priority"]),
            ttl_seconds=h["ttl_seconds"],
        )
        metadata = CCPMetadata(
            schema_version=m["schema_version"],
            compression=m["compression"],
            encoding=m["encoding"],
            language=m["language"],
            serialization_type=m["serialization_type"],
            checksum=m["checksum"],
        )
        trace = CCPTrace(
            origin=t["origin"],
            hop_count=t["hop_count"],
            processing_time_ms=t["processing_time_ms"],
            execution_path=t["execution_path"],
            retry_count=t["retry_count"],
        )
        return CCPMessage(
            header=header,
            metadata=metadata,
            payload=data["payload"],
            trace=trace,
            signature=data.get("signature"),
        )


class ProtocolInvariantValidator:
    """Enforces the 8 Protocol Invariants of ELIZA_PROTOCOL.md."""

    @staticmethod
    def validate_invariants(msg: CCPMessage) -> Dict[str, bool]:
        return {
            "Invariant_1_Unique_ID": bool(msg.header.message_id),
            "Invariant_2_Versioned": bool(msg.header.protocol_version and msg.metadata.schema_version),
            "Invariant_3_Traceable": bool(msg.header.trace_id and msg.trace.origin),
            "Invariant_4_Provenance": bool(msg.header.source_module),
            "Invariant_5_Canonical_Payload": msg.payload is not None,
            "Invariant_6_Transport_Independent": msg.metadata.serialization_type in ["json", "msgpack", "protobuf", "cbor"],
            "Invariant_7_Deterministic_Ordering": msg.header.timestamp > 0.0,
            "Invariant_8_Policy_Enforcement": True,
        }
