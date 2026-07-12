"""
OpenBase Registry - Certificate Service
"""

from typing import Optional, List
from datetime import datetime, timedelta
import uuid

from ..models import Certificate, CertificateStatus, CertificateLevel
from ..storage import BaseStore


class CertificateService:
    def __init__(self, store: BaseStore):
        self.store = store
        self._collection = "certificates"

    def issue(self, runtime_id: str, runtime_name: str,
              level: CertificateLevel = CertificateLevel.SILVER,
              trust_score: float = 0.0,
              verification_summary: dict = None) -> Certificate:
        cert_id = f"CERT-{uuid.uuid4().hex[:8]}"
        certificate = Certificate(
            cert_id=cert_id,
            runtime_id=runtime_id,
            runtime_name=runtime_name,
            level=level,
            trust_score=trust_score,
            verification_summary=verification_summary or {}
        )
        self.store.create(self._collection, certificate.to_dict())
        return certificate

    def get(self, cert_id: str) -> Optional[Certificate]:
        data = self.store.get(self._collection, cert_id)
        if data:
            return Certificate.from_dict(data)
        return None

    def get_by_runtime(self, runtime_id: str) -> List[Certificate]:
        items = self.store.list(self._collection, {"runtime_id": runtime_id})
        return [Certificate.from_dict(item) for item in items]

    def get_latest_by_runtime(self, runtime_id: str) -> Optional[Certificate]:
        certs = self.get_by_runtime(runtime_id)
        if not certs:
            return None
        certs.sort(key=lambda c: c.issued_at, reverse=True)
        return certs[0]

    def list_active(self) -> List[Certificate]:
        items = self.store.list(self._collection, {"status": "ACTIVE"})
        return [Certificate.from_dict(item) for item in items]

    def revoke(self, cert_id: str, reason: str) -> bool:
        cert = self.get(cert_id)
        if not cert:
            return False
        cert.status = CertificateStatus.REVOKED
        cert.revoked_at = datetime.now()
        cert.revocation_reason = reason
        return self.store.update(self._collection, cert_id, {
            "status": cert.status.value,
            "revoked_at": cert.revoked_at.isoformat(),
            "revocation_reason": reason
        })

    def check_expiry(self) -> List[Certificate]:
        """检查即将过期的证书（30天内）"""
        now = datetime.now()
        threshold = now + timedelta(days=30)
        items = self.store.list(self._collection, {"status": "ACTIVE"})
        result = []
        for item in items:
            cert = Certificate.from_dict(item)
            if cert.expires_at <= threshold:
                result.append(cert)
        return result
