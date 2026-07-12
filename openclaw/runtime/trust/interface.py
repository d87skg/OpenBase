#!/usr/bin/env python3
"""
Trust Provider Interface

定义可插拔的信任计算接口，不锁定具体算法。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class TrustProvider(ABC):
    """
    信任提供者接口

    所有信任计算实现必须实现此接口。
    """

    @abstractmethod
    def calculate(self, evidence: List[Dict[str, Any]]) -> float:
        """
        计算信任分数

        Args:
            evidence: 证据列表

        Returns:
            信任分数 (0.0 - 1.0)
        """
        pass

    @abstractmethod
    def verify(self, score: float, threshold: float = 0.6) -> bool:
        """
        验证信任分数是否达到阈值

        Args:
            score: 信任分数
            threshold: 阈值 (默认 0.6)

        Returns:
            True 如果分数 >= 阈值
        """
        return score >= threshold

    @abstractmethod
    def explain(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        解释信任分数的计算依据

        Args:
            evidence: 证据列表

        Returns:
            解释信息
        """
        pass


class SimpleTrustProvider(TrustProvider):
    """
    简单信任提供者（默认实现）

    基于证据数量计算信任分数：
    - 0 条证据: 0.0
    - 1-2 条: 0.3
    - 3-4 条: 0.6
    - 5-9 条: 0.8
    - 10+ 条: 0.95
    """

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

    def verify(self, score: float, threshold: float = 0.6) -> bool:
        return score >= threshold

    def explain(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        count = len(evidence)
        score = self.calculate(evidence)

        explanation = f"基于 {count} 条证据计算信任分数"

        if count == 0:
            detail = "尚无证据，信任分数为 0"
        elif count <= 2:
            detail = "证据较少，信任分数较低"
        elif count <= 4:
            detail = "证据充足，信任分数中等"
        elif count <= 9:
            detail = "证据丰富，信任分数较高"
        else:
            detail = "证据充足，信任分数高"

        return {
            "score": score,
            "evidence_count": count,
            "explanation": explanation,
            "detail": detail,
            "verified": self.verify(score)
        }


class WeightedTrustProvider(TrustProvider):
    """
    加权信任提供者

    基于证据类型加权计算：
    - AGENT_STARTED: +0.1
    - LLM_CALL: +0.2
    - TOOL_CALL: +0.2
    - TOOL_RESULT: +0.2
    - AGENT_FINISHED: +0.1
    - ERROR: -0.3
    """

    WEIGHTS = {
        "AGENT_STARTED": 0.1,
        "LLM_CALL": 0.2,
        "TOOL_CALL": 0.2,
        "TOOL_RESULT": 0.2,
        "AGENT_FINISHED": 0.1,
        "ERROR": -0.3,
    }

    def calculate(self, evidence: List[Dict[str, Any]]) -> float:
        score = 0.0
        for ev in evidence:
            event_type = ev.get("event_type", "")
            score += self.WEIGHTS.get(event_type, 0.0)

        # 确保分数在 0.0 - 1.0 之间
        return max(0.0, min(1.0, score))

    def verify(self, score: float, threshold: float = 0.6) -> bool:
        return score >= threshold

    def explain(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = self.calculate(evidence)
        breakdown = []

        for ev in evidence:
            event_type = ev.get("event_type", "")
            weight = self.WEIGHTS.get(event_type, 0.0)
            breakdown.append({
                "event_type": event_type,
                "weight": weight
            })

        return {
            "score": score,
            "evidence_count": len(evidence),
            "breakdown": breakdown,
            "verified": self.verify(score)
        }