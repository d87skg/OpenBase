import json
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import base64
from .vector_clock import VectorClock

class Evidence:
    def __init__(self, agent_id: str, execution_id: str, event_type: str, payload: Dict[str, Any], 
                 parent_id: Optional[str] = None, agent_metadata: Optional[Dict[str, Any]] = None,
                 node_id: Optional[str] = None, vector_clock: Optional[Dict[str, int]] = None):
        if not agent_id or not execution_id:
            raise ValueError("agent_id and execution_id are required")
        
        self.run_id = str(uuid.uuid4())
        self.execution_id = execution_id
        self.agent_id = agent_id
        self.agent_metadata = agent_metadata or {"status": "unregistered"}
        self.event_type = event_type
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.parent_id = parent_id
        self.payload = payload
        self.spec_version = "0.3.1"
        self._status = "experimental-unstable"
        self.node_id = node_id or "localhost"
        self.vector_clock = vector_clock or {}  # 允许空字典
        self.hash = None
        self.signature = None
        self.public_key = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "spec_version": self.spec_version,
            "status": self._status,
            "execution_id": self.execution_id,
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "agent_metadata": self.agent_metadata,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "parent_id": self.parent_id,
            "payload": self.payload,
            "node_id": self.node_id,
            "vector_clock": self.vector_clock,
        }
        if self.hash: d["hash"] = self.hash
        if self.signature: d["signature"] = self.signature
        if self.public_key: d["public_key"] = self.public_key
        return d

    def sign(self, previous_hash: Optional[str] = None, private_key=None):
        data_str = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        if previous_hash: data_str = previous_hash + data_str
        self.hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        if private_key:
            from .identity import AgentIdentity
            if isinstance(private_key, str):
                private_bytes = base64.b64decode(private_key)
                identity = AgentIdentity.from_private_key_bytes(private_bytes)
            else:
                identity = private_key
            sign_data = (self.hash + self.execution_id).encode()
            self.signature = base64.b64encode(identity.sign(sign_data)).decode('ascii')
            self.public_key = identity.get_public_key_base64()
        return self.hash

class EventBus:
    def __init__(self, node_id: str = "localhost"):
        self.subscribers = []
        self.clock = VectorClock(node_id)
        self.node_id = node_id

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def emit(self, evidence: Evidence):
        # 强制获取新的向量时钟，并赋值给证据
        evidence.vector_clock = self.clock.tick()
        if not evidence.hash:
            evidence.sign()
        for cb in self.subscribers:
            cb(evidence.to_dict())