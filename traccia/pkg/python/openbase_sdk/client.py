#!/usr/bin/env python3
"""
OpenBase SDK - Lightweight client for emitting OpenBase Evidence
Zero dependencies, can be embedded in any Python project.
"""

import json
import uuid
import hashlib
import base64
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

class Evidence:
    def __init__(self, actor: str, event_type: str, action: Dict, 
                 execution_id: Optional[str] = None,
                 parent_id: Optional[str] = None,
                 metadata: Optional[Dict] = None,
                 private_key: Optional[str] = None):
        self.actor = actor
        self.event_type = event_type
        self.action = action
        self.execution_id = execution_id or str(uuid.uuid4())
        self.parent_id = parent_id
        self.metadata = metadata or {}
        self.private_key = private_key
        self.event_id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.vector_clock = None  # set by external system if needed
        self.hash = None
        self.signature = None

    def to_dict(self) -> Dict:
        d = {
            "spec": "openbase.evidence.v1",
            "event_id": self.event_id,
            "execution_id": self.execution_id,
            "actor": self.actor,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "causal": {
                "parent_id": self.parent_id,
                "vector_clock": self.vector_clock or {}
            },
            "action": self.action,
            "proof": {
                "hash": self.hash,
                "signature": self.signature,
                "merkle_root": None
            }
        }
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    def sign(self, private_key: Optional[str] = None):
        """Sign the evidence using Ed25519 private key (base64)"""
        key = private_key or self.private_key
        if not key:
            return
        # In real implementation, use cryptography library
        # For now, just placeholder
        import base64
        from cryptography.hazmat.primitives.asymmetric import ed25519
        private_bytes = base64.b64decode(key)
        sk = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
        # sign the serialized event (without signature field)
        data = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        signature = sk.sign(data.encode())
        self.signature = base64.b64encode(signature).decode('ascii')
        # compute hash
        self.hash = hashlib.sha256(data.encode()).hexdigest()

    def emit(self, endpoint: Optional[str] = None):
        """Emit evidence to stdout or HTTP endpoint"""
        if endpoint:
            # HTTP POST (placeholder)
            pass
        else:
            print(json.dumps(self.to_dict()))

    @staticmethod
    def from_dict(data: Dict) -> "Evidence":
        ev = Evidence(
            actor=data["actor"],
            event_type=data["event_type"],
            action=data["action"],
            execution_id=data.get("execution_id"),
            parent_id=data.get("causal", {}).get("parent_id"),
            metadata=data.get("metadata")
        )
        ev.event_id = data["event_id"]
        ev.timestamp = data["timestamp"]
        ev.vector_clock = data.get("causal", {}).get("vector_clock")
        ev.hash = data.get("proof", {}).get("hash")
        ev.signature = data.get("proof", {}).get("signature")
        return ev


class OpenBaseClient:
    def __init__(self, execution_id: Optional[str] = None,
                 private_key: Optional[str] = None,
                 actor: str = "system"):
        self.execution_id = execution_id or str(uuid.uuid4())
        self.private_key = private_key
        self.actor = actor
        self.events = []

    def record(self, event_type: str, action: Dict, 
               parent_id: Optional[str] = None,
               metadata: Optional[Dict] = None) -> Evidence:
        ev = Evidence(
            actor=self.actor,
            event_type=event_type,
            action=action,
            execution_id=self.execution_id,
            parent_id=parent_id,
            metadata=metadata,
            private_key=self.private_key
        )
        if self.private_key:
            ev.sign()
        self.events.append(ev)
        return ev

    def flush(self, endpoint: Optional[str] = None):
        for ev in self.events:
            ev.emit(endpoint)
        self.events = []