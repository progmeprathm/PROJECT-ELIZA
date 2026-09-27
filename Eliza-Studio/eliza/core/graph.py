"""
Cognitive Graph Representation for ELIZA.
Enforces ELIZA_FORMALISM.md: C = (O, E, B, K, G, P, D, A, M, W).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from eliza.core.fcrl import FCRLObject


@dataclass
class CognitiveEdge:
    source_id: str
    target_id: str
    relation_label: str
    weight: float = 1.0


class CognitiveGraph:
    """
    Directed labeled graph representing the complete cognitive state C = (O, E, B, K, G, P, D, A, M, W).
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, FCRLObject] = {}
        self.edges: List[CognitiveEdge] = []

    def add_node(self, node: FCRLObject) -> None:
        self.nodes[node.id] = node

    def add_edge(self, source_id: str, target_id: str, relation_label: str, weight: float = 1.0) -> None:
        if source_id in self.nodes and target_id in self.nodes:
            self.edges.append(CognitiveEdge(source_id=source_id, target_id=target_id, relation_label=relation_label, weight=weight))

    def get_neighbors(self, node_id: str, relation_label: Optional[str] = None) -> List[FCRLObject]:
        neighbors = []
        for edge in self.edges:
            if edge.source_id == node_id:
                if relation_label is None or edge.relation_label == relation_label:
                    if edge.target_id in self.nodes:
                        neighbors.append(self.nodes[edge.target_id])
        return neighbors

    def get_nodes_of_type(self, cls: type) -> List[FCRLObject]:
        return [node for node in self.nodes.values() if isinstance(node, cls)]

    def to_state_summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for node in self.nodes.values():
            name = node.__class__.__name__
            counts[name] = counts.get(name, 0) + 1
        return counts
