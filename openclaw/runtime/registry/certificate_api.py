"""
OpenBase Registry - Certificate API
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..service import CertificateService
from ..service import TrustService
from ..models import Certificate, CertificateLevel, CertificateStatus

router = APIRouter(prefix="/certificates", tags=["certificates"])


class CertificateIssueRequest(BaseModel):
    runtime_id: str
    runtime_name: str
    level: str = "SILVER"
    trust_score: float = 0.0
    verification_summary: dict = {}


class CertificateResponse(BaseModel):
    cert_id: str
    runtime_id: str
    runtime_name: str
    level: str
    status: str
    trust_score: float
    issued_at: str
    expires_at: str
    revoked_at: Optional[str]
    revocation_reason: Optional[str]


def setup_certificate_routes(cert_service: CertificateService, trust_service: TrustService):
    @router.post("/issue", response_model=CertificateResponse)
    async def issue_certificate(request: CertificateIssueRequest):
        try:
            level = CertificateLevel(request.level.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid level: {request.level}")

        cert = cert_service.issue(
            runtime_id=request.runtime_id,
            runtime_name=request.runtime_name,
            level=level,
            trust_score=request.trust_score,
            verification_summary=request.verification_summary
        )

        # 自动更新信任记录
        try:
            # 获取该 runtime 的所有活跃证书
            existing_certs = cert_service.get_by_runtime(request.runtime_id)
            active_certs = [c for c in existing_certs if c.status.value == "ACTIVE"]
            trust_score = trust_service.compute_score(request.runtime_id, active_certs, evidence_count=0)
            trust_service.update(
                runtime_id=request.runtime_id,
                runtime_name=request.runtime_name,
                certificate_count=len(active_certs),
                revoked_count=len([c for c in existing_certs if c.status.value == "REVOKED"]),
                verification_status="PASS" if trust_score > 0.7 else "REVIEW"
            )
        except Exception:
            # 信任记录更新失败不影响证书颁发
            pass

        return CertificateResponse(**cert.to_dict())

    @router.get("/{cert_id}", response_model=CertificateResponse)
    async def get_certificate(cert_id: str):
        cert = cert_service.get(cert_id)
        if not cert:
            raise HTTPException(status_code=404, detail=f"Certificate {cert_id} not found")
        return CertificateResponse(**cert.to_dict())

    @router.get("/runtime/{runtime_id}", response_model=List[CertificateResponse])
    async def get_certificates_by_runtime(runtime_id: str):
        certs = cert_service.get_by_runtime(runtime_id)
        return [CertificateResponse(**c.to_dict()) for c in certs]

    @router.get("/runtime/{runtime_id}/latest", response_model=Optional[CertificateResponse])
    async def get_latest_certificate(runtime_id: str):
        cert = cert_service.get_latest_by_runtime(runtime_id)
        if not cert:
            return None
        return CertificateResponse(**cert.to_dict())

    @router.post("/{cert_id}/revoke")
    async def revoke_certificate(cert_id: str, reason: str = "Revoked by admin"):
        success = cert_service.revoke(cert_id, reason)
        if not success:
            raise HTTPException(status_code=404, detail=f"Certificate {cert_id} not found")
        return {"message": f"Certificate {cert_id} revoked", "reason": reason}

    @router.get("/active", response_model=List[CertificateResponse])
    async def list_active_certificates():
        certs = cert_service.list_active()
        return [CertificateResponse(**c.to_dict()) for c in certs]

    return router
