"""
OpenBase Registry - Trust API
"""

from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..service import TrustService
from ..service.certificate_service import CertificateService
from ..models import TrustRecord

router = APIRouter(prefix="/trust", tags=["trust"])


class TrustResponse(BaseModel):
    runtime_id: str
    runtime_name: str
    trust_score: float
    certificate_count: int
    revoked_count: int
    replay_success_rate: float
    verification_status: str
    last_updated: str


class TrustRankingResponse(BaseModel):
    runtime_id: str
    runtime_name: str
    trust_score: float


def setup_trust_routes(trust_service: TrustService, cert_service: CertificateService):
    # 注意：/ranking 必须在 /{runtime_id} 之前，否则会被捕获为 runtime_id="ranking"
    @router.get("/ranking", response_model=List[TrustRankingResponse])
    async def get_ranking(limit: int = 10):
        records = trust_service.get_ranking(limit)
        return [TrustRankingResponse(
            runtime_id=r.runtime_id,
            runtime_name=r.runtime_name,
            trust_score=r.trust_score
        ) for r in records]

    @router.get("/{runtime_id}", response_model=TrustResponse)
    async def get_trust(runtime_id: str):
        record = trust_service.get(runtime_id)
        if not record:
            raise HTTPException(status_code=404, detail=f"Trust record for {runtime_id} not found")
        return TrustResponse(**record.to_dict())

    @router.get("/{runtime_id}/refresh", response_model=TrustResponse)
    async def refresh_trust(runtime_id: str):
        certs = cert_service.get_by_runtime(runtime_id)
        active_certs = [c for c in certs if c.status.value == "ACTIVE"]
        trust_score = trust_service.compute_score(runtime_id, active_certs, evidence_count=0)

        record = trust_service.update(
            runtime_id=runtime_id,
            runtime_name=f"runtime-{runtime_id[:8]}",
            certificate_count=len(active_certs),
            revoked_count=len([c for c in certs if c.status.value == "REVOKED"]),
            verification_status="PASS" if trust_score > 0.7 else "REVIEW"
        )
        return TrustResponse(**record.to_dict())

    @router.get("/", response_model=List[TrustResponse])
    async def list_trust():
        records = trust_service.list_all()
        return [TrustResponse(**r.to_dict()) for r in records]

    return router
