import logging
logger = logging.getLogger(__name__)
from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from fastapi import WebSocket, WebSocketDisconnect
"""
State API for OpenBase Registry
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from engines.state_transition import transition_engine

router = APIRouter(prefix="/state", tags=["state"])

# WebSocket 客户端列表

ws_clients = []


class EvidenceTransitionRequest(BaseModel):
    type: str  # "evidence"
    runtime_id: str
    execution_id: str
    event_type: str
    payload: Dict[str, Any]


@router.get("/all")
async def get_all_states():
    return transition_engine.get_all_states()


@router.post("/transition")
async def transition(request: EvidenceTransitionRequest):
    if request.type != "evidence":
        raise HTTPException(status_code=400, detail="Only 'evidence' transition supported")
    evidence = transition_engine.process_evidence(
        request.runtime_id,
        request.execution_id,
        request.event_type,
        request.payload
    )
    return evidence


@router.get("/evidence/{runtime_id}")
async def get_evidence(runtime_id: str):
    return transition_engine.get_evidence(runtime_id)


@router.get("/evidence/{runtime_id}/count")
async def get_evidence_count(runtime_id: str):
    evidence = transition_engine.get_evidence(runtime_id)
    return {"runtime_id": runtime_id, "evidence_count": len(evidence)}


@router.get("/trust/{runtime_id}")
async def get_trust(runtime_id: str):
    trust = transition_engine.get_trust(runtime_id)
    if not trust:
        raise HTTPException(status_code=404, detail=f"Trust not found for runtime {runtime_id}")
    return trust


@router.get("/execution/{execution_id}")
async def get_execution(execution_id: str):
    execution = transition_engine.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail=f"Execution {execution_id} not found")
    return execution


@router.get("/history")
async def get_history(key: Optional[str] = None, limit: int = 100):
    return transition_engine.get_history(key, limit)


@router.post("/clear")
async def clear_all():
    transition_engine.clear_all()
    return {"status": "cleared"}


@router.get("/world")
async def get_world_state(request: Request):
    """获取全局世界状态 - 所有 Runtime、Execution、Evidence 的汇总"""
    try:
        ingestion_engine = request.app.state.ingestion_engine
        store = request.app.state.store
        
        # 获取所有 Runtime
        runtimes = store.list("runtimes")
        
        world_state = {
            "timestamp": datetime.now().timestamp(),
            "total_runtimes": len(runtimes),
            "runtimes": [],
            "total_evidence": 0,
            "total_executions": 0,
            "graph": None
        }
        
        for runtime in runtimes:
            runtime_id = runtime["runtime_id"]
            # 获取该 Runtime 的 Evidence
            evidence_items = store.list("evidence", {"runtime_id": runtime_id})
            # 获取 Trust
            trust_record = store.get("trust", runtime_id)
            # 获取 Certificate
            cert_items = store.list("certificates", {"runtime_id": runtime_id})
            latest_cert = max(cert_items, key=lambda c: c.get("issued_at", "")) if cert_items else None
            
            world_state["runtimes"].append({
                "runtime_id": runtime_id,
                "name": runtime.get("name", "unknown"),
                "version": runtime.get("version", "unknown"),
                "status": runtime.get("status", "unknown"),
                "evidence_count": len(evidence_items),
                "trust_score": trust_record.get("trust_score", 0.5) if trust_record else 0.5,
                "certificate": latest_cert.get("level") if latest_cert else None,
                "certificate_status": latest_cert.get("status") if latest_cert else None
            })
            world_state["total_evidence"] += len(evidence_items)
        
        # 获取 Graph 状态
        try:
            graph = ingestion_engine.get_graph()
            world_state["graph"] = {
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges)
            }
        except:
            world_state["graph"] = {"node_count": 0, "edge_count": 0}
        
        return world_state
    except Exception as e:
        logger.error(f"Error getting world state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/replay")
async def replay_execution(request: Request, execution_id: str):
    """重放某个 Execution 的完整状态变化历史"""
    try:
        ingestion_engine = request.app.state.ingestion_engine
        store = request.app.state.store
        
        # 获取该 execution 的所有 Evidence
        evidence_items = store.list("evidence", {"execution_id": execution_id})
        
        if not evidence_items:
            return {
                "execution_id": execution_id,
                "status": "NOT_FOUND",
                "events": []
            }
        
        # 按时间排序
        evidence_items.sort(key=lambda e: e.get("timestamp", ""))
        
        # 构建重放序列
        replay_events = []
        for ev in evidence_items:
            replay_events.append({
                "timestamp": ev.get("timestamp"),
                "event_type": ev.get("event_type"),
                "evidence_id": ev.get("evidence_id"),
                "payload": ev.get("payload", {}),
                "semantic_id": ev.get("semantic_id"),
                "verified": ev.get("verified", False)
            })
        
        # 获取相关的 Trust 变化
        trust_history = []
        runtime_id = evidence_items[0].get("runtime_id") if evidence_items else None
        if runtime_id:
            trust_record = store.get("trust", runtime_id)
            if trust_record:
                trust_history = trust_record.get("history", [])
        
        return {
            "execution_id": execution_id,
            "runtime_id": runtime_id,
            "total_events": len(replay_events),
            "events": replay_events,
            "trust_history": trust_history,
            "status": "COMPLETED"
        }
    except Exception as e:
        logger.error(f"Error replaying execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/stream")
async def state_stream(websocket: WebSocket):
    """WebSocket 实时状态流"""
    await websocket.accept()
    try:
        # 添加客户端到广播列表
        global ws_clients
        ws_clients.append(websocket)
        
        # 发送初始状态
        await websocket.send_json({
            "type": "init",
            "message": "Connected to OpenBase State Stream",
            "timestamp": datetime.now().timestamp()
        })
        
        # 保持连接并监听状态变化
        while True:
            # 接收客户端消息（用于心跳）
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().timestamp()
                })
    except Exception as e:
        logger.info(f"WebSocket disconnected: {e}")
    finally:
        if websocket in ws_clients:
            ws_clients.remove(websocket)
