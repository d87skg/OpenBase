"""
OpenBase Registry - Evidence Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Evidence:
    evidence_id: str
    execution_id: str
    runtime_id: str
    event_type: str
    payload: Dict[str, Any]
    hash: str
    timestamp: datetime = field(default_factory=datetime.now)
    signature: Optional[str] = None
    public_key: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "execution_id": self.execution_id,
            "runtime_id": self.runtime_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "hash": self.hash,
            "timestamp": self.timestamp.isoformat(),
            "signature": self.signature,
            "public_key": self.public_key
        }

    @staticmethod
    def from_dict(data: dict) -> "Evidence":
        return Evidence(
            evidence_id=data["evidence_id"],
            execution_id=data["execution_id"],
            runtime_id=data["runtime_id"],
            event_type=data["event_type"],
            payload=data["payload"],
            hash=data["hash"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.now(),
            signature=data.get("signature"),
            public_key=data.get("public_key")
        )
