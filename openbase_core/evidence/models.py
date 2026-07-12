"""
OpenBase Evidence Models
Evidence v2.0 Python Implementation
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import uuid
import json
from datetime import datetime, timezone


@dataclass
class Causal:
    """Causal ordering data for evidence chain."""
    parent_id: Optional[str]
    vector_clock: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parent_id": self.parent_id,
            "vector_clock": self.vector_clock,
        }


@dataclass
class Evidence:
    """OpenBase Evidence v2.0 — Signed snapshot of an OBS Event."""
    evidence_id: str
    event_id: str
    execution_id: str
    agent_id: str
    event_type: str
    timestamp: str
    causal: Causal
    payload: Dict[str, Any]
    hash: str
    signature: str
    public_key: str
    spec_version: str = "2.0"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to Evidence JSON format."""
        return {
            "evidence_id": self.evidence_id,
            "spec_version": self.spec_version,
            "event_id": self.event_id,
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "causal": self.causal.to_dict(),
            "payload": self.payload,
            "hash": self.hash,
            "signature": self.signature,
            "public_key": self.public_key,
        }

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evidence":
        causal_data = data.get("causal", {})
        return cls(
            evidence_id=data["evidence_id"],
            spec_version=data.get("spec_version", "2.0"),
            event_id=data["event_id"],
            execution_id=data["execution_id"],
            agent_id=data["agent_id"],
            event_type=data["event_type"],
            timestamp=data["timestamp"],
            causal=Causal(
                parent_id=causal_data.get("parent_id"),
                vector_clock=causal_data.get("vector_clock", {}),
            ),
            payload=data.get("payload", {}),
            hash=data["hash"],
            signature=data["signature"],
            public_key=data["public_key"],
        )
