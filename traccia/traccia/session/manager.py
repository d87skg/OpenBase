"""
Session Manager
Manages agent execution sessions with OpenBase integration.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import uuid
from enum import Enum


class SessionStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Session:
    """An agent execution session producing OpenBase evidence."""

    def __init__(self, objective: str, agent_id: str = "agent.default"):
        self.session_id = f"sess_{uuid.uuid4().hex[:12]}"
        self.objective = objective
        self.agent_id = agent_id
        self.status = SessionStatus.RUNNING
        self.started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.ended_at: Optional[str] = None
        self._events: List[Dict[str, Any]] = []
        self._evidence_chain: List[Dict[str, Any]] = []

    @property
    def execution_id(self) -> str:
        return f"exec_{self.session_id}"

    def record(self, event_type: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        event = {
            "event_id": f"evt_{uuid.uuid4().hex[:12]}",
            "session_id": self.session_id,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_type": event_type,
            "actor_id": self.agent_id,
            "payload": payload or {},
        }
        self._events.append(event)
        return event

    def complete(self):
        self.status = SessionStatus.COMPLETED
        self.ended_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def fail(self, error: str = ""):
        self.status = SessionStatus.FAILED
        self.ended_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.record("agent_error", {"error": error})

    def cancel(self):
        self.status = SessionStatus.CANCELLED
        self.ended_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_events(self) -> list:
        return self._events

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "objective": self.objective,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "event_count": len(self._events),
        }
