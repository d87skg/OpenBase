import os

code = '''"""
Tests for OpenBase Event Engine
"""

import json
import pytest
from openbase_core.event import (
    Event, Actor, ActorType, Runtime, EventType, StateTransition,
    EventFactory, EventValidator, EventSerializer
)


class TestActor:
    def test_create_actor(self):
        actor = Actor(id="agent.test.bot", type=ActorType.AGENT)
        assert actor.id == "agent.test.bot"
        assert actor.type == ActorType.AGENT

    def test_actor_to_dict(self):
        actor = Actor(id="agent.test.bot", type=ActorType.AGENT)
        d = actor.to_dict()
        assert d == {"id": "agent.test.bot", "type": "agent"}

    def test_all_actor_types(self):
        for at in ActorType:
            actor = Actor(id=f"{at.value}.test.entity", type=at)
            assert actor.type == at


class TestEventCreation:
    def test_create_minimal_event(self):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
        )
        assert event.event_id.startswith("evt_")
        assert event.version == "1.0"
        assert event.event_type == EventType.AGENT_STARTED

    def test_event_to_dict(self):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
            payload={"task": "test"},
            state=StateTransition(before="created", after="running"),
        )
        d = event.to_dict()
        assert d["event_type"] == "AGENT_STARTED"
        assert d["actor"]["id"] == "agent.test"
        assert d["runtime"]["name"] == "openclaw"
        assert d["payload"]["task"] == "test"
        assert d["state"]["before"] == "created"
        assert d["state"]["after"] == "running"

    def test_event_to_json(self):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
        )
        json_str = event.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["event_type"] == "AGENT_STARTED"

    def test_event_from_dict_roundtrip(self):
        original = Event(
            event_type=EventType.TOOL_CALL,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
            payload={"tool": "read_file"},
            parent_id="evt_parent",
            state=StateTransition(before="idle", after="calling"),
            vector_clock={"agent.test": 3},
        )
        d = original.to_dict()
        restored = Event.from_dict(d)
        assert restored.event_id == original.event_id
        assert restored.event_type == original.event_type
        assert restored.actor.id == original.actor.id
        assert restored.parent_id == original.parent_id
        assert restored.vector_clock == original.vector_clock

    def test_event_with_parent_id(self):
        event = Event(
            event_type=EventType.TOOL_CALL,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
            parent_id="evt_parent_123",
        )
        assert "parent_id" in event.to_dict()

    def test_event_without_parent_id(self):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
        )
        assert "parent_id" not in event.to_dict()

    def test_event_unique_ids(self):
        events = [
            Event(
                event_type=EventType.AGENT_STARTED,
                actor=Actor(id="agent.test", type=ActorType.AGENT),
                runtime=Runtime(name="openclaw", version="0.1.0"),
            )
            for _ in range(10)
        ]
        ids = [e.event_id for e in events]
        assert len(ids) == len(set(ids))


class TestEventFactory:
    def test_factory_agent_started(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test task")
        assert event.event_type == EventType.AGENT_STARTED
        assert event.payload["task"] == "test task"
        assert event.actor.id == "agent.demo"

    def test_factory_tool_call(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        event = factory.tool_call("read_file", {"path": "/test.txt"}, parent_id="evt_parent")
        assert event.event_type == EventType.TOOL_CALL
        assert event.payload["tool_name"] == "read_file"
        assert event.parent_id == "evt_parent"

    def test_factory_chain(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        e1 = factory.agent_started("task")
        e2 = factory.llm_request("claude", [], parent_id=e1.event_id)
        e3 = factory.llm_response("result", parent_id=e2.event_id)
        e4 = factory.agent_finished("done", parent_id=e3.event_id)
        assert e1.parent_id is None
        assert e2.parent_id == e1.event_id
        assert e3.parent_id == e2.event_id
        assert e4.parent_id == e3.event_id

    def test_factory_tool_error(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        event = factory.tool_error("broken_tool", "connection refused")
        assert event.event_type == EventType.TOOL_ERROR
        assert event.payload["error"] == "connection refused"


class TestEventValidator:
    def test_valid_event_passes(self):
        factory = EventFactory("agent.openclaw.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test")
        validator = EventValidator()
        assert validator.is_valid(event)

    def test_valid_tool_call_passes(self):
        factory = EventFactory("agent.openclaw.demo", "openclaw", "0.1.0")
        event = factory.tool_call("read", {"path": "/tmp"})
        validator = EventValidator()
        assert validator.is_valid(event)

    def test_invalid_actor_type_fails(self):
        event = Event(
            event_type=EventType.AGENT_STARTED,
            actor=Actor(id="agent.test", type=ActorType.AGENT),
            runtime=Runtime(name="openclaw", version="0.1.0"),
        )
        d = event.to_dict()
        d["actor"]["type"] = "invalid_type"
        validator = EventValidator()
        assert not validator.is_valid_dict(d)

    def test_missing_required_field_fails(self):
        factory = EventFactory("agent.openclaw.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test")
        d = event.to_dict()
        del d["event_id"]
        validator = EventValidator()
        assert not validator.is_valid_dict(d)


class TestEventSerializer:
    def test_to_json_and_back(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        original = factory.agent_started("test")
        json_str = EventSerializer.to_json(original)
        restored = EventSerializer.from_json(json_str)
        assert restored.event_id == original.event_id
        assert restored.event_type == original.event_type

    def test_canonical_json(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test")
        canonical = EventSerializer.to_canonical(event)
        assert isinstance(canonical, bytes)
        assert canonical[0] == ord('{')
        assert canonical[-1] == ord('}')

    def test_serialize_chain(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        events = [
            factory.agent_started("task"),
            factory.tool_call("read", {}),
            factory.agent_finished("done"),
        ]
        json_str = EventSerializer.serialize_chain(events)
        restored = EventSerializer.deserialize_chain(json_str)
        assert len(restored) == 3
        assert restored[0].event_id == events[0].event_id

    def test_canonical_deterministic(self):
        factory = EventFactory("agent.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test")
        c1 = EventSerializer.to_canonical(event)
        c2 = EventSerializer.to_canonical(event)
        assert c1 == c2


class TestEventTypeEnum:
    def test_all_event_types_present(self):
        assert len(EventType) == 22

    def test_event_type_values(self):
        assert EventType.AGENT_STARTED.value == "AGENT_STARTED"
        assert EventType.TOOL_CALL.value == "TOOL_CALL"
        assert EventType.LLM_REQUEST.value == "LLM_REQUEST"
        assert EventType.APPROVAL_REQUEST.value == "APPROVAL_REQUEST"
'''

path = r'D:\OpenBase\openbase-core\tests\event\test_models.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_models.py written')
