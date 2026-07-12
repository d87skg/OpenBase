#!/usr/bin/env python3
"""
Certificate Engine

最小闭环: Evidence → Verification → Certificate
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class CertificateEngine:
    """证书引擎"""

    def __init__(self, evidence_dir: str = "./evidence"):
        self.evidence_dir = Path(evidence_dir)
        self.evidence: List[Dict[str, Any]] = []

    def load_evidence(self) -> "CertificateEngine":
        """加载证据"""
        if not self.evidence_dir.exists():
            print(f"❌ 证据目录不存在: {self.evidence_dir}")
            return self

        files = list(self.evidence_dir.glob("*.json"))
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    self.evidence.append(json.load(fp))
            except Exception as e:
                print(f"⚠️ 跳过 {f.name}: {e}")

        print(f"✅ 加载了 {len(self.evidence)} 条证据")
        return self

    def verify(self) -> Dict[str, Any]:
        """验证证据完整性"""
        if len(self.evidence) < 3:
            return {
                "status": "FAILED",
                "reason": f"证据不足: 需要至少 3 条，当前 {len(self.evidence)} 条"
            }

        event_types = [e.get("event_type") for e in self.evidence]
        has_started = "AGENT_STARTED" in event_types
        has_finished = "AGENT_FINISHED" in event_types

        if not has_started or not has_finished:
            return {
                "status": "FAILED",
                "reason": "缺少 AGENT_STARTED 或 AGENT_FINISHED 事件"
            }

        return {"status": "PASS", "reason": "验证通过"}

    def issue_certificate(self, runtime_id: str, level: str = "BRONZE") -> Dict[str, Any]:
        """颁发证书"""
        verification = self.verify()

        if verification["status"] != "PASS":
            print(f"❌ 验证失败: {verification['reason']}")
            return verification

        certificate_id = f"cert-{uuid.uuid4().hex[:8]}"
        now = datetime.now()

        levels = {
            "BRONZE": 90,
            "SILVER": 180,
            "GOLD": 365,
            "PLATINUM": 365
        }

        days = levels.get(level, 90)
        expires_at = now + timedelta(days=days)

        certificate = {
            "certificate_id": certificate_id,
            "runtime_id": runtime_id,
            "level": level,
            "status": "ACTIVE",
            "issued_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "evidence_count": len(self.evidence),
            "verification": verification
        }

        print(f"✅ 证书已颁发: {certificate_id} ({level})")
        print(f"   📅 有效期: {days} 天")
        print(f"   📄 证据数: {len(self.evidence)}")

        return certificate

    def save_certificate(self, certificate: Dict[str, Any], output_dir: str = "./reports") -> None:
        """保存证书"""
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        filename = path / f"{certificate['certificate_id']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(certificate, f, indent=2)

        print(f"   💾 已保存: {filename.absolute()}")
