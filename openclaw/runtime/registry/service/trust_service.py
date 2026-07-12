"""
OpenBase Registry - Trust Service
"""

from typing import Optional, List
from datetime import datetime, timedelta

from ..models import TrustRecord, CertificateLevel
from ..storage import BaseStore


class TrustService:
    def __init__(self, store: BaseStore):
        self.store = store
        self._collection = "trust"

    def compute_score(self, runtime_id: str, certificates: List, evidence_count: int = 0) -> float:
        """计算信任分数（基于证书等级、数量和证据）"""
        if not certificates:
            return 0.3  # 无证书默认低分

        active_certs = [c for c in certificates if c.status.value == "ACTIVE"]
        if not active_certs:
            return 0.2  # 无活跃证书

        # 1. 证书等级分数
        level_scores = {
            "BRONZE": 0.6,
            "SILVER": 0.75,
            "GOLD": 0.88,
            "PLATINUM": 0.95
        }

        # 取最高等级证书
        best_cert = max(active_certs, key=lambda c: level_scores.get(c.level.value, 0.5))
        base_score = level_scores.get(best_cert.level.value, 0.5)

        # 2. 证书数量加成（最多 +0.08）
        cert_count_bonus = min(0.08, len(active_certs) * 0.015)

        # 3. 证据数量加成（最多 +0.05）
        evidence_bonus = min(0.05, evidence_count * 0.001)

        # 4. 时间衰减：旧证书略有衰减（1年内有效）
        now = datetime.now()
        age_days = (now - best_cert.issued_at).days
        time_bonus = max(0, 0.02 - age_days * 0.0001)  # 365天后衰减0.0365

        # 5. 撤销惩罚：如果有撤销记录，扣分
        revoked_count = len([c for c in certificates if c.status.value == "REVOKED"])
        revocation_penalty = min(0.15, revoked_count * 0.05)

        total = base_score + cert_count_bonus + evidence_bonus + time_bonus - revocation_penalty
        return max(0.0, min(1.0, total))

    def get(self, runtime_id: str) -> Optional[TrustRecord]:
        data = self.store.get(self._collection, runtime_id)
        if data:
            return TrustRecord.from_dict(data)
        return None

    def update(self, runtime_id: str, runtime_name: str,
               certificate_count: int = 0,
               revoked_count: int = 0,
               replay_success_rate: float = 0.0,
               verification_status: str = "UNKNOWN") -> TrustRecord:
        existing = self.get(runtime_id)
        trust_score = 0.5  # 默认值，会被 compute_score 覆盖

        if existing:
            record = TrustRecord(
                runtime_id=runtime_id,
                runtime_name=runtime_name,
                trust_score=trust_score,
                certificate_count=certificate_count,
                revoked_count=revoked_count,
                replay_success_rate=replay_success_rate,
                verification_status=verification_status
            )
            self.store.update(self._collection, runtime_id, record.to_dict())
            return record
        else:
            record = TrustRecord(
                runtime_id=runtime_id,
                runtime_name=runtime_name,
                trust_score=trust_score,
                certificate_count=certificate_count,
                revoked_count=revoked_count,
                replay_success_rate=replay_success_rate,
                verification_status=verification_status
            )
            self.store.create(self._collection, record.to_dict())
            return record

    def list_all(self) -> List[TrustRecord]:
        items = self.store.list(self._collection)
        return [TrustRecord.from_dict(item) for item in items]

    def get_ranking(self, limit: int = 10) -> List[TrustRecord]:
        records = self.list_all()
        records.sort(key=lambda r: r.trust_score, reverse=True)
        return records[:limit]
