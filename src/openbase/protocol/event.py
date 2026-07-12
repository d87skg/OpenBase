"""
Event Backbone (EB) - v0.1
Append-only event log for agent execution network
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


@dataclass
class Event:
    """网络事件"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""  # EXEC_START, EXEC_END, TOOL_CALL, STATE_CHANGE, TRUST_UPDATE, REGISTRY_SYNC
    node_id: str = "local"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    prev_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "node_id": self.node_id,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
        }


@dataclass
class EventStream:
    """事件流 - 不可变日志"""
    events: List[Event] = field(default_factory=list)
    last_hash: Optional[str] = None

    def append(self, event: Event) -> None:
        """追加事件，自动计算哈希链"""
        event.prev_hash = self.last_hash
        self.events.append(event)
        self.last_hash = hash(str(event.to_dict()))

    def get_all(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.events]