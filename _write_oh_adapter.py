import os

code = '''"""
OpenHands Adapter for OpenBase
Maps OpenHands runtime events to OBS (OpenBase Event Specification).
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field

from openbase_core.event import Event, Actor, ActorType, Runtime, EventType, StateTransition


# OpenHands -> OBS event mapping
EVENT_MAP = {
    "agent_start": "AGENT_STARTED",
    "agent_finish": "AGENT_FINISHED",
    "agent_error": "AGENT_FAILED",
    "tool_start": "TOOL_CALL",
    "tool_finish": "TOOL_RESULT",
    "tool_error": "TOOL_ERROR",
    "llm_request": "LLM_REQUEST",
    "llm_response": "LLM_RESPONSE",
    "file_read": "FILE_READ",
    "file_write": "FILE_WRITE",
    "command_execute": "COMMAND_EXECUTE",
    "memory_read": "MEMORY_READ",
    "memory_write": "MEMORY_WRITE",
    "approval_request": "APPROVAL_REQUEST",
    "approval_granted": "APPROVAL_GRANTED",
    "approval_denied": "APPROVAL_DENIED",
}


@dataclass
class OpenHandsEvent:
    """A raw event from an OpenHands runtime."""
    event_type: str  # OpenHands event name
    agent_id: str
    runtime_version: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    event_id: Optional[str] = None
    parent_id: Optional[str] = None


class OpenHandsAdapter:
    """Adapter that converts OpenHands events to OBS Events and feeds into OpenBase.

    Usage:
        from adapters.openhands import OpenHandsAdapter
        from openbase_core.registry import OpenBaseRuntime

        rt = OpenBaseRuntime(...)
        adapter = OpenHandsAdapter(rt)

        # Simulate OpenHands events
        adapter.on_agent_start("research task")
        adapter.on_tool_call("read_file", {"path": "/tmp/data"})
        adapter.on_tool_result("read_file", "file content")
        adapter.on_agent_finish("done")

        result = rt.finish()
        print(result.trust_score)
    """

    def __init__(self, openbase_runtime, agent_id: str = "agent.openhands.adapter",
                 runtime_version: str = "0.15.0"):
        self.rt = openbase_runtime
        self.agent_id = agent_id
        self.runtime_version = runtime_version
        self._event_count = 0
        self._last_event_id: Optional[str] = None

    def _next_event_id(self) -> str:
        from uuid import uuid4
        self._event_count += 1
        return f"evt_oh_{uuid4().hex[:8]}"

    def _map_event_type(self, oh_type: str) -> EventType:
        """Map OpenHands event type to OBS EventType."""
        obs_type = EVENT_MAP.get(oh_type, "AGENT_STARTED")
        return EventType(obs_type)

    def _create_obs_event(self, oh_type: str, payload: Dict[str, Any]) -> Event:
        """Create an OBS Event from OpenHands event data."""
        event_id = self._next_event_id()
        self._last_event_id = event_id

        return Event(
            event_type=self._map_event_type(oh_type),
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name="openhands", version=self.runtime_version),
            payload=payload,
            event_id=event_id,
            parent_id=self._last_event_id,
        )

    # --- Convenience methods mimicking OpenHands event hooks ---

    def on_agent_start(self, task: str, **kwargs):
        """Handle agent start event."""
        event = self._create_obs_event("agent_start", {"task": task, **kwargs})
        return self.rt.emit(event)

    def on_agent_finish(self, result: Any = None, **kwargs):
        """Handle agent finish event."""
        event = self._create_obs_event("agent_finish", {"result": result, **kwargs})
        return self.rt.emit(event)

    def on_agent_error(self, error: str, **kwargs):
        """Handle agent error event."""
        event = self._create_obs_event("agent_error", {"error": error, **kwargs})
        return self.rt.emit(event)

    def on_tool_call(self, tool_name: str, tool_input: Dict[str, Any], **kwargs):
        """Handle tool start event."""
        event = self._create_obs_event("tool_start", {
            "tool_name": tool_name,
            "tool_input": tool_input,
            **kwargs,
        })
        return self.rt.emit(event)

    def on_tool_result(self, tool_name: str, result: Any, **kwargs):
        """Handle tool finish event."""
        event = self._create_obs_event("tool_finish", {
            "tool_name": tool_name,
            "result": result,
            **kwargs,
        })
        return self.rt.emit(event)

    def on_tool_error(self, tool_name: str, error: str, **kwargs):
        """Handle tool error event."""
        event = self._create_obs_event("tool_error", {
            "tool_name": tool_name,
            "error": error,
            **kwargs,
        })
        return self.rt.emit(event)

    def on_llm_request(self, model: str, messages: list, **kwargs):
        """Handle LLM request event."""
        event = self._create_obs_event("llm_request", {
            "model": model,
            "messages": messages,
            **kwargs,
        })
        return self.rt.emit(event)

    def on_llm_response(self, content: str, **kwargs):
        """Handle LLM response event."""
        event = self._create_obs_event("llm_response", {"content": content, **kwargs})
        return self.rt.emit(event)

    def on_file_read(self, path: str, content: Optional[str] = None, **kwargs):
        """Handle file read event."""
        event = self._create_obs_event("file_read", {"path": path, "content": content, **kwargs})
        return self.rt.emit(event)

    def on_file_write(self, path: str, content: str, **kwargs):
        """Handle file write event."""
        event = self._create_obs_event("file_write", {"path": path, "content": content[:200], **kwargs})
        return self.rt.emit(event)

    def on_command_execute(self, command: str, exit_code: int = 0, output: str = "", **kwargs):
        """Handle command execute event."""
        event = self._create_obs_event("command_execute", {
            "command": command,
            "exit_code": exit_code,
            "output": output[:200],
            **kwargs,
        })
        return self.rt.emit(event)

    def on_approval_request(self, request_id: str, action: str, **kwargs):
        """Handle approval request event."""
        event = self._create_obs_event("approval_request", {
            "request_id": request_id,
            "action": action,
            **kwargs,
        })
        return self.rt.emit(event)

    def on_approval_granted(self, request_id: str, **kwargs):
        """Handle approval granted event."""
        event = self._create_obs_event("approval_granted", {"request_id": request_id, **kwargs})
        return self.rt.emit(event)

    def on_approval_denied(self, request_id: str, reason: str = "", **kwargs):
        """Handle approval denied event."""
        event = self._create_obs_event("approval_denied", {
            "request_id": request_id,
            "reason": reason,
            **kwargs,
        })
        return self.rt.emit(event)
'''

path = r'D:\OpenBase\adapters\openhands\adapter.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('openhands/adapter.py written')
