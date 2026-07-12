#!/usr/bin/env python3
"""
Evidence Engine
"""

import json
import hashlib
from typing import Dict, Any


class EvidenceEngine:
    """证据引擎 - 验证和操作 Evidence"""

    @staticmethod
    def verify_hash(evidence: Dict[str, Any]) -> bool:
        """验证证据哈希"""
        if "proof" not in evidence or "hash" not in evidence["proof"]:
            return False

        # 重新计算哈希
        payload = evidence.get("payload", {})
        content = json.dumps(payload, sort_keys=True)
        computed = f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"

        return computed == evidence["proof"]["hash"]

    @staticmethod
    def verify_signature(evidence: Dict[str, Any]) -> bool:
        """验证签名（示例实现）"""
        # 实际实现应验证 Ed25519 签名
        return evidence.get("proof", {}).get("signature") is not None

    @staticmethod
    def get_evidence_id(evidence: Dict[str, Any]) -> str:
        return evidence.get("evidence_id", "unknown")

    @staticmethod
    def get_event_type(evidence: Dict[str, Any]) -> str:
        return evidence.get("event_type", "UNKNOWN")