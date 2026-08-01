"""
Layer 2: Cognitive Networking Node over CCP.
Inter-mind P2P communication layer enforcing observable CCP message delivery.
"""

from typing import Any, Callable, Dict, List, Optional

from eliza.protocol.bus import CCPEventBus
from eliza.protocol.ccp import CCPHeader, CCPMetadata, CCPMessage, MessageType


class CognitiveNetworkNode:
    """
    P2P Network Node linking specialized minds across the cognitive civilization network.
    """

    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.bus = CCPEventBus()
        self._peer_nodes: Dict[str, "CognitiveNetworkNode"] = {}

    def connect_peer(self, peer: "CognitiveNetworkNode") -> None:
        self._peer_nodes[peer.node_id] = peer
        peer._peer_nodes[self.node_id] = self

    def send_ccp_message(self, recipient_node_id: str, payload: Any, msg_type: MessageType = MessageType.EVENT) -> bool:
        header = CCPHeader(
            message_type=msg_type,
            source_module=self.node_id,
            destination_module=recipient_node_id,
        )
        msg = CCPMessage(header=header, metadata=CCPMetadata(), payload=payload)

        # Publish locally
        self.bus.publish(msg)

        # Route to peer if connected
        if recipient_node_id in self._peer_nodes:
            self._peer_nodes[recipient_node_id].bus.publish(msg)
            return True
        return False
