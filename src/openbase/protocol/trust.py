"""
Trust Protocol (TP) - v0.1
Trust as network-native computation
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class TrustNode:
    """信任图中的节点"""
    entity_id: str
    entity_type: str  # runtime | agent | execution
    trust_score: float = 0.5
    evidence_count: int = 0
    peer_validations: List[str] = field(default_factory=list)
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "trust_score": self.trust_score,
            "evidence_count": self.evidence_count,
            "peer_validations": self.peer_validations,
            "last_updated": self.last_updated,
        }


@dataclass
class TrustEdge:
    """信任图中的边"""
    from_entity: str
    to_entity: str
    weight: float = 0.5
    validation_type: str = "direct"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_entity,
            "to": self.to_entity,
            "weight": self.weight,
            "validation_type": self.validation_type,
        }


class TrustCalculator:
    """信任计算引擎 - PageRank-like 传播"""

    @staticmethod
    def calculate(nodes: List[TrustNode], edges: List[TrustEdge]) -> Dict[str, float]:
        """计算所有节点的信任分数"""
        # 简化实现：基于证据数量 + 边权重
        scores = {}
        for node in nodes:
            base_score = 0.5 + min(0.4, node.evidence_count * 0.01)
            peer_boost = sum(e.weight for e in edges if e.to_entity == node.entity_id) * 0.1
            scores[node.entity_id] = min(1.0, base_score + peer_boost)
        return scores