"""
Cognitive Communication Protocol (CCP) Package for ELIZA.
Enforces ELIZA_PROTOCOL.md Version 1.0 (Canonical Inter-Module Communication Standard).
"""

from eliza.protocol.ccp import (
    CCPHeader,
    CCPMetadata,
    CCPMessage,
    CCPTrace,
    CCPEncoderDecoder,
    MessagePriority,
    MessageType,
    ProtocolInvariantValidator,
)
from eliza.protocol.bus import CCPEventBus

__all__ = [
    "MessageType",
    "MessagePriority",
    "CCPHeader",
    "CCPMetadata",
    "CCPTrace",
    "CCPMessage",
    "CCPEncoderDecoder",
    "ProtocolInvariantValidator",
    "CCPEventBus",
]
