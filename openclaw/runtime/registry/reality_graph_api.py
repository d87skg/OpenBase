"""
Reality Graph API for OpenBase Registry
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

from engines.reality_graph import RealityGraph, RealityNode, RealityEdge

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reality", tags=["reality"])


class QueryRequest(BaseModel):
    claim: str


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    support: List[dict]
    conflict: List[dict]


@router.post("/build/{runtime_id}")
async def build_graph(request: Request, runtime_id: str):
    """构建 Runtime 的 Reality Graph"""
    logger.info(f"Building graph for runtime: {runtime_id}")
    try:
        ingestion_engine = request.app.state.ingestion_engine
        graph = ingestion_engine.build_from_runtime(runtime_id)
        return graph.to_dict()
    except Exception as e:
        logger.error(f"Error building graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def query_claim(request: Request, query_req: QueryRequest):
    """查询某个 claim 的全局真值"""
    logger.info(f"Querying claim: {query_req.claim}")
    try:
        ingestion_engine = request.app.state.ingestion_engine
        graph = ingestion_engine.get_graph()
        result = graph.query(query_req.claim)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conflicts")
async def get_conflicts(request: Request, threshold: float = 0.2):
    """获取所有冲突边"""
    logger.info(f"Getting conflicts with threshold {threshold}")
    try:
        ingestion_engine = request.app.state.ingestion_engine
        graph = ingestion_engine.get_graph()
        conflicts = graph.get_conflicts(threshold)
        return conflicts
    except Exception as e:
        logger.error(f"Error getting conflicts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph")
async def get_full_graph(request: Request):
    """获取完整的 Reality Graph"""
    try:
        ingestion_engine = request.app.state.ingestion_engine
        graph = ingestion_engine.get_graph()
        return graph.to_dict()
    except Exception as e:
        logger.error(f"Error getting graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/evidence")
async def ingest_evidence(request: Request, evidence: dict):
    """手动触发证据 Ingestion"""
    try:
        ingestion_engine = request.app.state.ingestion_engine
        node = ingestion_engine.ingest_evidence(evidence)
        if node:
            return {"status": "ingested", "node_id": node.node_id}
        return {"status": "skipped", "reason": "no evidence provided"}
    except Exception as e:
        logger.error(f"Error ingesting evidence: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/trust")
async def ingest_trust(request: Request, trust_record: dict):
    """手动触发信任 Ingestion"""
    try:
        ingestion_engine = request.app.state.ingestion_engine
        node = ingestion_engine.ingest_trust(trust_record)
        if node:
            return {"status": "ingested", "node_id": node.node_id}
        return {"status": "skipped", "reason": "no trust record provided"}
    except Exception as e:
        logger.error(f"Error ingesting trust: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semantic/normalize")
async def normalize_text(text: dict):
    """归一化文本"""
    from engines.semantic_layer import semantic_layer
    normalized = semantic_layer.normalizer.normalize(text.get("text", ""))
    return {"original": text.get("text", ""), "normalized": normalized}


@router.post("/semantic/compare")
async def compare_semantic(data: dict):
    """比较两个文本的语义"""
    from engines.semantic_layer import semantic_layer
    result = semantic_layer.compare_semantic(data.get("text_a", ""), data.get("text_b", ""))
    return result


@router.get("/semantic/index")
async def get_semantic_index():
    """获取语义索引"""
    from engines.semantic_layer import semantic_layer
    return semantic_layer.to_dict()


@router.post("/semantic/related")
async def find_related(data: dict):
    """查找语义相关的概念"""
    from engines.semantic_layer import semantic_layer
    results = semantic_layer.find_related(data.get("text", ""), data.get("threshold", 0.7))
    return results
