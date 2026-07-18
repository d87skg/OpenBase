"""
Base Emitter — Universal adapter interface for all Agent frameworks.
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime, timezone
from openbase_core.event import Event, Actor, ActorType, Runtime, EventType
from openbase_core.registry import OpenBaseRuntime, RuntimeConfig


class BaseEmitter:
    """Universal emitter that wraps any Agent framework with OpenBase tracing.

    Usage:
        emitter = BaseEmitter("langchain", agent_id="agent.demo")
        emitter.on_start("task description")
        emitter.on_tool_call("search", {"query": "AI"})
        emitter.on_tool_result("search", "results")
        emitter.on_finish("done")
        result = emitter.finish()
    """

    def __init__(self, runtime_name: str, agent_id: str = "agent.default",
                 runtime_version: str = "1.0.0"):
        self.runtime_name = runtime_name
        self.agent_id = agent_id
        config = RuntimeConfig(
            agent_id=agent_id,
            runtime_name=runtime_name,
            runtime_version=runtime_version,
        )
        self.rt = OpenBaseRuntime(config)
        self._last_event_id: Optional[str] = None

    def on_start(self, task: str, **kwargs):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"task": task, **kwargs},
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_tool_call(self, tool_name: str, tool_input: Dict[str, Any], **kwargs):
        event = Event(
            event_type=EventType.TOOL_CALL,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"tool_name": tool_name, "tool_input": tool_input, **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_tool_result(self, tool_name: str, result: Any, **kwargs):
        event = Event(
            event_type=EventType.TOOL_RESULT,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"tool_name": tool_name, "result": str(result)[:500], **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_tool_error(self, tool_name: str, error: str, **kwargs):
        event = Event(
            event_type=EventType.TOOL_ERROR,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"tool_name": tool_name, "error": error, **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_llm_request(self, model: str, messages: list, **kwargs):
        event = Event(
            event_type=EventType.LLM_REQUEST,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"model": model, "messages_count": len(messages), **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_llm_response(self, content: str, **kwargs):
        event = Event(
            event_type=EventType.LLM_RESPONSE,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"content": content[:500], **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_file_read(self, path: str, **kwargs):
        event = Event(
            event_type=EventType.FILE_READ,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"path": path, **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_file_write(self, path: str, **kwargs):
        event = Event(
            event_type=EventType.FILE_WRITE,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"path": path, **kwargs},
            parent_id=self._last_event_id,
        )
        self._last_event_id = event.event_id
        return self.rt.emit(event)

    def on_finish(self, result: Any = None, **kwargs):
        event = Event(
            event_type=EventType.AGENT_FINISHED,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"result": str(result)[:500] if result else None, **kwargs},
            parent_id=self._last_event_id,
        )
        return self.rt.emit(event)

    def on_fail(self, error: str, **kwargs):
        event = Event(
            event_type=EventType.AGENT_FAILED,
            actor=Actor(id=self.agent_id, type=ActorType.AGENT),
            runtime=Runtime(name=self.runtime_name, version="1.0.0"),
            payload={"error": error, **kwargs},
            parent_id=self._last_event_id,
        )
        return self.rt.emit(event)

    def finish(self):
        """Complete execution and return full result with trust + certificate."""
        return self.rt.finish()

    def get_evidence_chain(self):
        return self.rt.get_evidence_chain()
