"""
OpenBase Registry - Evidence API
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..service import RuntimeService
from ..storage import BaseStore

router = APIRouter(prefix="/evidence", tags=["evidence"])


class EvidencePushRequest(BaseModel):
    runtime_id: str
    execution_id: str
    event_type: str
    payload: dict
    evidence_id: Optional[str] = None
    timestamp: Optional[str] = None


class EvidenceResponse(BaseModel):
    evidence_id: str
    runtime_id: str
    execution_id: str
    event_type: str
    payload: dict
    timestamp: str
    hash: Optional[str] = None


def setup_evidence_routes(store: BaseStore, runtime_service: RuntimeService):
    evidence_collection = "evidence"

    @router.post("/", response_model=EvidenceResponse)
    async def push_evidence(request: Request, evidence_request: EvidencePushRequest):
        runtime = runtime_service.get(evidence_request.runtime_id)
        if not runtime:
            raise HTTPException(status_code=404, detail=f"Runtime {evidence_request.runtime_id} not found")

        evidence_id = evidence_request.evidence_id or f"evid-{uuid.uuid4().hex[:8]}"
        timestamp = evidence_request.timestamp or datetime.now().isoformat()

        evidence_data = {
            "evidence_id": evidence_id,
            "runtime_id": evidence_request.runtime_id,
            "execution_id": evidence_request.execution_id,
            "event_type": evidence_request.event_type,
            "payload": evidence_request.payload,
            "timestamp": timestamp
        }

        store.create(evidence_collection, evidence_data)

        # 自动触发 Reality Ingestion
        try:
            ingestion_engine = request.app.state.ingestion_engine
            ingestion_engine.ingest_evidence(evidence_data)
        except Exception as e:
            print(f"⚠️ Ingestion error: {e}")

        return EvidenceResponse(**evidence_data)

    @router.get("/{evidence_id}", response_model=EvidenceResponse)
    async def get_evidence(evidence_id: str):
        data = store.get(evidence_collection, evidence_id)
        if not data:
            raise HTTPException(status_code=404, detail=f"Evidence {evidence_id} not found")
        return EvidenceResponse(**data)

    @router.get("/execution/{execution_id}", response_model=List[EvidenceResponse])
    async def list_evidence_by_execution(execution_id: str):
        items = store.list(evidence_collection, {"execution_id": execution_id})
        return [EvidenceResponse(**item) for item in items]

    @router.get("/runtime/{runtime_id}", response_model=List[EvidenceResponse])
    async def list_evidence_by_runtime(runtime_id: str):
        items = store.list(evidence_collection, {"runtime_id": runtime_id})
        return [EvidenceResponse(**item) for item in items]

    @router.get("/", response_model=List[EvidenceResponse])
    async def list_all_evidence(limit: int = 100):
        items = store.list(evidence_collection)
        return [EvidenceResponse(**item) for item in items[:limit]]

    return router
