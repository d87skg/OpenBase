"""
Execution Protocol (EP) - v0.1
Agent execution as a network event
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


@dataclass
class ExecutionRequest:
    """执行请求 - 协议层消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent: str = ""
    input: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    preferred_runtime: Optional[str] = None
    trust_requirements: Dict[str, float] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent": self.agent,
            "input": self.input,
            "constraints": self.constraints,
            "preferred_runtime": self.preferred_runtime,
            "trust_requirements": self.trust_requirements,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionRequest":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            agent=data.get("agent", ""),
            input=data.get("input", {}),
            constraints=data.get("constraints", {}),
            preferred_runtime=data.get("preferred_runtime"),
            trust_requirements=data.get("trust_requirements", {}),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )


@dataclass
class ExecutionResult:
    """执行结果 - 协议层消息"""
    id: str
    request_id: str
    runtime_id: str
    status: str  # SUCCESS | FAILED | PARTIAL
    output: Dict[str, Any] = field(default_factory=dict)
    evidence_ids: List[str] = field(default_factory=list)
    trust_delta: float = 0.0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "request_id": self.request_id,
            "runtime_id": self.runtime_id,
            "status": self.status,
            "output": self.output,
            "evidence_ids": self.evidence_ids,
            "trust_delta": self.trust_delta,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }