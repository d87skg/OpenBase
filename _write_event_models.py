import os

code = '''"""
OpenBase Event Models
OBS v1.0 Python Implementation
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from enum import Enum
import uuid
import json


class ActorType(str, Enum):
    AGENT = "agent"
    TOOL = "tool"
    HUMAN = "human"
    SYSTEM = "system"


class EventType(str, Enum):
    AGENT_CREATED = "AGENT_CREATED"
    AGENT_STARTED = "AGENT_STARTED"
    AGENT_PAUSED = "AGENT_PAUSED"
    AGENT_RESUMED = "AGENT_RESUMED"
    AGENT_FINISHED = "AGENT_FINISHED"
    AGENT_FAILED = "AGENT_FAILED"
    LLM_REQUEST = "LLM_REQUEST"
    LLM_RESPONSE = "LLM_RESPONSE"
    LLM_STREAM_START = "LLM_STREAM_START"
    LLM_STREAM_END = "LLM_STREAM_END"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    TOOL_ERROR = "TOOL_ERROR"
    MEMORY_READ = "MEMORY_READ"
    MEMORY_WRITE = "MEMORY_WRITE"
    MEMORY_DELETE = "MEMORY_DELETE"
    COMMAND_EXECUTE = "COMMAND_EXECUTE"
    FILE_READ = "FILE_READ"
    FILE_WRITE = "FILE_WRITE"
    CODE_EXECUTE = "CODE_EXECUTE"
    APPROVAL_REQUEST = "APPROVAL_REQUEST"
    APPROVAL_GRANTED = "APPROVAL_GRANTED"
    APPROVAL_DENIED = "APPROVAL_DENIED"


@dataclass
class Actor:
    """Entity that produces an event."""
    id: str
    type: ActorType

    def to_dict(self) -> Dict[str, str]:
        return {"id": self.id, "type": self.type.value}


@dataclass
class Runtime:
    """Execution environment metadata."""
    name: str
    version: str

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "version": self.version}


@dataclass
class StateTransition:
    """Before/after state snapshot."""
    before: Optional[str] = None
    after: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {"before": self.before, "after": self.after}


@dataclass
class Event:
    """OpenBase Event Specification (OBS) v1.0 Event."""
    event_type: EventType
    actor: Actor
    runtime: Runtime
    payload: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    version: str = "1.0"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    parent_id: Optional[str] = None
    state: Optional[StateTransition] = None
    vector_clock: Optional[Dict[str, int]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to OBS JSON format."""
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "version": self.version,
            "actor": self.actor.to_dict(),
            "runtime": self.runtime.to_dict(),
            "timestamp": self.timestamp,
            "payload": self.payload,
        }
        if self.parent_id:
            result["parent_id"] = self.parent_id
        if self.state:
            result["state"] = self.state.to_dict()
        if self.vector_clock:
            result["vector_clock"] = self.vector_clock
        return result

    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Deserialize from OBS JSON dict."""
        actor = Actor(
            id=data["actor"]["id"],
            type=ActorType(data["actor"]["type"])
        )
        runtime_data = data.get("runtime", {})
        runtime = Runtime(
            name=runtime_data.get("name", "unknown"),
            version=runtime_data.get("version", "0.0.0")
        )
        state = None
        if "state" in data and data["state"]:
            state = StateTransition(
                before=data["state"].get("before"),
                after=data["state"].get("after")
            )
        return cls(
            event_id=data["event_id"],
            event_type=EventType(data["event_type"]),
            version=data.get("version", "1.0"),
            actor=actor,
            runtime=runtime,
            timestamp=data["timestamp"],
            parent_id=data.get("parent_id"),
            state=state,
            vector_clock=data.get("vector_clock"),
            payload=data.get("payload", {}),
        )
'''

path = r'D:\OpenBase\openbase-core\event\models.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('models.py written')
