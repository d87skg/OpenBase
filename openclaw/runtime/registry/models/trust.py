"""
OpenBase Registry - Trust Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TrustRecord:
    runtime_id: str
    runtime_name: str
    trust_score: float = 0.0
    certificate_count: int = 0
    revoked_count: int = 0
    replay_success_rate: float = 0.0
    verification_status: str = "UNKNOWN"
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "runtime_id": self.runtime_id,
            "runtime_name": self.runtime_name,
            "trust_score": self.trust_score,
            "certificate_count": self.certificate_count,
            "revoked_count": self.revoked_count,
            "replay_success_rate": self.replay_success_rate,
            "verification_status": self.verification_status,
            "last_updated": self.last_updated.isoformat()
        }

    @staticmethod
    def from_dict(data: dict) -> "TrustRecord":
        return TrustRecord(
            runtime_id=data["runtime_id"],
            runtime_name=data["runtime_name"],
            trust_score=data.get("trust_score", 0.0),
            certificate_count=data.get("certificate_count", 0),
            revoked_count=data.get("revoked_count", 0),
            replay_success_rate=data.get("replay_success_rate", 0.0),
            verification_status=data.get("verification_status", "UNKNOWN"),
            last_updated=datetime.fromisoformat(data["last_updated"]) if "last_updated" in data else datetime.now()
        )
