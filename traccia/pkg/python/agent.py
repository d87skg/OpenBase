from .events import EventBus, Evidence
from typing import Dict, Any, Optional
import uuid
import base64

class BaseAgent:
    def __init__(self, agent_id: str, event_bus: EventBus, 
                 private_key: Optional[str] = None,
                 agent_metadata: Optional[Dict[str, Any]] = None,
                 execution_id: Optional[str] = None):
        if not agent_id: raise ValueError("agent_id required")
        self.agent_id = agent_id
        self.agent_metadata = agent_metadata or {}
        self.event_bus = event_bus
        self.private_key = private_key
        self.execution_id = execution_id if execution_id else str(uuid.uuid4())
        self._previous_hash = None

    def _emit(self, event_type: str, payload: Dict[str, Any], parent_id: Optional[str] = None):
        ev = Evidence(
            agent_id=self.agent_id,
            execution_id=self.execution_id,
            event_type=event_type,
            payload=payload,
            parent_id=parent_id,
            agent_metadata=self.agent_metadata,
            node_id=self.event_bus.node_id
        )
        ev.sign(previous_hash=self._previous_hash, private_key=self.private_key)
        self._previous_hash = ev.hash
        self.event_bus.emit(ev)
        return ev.run_id

    def run(self, input_text: str): raise NotImplementedError