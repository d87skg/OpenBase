"""
EventFactory — convenience methods for creating OBS Events.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from .models import Event, Actor, ActorType, Runtime, EventType, StateTransition


class EventFactory:
    """Factory for creating well-formed OBS Events."""

    def __init__(self, agent_id: str, runtime_name: str, runtime_version: str):
        self.actor = Actor(id=agent_id, type=ActorType.AGENT)
        self.runtime = Runtime(name=runtime_name, version=runtime_version)
        self._counter = 0

    def _next_id(self) -> str:
        from uuid import uuid4
        self._counter += 1
        return f"evt_{uuid4().hex[:12]}"

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def agent_started(self, task: str, parameters: Optional[Dict] = None) -> Event:
        return Event(
            event_type=EventType.AGENT_STARTED,
            actor=self.actor,
            runtime=self.runtime,
            payload={"task": task, "parameters": parameters or {}},
            state=StateTransition(before="created", after="running"),
        )

    def agent_finished(self, result: Any = None, parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.AGENT_FINISHED,
            actor=self.actor,
            runtime=self.runtime,
            payload={"result": result},
            parent_id=parent_id,
            state=StateTransition(before="running", after="completed"),
        )

    def agent_failed(self, error: str, parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.AGENT_FAILED,
            actor=self.actor,
            runtime=self.runtime,
            payload={"error": error},
            parent_id=parent_id,
            state=StateTransition(before="running", after="failed"),
        )

    def llm_request(self, model: str, messages: list, parameters: Optional[Dict] = None,
                    parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.LLM_REQUEST,
            actor=self.actor,
            runtime=self.runtime,
            payload={"model": model, "messages": messages, "parameters": parameters or {}},
            parent_id=parent_id,
        )

    def llm_response(self, content: str, usage: Optional[Dict] = None,
                     parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.LLM_RESPONSE,
            actor=self.actor,
            runtime=self.runtime,
            payload={"content": content, "usage": usage or {}},
            parent_id=parent_id,
        )

    def tool_call(self, tool_name: str, tool_input: Dict,
                  parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.TOOL_CALL,
            actor=self.actor,
            runtime=self.runtime,
            payload={"tool_name": tool_name, "tool_input": tool_input},
            parent_id=parent_id,
            state=StateTransition(before="running", after="tool_executing"),
        )

    def tool_result(self, tool_name: str, result: Any,
                    parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.TOOL_RESULT,
            actor=self.actor,
            runtime=self.runtime,
            payload={"tool_name": tool_name, "result": result},
            parent_id=parent_id,
            state=StateTransition(before="tool_executing", after="running"),
        )

    def tool_error(self, tool_name: str, error: str,
                   parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=EventType.TOOL_ERROR,
            actor=self.actor,
            runtime=self.runtime,
            payload={"tool_name": tool_name, "error": error},
            parent_id=parent_id,
            state=StateTransition(before="tool_executing", after="error"),
        )

    def custom(self, event_type: EventType, payload: Dict,
               parent_id: Optional[str] = None) -> Event:
        return Event(
            event_type=event_type,
            actor=self.actor,
            runtime=self.runtime,
            payload=payload,
            parent_id=parent_id,
        )
