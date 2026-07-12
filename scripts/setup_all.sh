#!/bin/bash

echo "🚀 OpenBase Full Setup - Creating all missing components"

# 创建必要的目录
mkdir -p engines/events
mkdir -p registry/engines
mkdir -p registry/workers
mkdir -p openbase-cli/commands

# 1. Event Bus
cat > engines/events/bus.py << 'PY'
import asyncio
from collections import defaultdict
from typing import Callable, Any, Dict, List

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        self.subscribers[event_type].append(handler)

    async def emit(self, event_type: str, payload: Dict[str, Any]):
        if event_type not in self.subscribers:
            return
        for handler in self.subscribers[event_type]:
            if asyncio.iscoroutinefunction(handler):
                await handler(payload)
            else:
                handler(payload)

event_bus = EventBus()
PY

# 2. Event Types
cat > engines/events/types.py << 'PY'
class EventType:
    EVIDENCE_INGESTED = "evidence.ingested"
    RUNTIME_REGISTERED = "runtime.registered"
    EXECUTION_COMPLETED = "execution.completed"
    TRUST_RECALCULATE = "trust.recalculate"
    TRUST_UPDATED = "trust.updated"
    CERT_ISSUE_REQUESTED = "cert.issue.requested"
    CERT_ISSUED = "cert.issued"
    CERT_REVOKED = "cert.revoked"
    COMPATIBILITY_UPDATED = "compatibility.updated"
    RANKING_UPDATED = "ranking.updated"
PY

# 3. Diff Engine
cat > engines/diff_engine.py << 'PY'
import json
from typing import Dict, List, Any

class DiffEngine:
    def __init__(self, registry_client):
        self.registry = registry_client

    def compute_diff(self, runtime_a: str, runtime_b: str) -> Dict:
        trace_a = self.registry.get_trace(runtime_a)
        trace_b = self.registry.get_trace(runtime_b)

        # Simplified diff calculation
        structural = self._structural_diff(trace_a, trace_b)
        temporal = self._temporal_diff(trace_a, trace_b)
        semantic = self._semantic_diff(trace_a, trace_b)
        evidence_loss = self._evidence_loss_diff(trace_a, trace_b)

        dds = 0.4 * structural + 0.3 * temporal + 0.2 * semantic + 0.1 * evidence_loss

        return {
            "runtime_a": runtime_a,
            "runtime_b": runtime_b,
            "structural_diff": structural,
            "temporal_diff": temporal,
            "semantic_diff": semantic,
            "evidence_loss": evidence_loss,
            "dds_score": dds,
            "classification": self._classify(dds)
        }

    def _structural_diff(self, a, b):
        # Placeholder: compare state graphs
        return 0.12

    def _temporal_diff(self, a, b):
        return 0.21

    def _semantic_diff(self, a, b):
        return 0.09

    def _evidence_loss_diff(self, a, b):
        return 0.03

    def _classify(self, dds):
        if dds < 0.1: return "LOW"
        if dds < 0.3: return "MEDIUM"
        return "HIGH"
PY

# 4. Consensus Engine
cat > engines/consensus_engine.py << 'PY'
from typing import List, Dict

class ConsensusEngine:
    def __init__(self, registry_client):
        self.registry = registry_client

    def reach_consensus(self, runtime_ids: List[str]) -> Dict:
        traces = [self.registry.get_trace(rid) for rid in runtime_ids]
        # Simplified: majority vote on event types
        event_counts = {}
        for trace in traces:
            for event in trace.get("events", []):
                etype = event.get("type")
                event_counts[etype] = event_counts.get(etype, 0) + 1

        consensus_events = [k for k, v in event_counts.items() if v > len(runtime_ids) // 2]
        return {
            "consensus_events": consensus_events,
            "total_events": len(set(event_counts.keys())),
            "confidence": len(consensus_events) / max(1, len(event_counts))
        }
PY

# 5. Update registry/app.py to include event bus and new engines
cat > registry/app.py << 'PY'
import sys
sys.path.insert(0, '.')
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .storage import MemoryStore
from .service import RuntimeService, CertificateService, TrustService
from .api import setup_runtime_routes, setup_certificate_routes, setup_trust_routes, health_router, setup_evidence_routes
from engines.events.bus import event_bus
from engines.events.types import EventType

app = FastAPI(title="OpenBase Registry API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

store = MemoryStore()
runtime_service = RuntimeService(store)
cert_service = CertificateService(store)
trust_service = TrustService(store)

app.include_router(health_router)
app.include_router(setup_runtime_routes(runtime_service))
app.include_router(setup_certificate_routes(cert_service, trust_service))
app.include_router(setup_trust_routes(trust_service, cert_service))
app.include_router(setup_evidence_routes(store, runtime_service))

# Auto-trigger trust update on evidence ingest
async def on_evidence(payload):
    runtime_id = payload.get("runtime_id")
    if runtime_id:
        trust = trust_service.get(runtime_id)
        if trust:
            score = trust_service.compute_score(runtime_id, cert_service.get_by_runtime(runtime_id), evidence_count=len(store.list("evidence", {"runtime_id": runtime_id})))
            trust_service.update(runtime_id, runtime_id, certificate_count=0, verification_status="UPDATED")
            await event_bus.emit(EventType.TRUST_UPDATED, {"runtime_id": runtime_id, "score": score})

event_bus.subscribe(EventType.EVIDENCE_INGESTED, on_evidence)

@app.on_event("startup")
async def startup():
    existing = runtime_service.get_by_name("OpenClaw")
    if not existing:
        runtime_service.register("OpenClaw", "1.0.0", "OpenBase", capabilities=["execution","evidence","replay","verification","determinism","certification"])
PY

echo "✅ All components created successfully."
echo "▶️  Now you can start the system with: python registry/run.py"
