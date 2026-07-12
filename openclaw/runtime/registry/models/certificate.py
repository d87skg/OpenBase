"""
OpenBase Registry - Certificate Model
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class CertificateStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class CertificateLevel(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


@dataclass
class Certificate:
    cert_id: str
    runtime_id: str
    runtime_name: str
    level: CertificateLevel
    status: CertificateStatus = CertificateStatus.ACTIVE
    trust_score: float = 0.0
    issued_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=365))
    revoked_at: Optional[datetime] = None
    revocation_reason: Optional[str] = None
    verification_summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "cert_id": self.cert_id,
            "runtime_id": self.runtime_id,
            "runtime_name": self.runtime_name,
            "level": self.level.value,
            "status": self.status.value,
            "trust_score": self.trust_score,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
            "revocation_reason": self.revocation_reason,
            "verification_summary": self.verification_summary
        }

    @staticmethod
    def from_dict(data: dict) -> "Certificate":
        return Certificate(
            cert_id=data["cert_id"],
            runtime_id=data["runtime_id"],
            runtime_name=data["runtime_name"],
            level=CertificateLevel(data["level"]),
            status=CertificateStatus(data.get("status", "ACTIVE")),
            trust_score=data.get("trust_score", 0.0),
            issued_at=datetime.fromisoformat(data["issued_at"]) if "issued_at" in data else datetime.now(),
            expires_at=datetime.fromisoformat(data["expires_at"]) if "expires_at" in data else datetime.now() + timedelta(days=365),
            revoked_at=datetime.fromisoformat(data["revoked_at"]) if data.get("revoked_at") else None,
            revocation_reason=data.get("revocation_reason"),
            verification_summary=data.get("verification_summary", {})
        )
