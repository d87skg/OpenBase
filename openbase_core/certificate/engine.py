"""
OpenBase Certificate Engine
Certificate v1.0 Implementation — issues and verifies trust certificates.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import uuid


@dataclass
class Certificate:
    """OpenBase Certificate v1.0 — Formal trust credential."""
    certificate_id: str
    subject_id: str
    subject_type: str
    level: str  # BRONZE, SILVER, GOLD, PLATINUM
    issuer: str
    issued_at: str
    expires_at: str
    trust_snapshot: Dict[str, Any]
    signature: str
    status: str = "active"  # active, expiring, expired, revoked
    revoked_at: Optional[str] = None
    revocation_reason: Optional[str] = None
    renewal_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "certificate_id": self.certificate_id,
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "level": self.level,
            "issuer": self.issuer,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "trust_snapshot": self.trust_snapshot,
            "signature": self.signature,
            "status": self.status,
            "renewal_count": self.renewal_count,
        }
        if self.revoked_at:
            result["revoked_at"] = self.revoked_at
        if self.revocation_reason:
            result["revocation_reason"] = self.revocation_reason
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def is_expired(self) -> bool:
        """Check if certificate is past its expiry date."""
        try:
            expires = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > expires
        except ValueError:
            return False

    def is_expiring_soon(self, days: int = 30) -> bool:
        """Check if certificate expires within given days."""
        try:
            expires = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
            threshold = datetime.now(timezone.utc) + timedelta(days=days)
            return datetime.now(timezone.utc) < expires <= threshold
        except ValueError:
            return False


class CertificateEngine:
    """Issues, verifies, renews, and revokes Certificates."""

    # Level thresholds (from TrustEngine)
    LEVEL_THRESHOLDS = {
        "PLATINUM": 0.90,
        "GOLD": 0.70,
        "SILVER": 0.50,
        "BRONZE": 0.30,
    }

    # Default validity periods (days)
    VALIDITY_DAYS = {
        "PLATINUM": 180,
        "GOLD": 90,
        "SILVER": 60,
        "BRONZE": 30,
    }

    def __init__(self, issuer: str = "registry.openbase.main", signer=None):
        """Initialize CertificateEngine.

        Args:
            issuer: Identifier for the certificate issuer.
            signer: EvidenceSigner for creating signatures.
        """
        self.issuer = issuer
        self._signer = signer
        self._certificates: Dict[str, Certificate] = {}
        self._revoked: Dict[str, Certificate] = {}

    def issue(
        self,
        subject_id: str,
        subject_type: str,
        trust_score,
        level: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Certificate]:
        """Issue a new certificate if trust score meets level threshold.

        Args:
            subject_id: Subject identifier.
            subject_type: 'runtime', 'agent', 'model', or 'tool'.
            trust_score: TrustScore object from TrustEngine.
            level: Desired level. Auto-detected from score if None.
            metadata: Additional metadata.

        Returns:
            Certificate if issued, None if score insufficient.
        """
        # Determine level
        if level is None:
            level = self._score_to_level(trust_score.score)

        threshold = self.LEVEL_THRESHOLDS.get(level, 0.30)
        if trust_score.score < threshold:
            return None  # Score too low

        now = datetime.now(timezone.utc)
        validity = self.VALIDITY_DAYS.get(level, 90)
        expires = now + timedelta(days=validity)

        cert_id = f"cert_{uuid.uuid4().hex[:12]}"

        # Check for previous certificates of this subject for renewal count
        renewal_count = 0
        for existing in self._certificates.values():
            if existing.subject_id == subject_id and existing.status in ("active", "expiring", "expired"):
                renewal_count += 1

        # Create signature
        signature = self._create_signature(cert_id, subject_id, level)

        cert = Certificate(
            certificate_id=cert_id,
            subject_id=subject_id,
            subject_type=subject_type,
            level=level,
            issuer=self.issuer,
            issued_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            expires_at=expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_snapshot={
                "score": trust_score.score,
                "evidence_count": trust_score.evidence_count,
                "dimensions": trust_score.dimensions.to_dict() if hasattr(trust_score.dimensions, 'to_dict') else {},
            },
            signature=signature,
            status="active",
            renewal_count=renewal_count,
            metadata=metadata or {},
        )

        self._certificates[cert_id] = cert
        return cert

    def _score_to_level(self, score: float) -> str:
        """Map a score to the highest eligible certificate level."""
        if score >= self.LEVEL_THRESHOLDS["PLATINUM"]:
            return "PLATINUM"
        elif score >= self.LEVEL_THRESHOLDS["GOLD"]:
            return "GOLD"
        elif score >= self.LEVEL_THRESHOLDS["SILVER"]:
            return "SILVER"
        elif score >= self.LEVEL_THRESHOLDS["BRONZE"]:
            return "BRONZE"
        else:
            return "BRONZE"  # Minimum

    def _create_signature(self, cert_id: str, subject_id: str, level: str) -> str:
        """Create a certificate signature."""
        if self._signer:
            import hashlib
            message = f"{cert_id}:{subject_id}:{level}:{self.issuer}".encode('ascii')
            h = hashlib.sha256(message).hexdigest()
            return f"sha256:{h}"
        else:
            import hashlib
            message = f"{cert_id}:{subject_id}:{level}:{self.issuer}".encode('ascii')
            h = hashlib.sha256(message).hexdigest()
            return f"sha256:{h}"

    def verify(self, certificate: Certificate) -> bool:
        """Verify a certificate is valid (not expired, not revoked, signature matches)."""
        # Check revocation
        if certificate.status == "revoked":
            return False

        # Check expiry
        if certificate.is_expired():
            return False

        # Verify signature
        expected_sig = self._create_signature(
            certificate.certificate_id,
            certificate.subject_id,
            certificate.level,
        )
        if certificate.signature != expected_sig:
            return False

        return True

    def revoke(self, certificate_id: str, reason: str) -> Optional[Certificate]:
        """Revoke a certificate."""
        cert = self._certificates.get(certificate_id)
        if cert is None:
            return None

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        cert.status = "revoked"
        cert.revoked_at = now
        cert.revocation_reason = reason

        self._revoked[certificate_id] = cert
        return cert

    def renew(self, certificate_id: str, trust_score) -> Optional[Certificate]:
        """Renew a certificate if trust score still meets threshold."""
        cert = self._certificates.get(certificate_id)
        if cert is None:
            return None

        if cert.status == "revoked":
            return None

        threshold = self.LEVEL_THRESHOLDS.get(cert.level, 0.30)
        if trust_score.score < threshold:
            return None

        # Issue a new certificate (increment renewal count)
        new_cert = self.issue(
            subject_id=cert.subject_id,
            subject_type=cert.subject_type,
            trust_score=trust_score,
            level=cert.level,
            metadata={"renewed_from": certificate_id},
        )
        if new_cert:
            new_cert.renewal_count = cert.renewal_count + 1

        return new_cert

    def get_certificate(self, certificate_id: str) -> Optional[Certificate]:
        """Get a certificate by ID."""
        return self._certificates.get(certificate_id)

    def get_active_certificates(self, subject_id: str) -> List[Certificate]:
        """Get all active certificates for a subject."""
        return [
            c for c in self._certificates.values()
            if c.subject_id == subject_id and c.status == "active" and not c.is_expired()
        ]

    def list_all(self) -> List[Certificate]:
        """List all certificates."""
        return list(self._certificates.values())

    def update_statuses(self):
        """Update certificate statuses based on current time."""
        for cert in self._certificates.values():
            if cert.status == "revoked":
                continue
            if cert.is_expired():
                cert.status = "expired"
            elif cert.is_expiring_soon(days=30):
                cert.status = "expiring"
