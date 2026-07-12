from typing import List, Dict, Any


class TrustProvider:
    """信任提供者接口"""

    def calculate(self, evidence: List[Dict[str, Any]]) -> float:
        raise NotImplementedError

    def explain(self, evidence: List[Dict[str, Any]]) -> str:
        raise NotImplementedError


class SimpleTrustProvider(TrustProvider):
    """简单信任提供者 - 基于证据数量"""

    def calculate(self, evidence: List[Dict[str, Any]]) -> float:
        count = len(evidence)
        if count == 0:
            return 0.0
        elif count <= 2:
            return 0.3
        elif count <= 4:
            return 0.6
        elif count <= 9:
            return 0.8
        else:
            return 0.95

    def explain(self, evidence: List[Dict[str, Any]]) -> str:
        count = len(evidence)
        if count == 0:
            return "尚无证据"
        elif count <= 2:
            return "证据较少，信任分数较低"
        elif count <= 4:
            return "证据充足，信任分数中等"
        elif count <= 9:
            return "证据丰富，信任分数较高"
        else:
            return "证据充足，信任分数高"
