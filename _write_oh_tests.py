import os

code = '''"""
Tests for OpenHands Adapter
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from adapters.openhands import OpenHandsAdapter, EVENT_MAP
from openbase_core.registry import OpenBaseRuntime, RuntimeConfig
from openbase_core.event import EventType


class TestEventMapping:
    def test_all_mapped_events_are_valid(self):
        for oh_type, obs_type in EVENT_MAP.items():
            event_type = EventType(obs_type)
            assert event_type.value == obs_type

    def test_agent_start_maps_correctly(self):
        assert EVENT_MAP["agent_start"] == "AGENT_STARTED"

    def test_tool_start_maps_correctly(self):
        assert EVENT_MAP["tool_start"] == "TOOL_CALL"

    def test_tool_finish_maps_correctly(self):
        assert EVENT_MAP["tool_finish"] == "TOOL_RESULT"

    def test_known_events_count(self):
        # Ensure we cover the main OpenHands event types
        expected = {
            "agent_start", "agent_finish", "agent_error",
            "tool_start", "tool_finish", "tool_error",
            "llm_request", "llm_response",
            "file_read", "file_write",
            "command_execute",
            "memory_read", "memory_write",
            "approval_request", "approval_granted", "approval_denied",
        }
        assert set(EVENT_MAP.keys()) == expected


class TestOpenHandsAdapter:
    def test_adapter_agent_lifecycle(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.test"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.test")

        adapter.on_agent_start("test task")
        adapter.on_tool_call("read_file", {"path": "/tmp/test"})
        adapter.on_tool_result("read_file", "content")
        adapter.on_agent_finish("done")

        result = rt.finish()
        assert result.status in ("completed", "completed_with_errors")
        assert len(result.events) >= 4

    def test_adapter_produces_evidence(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.evidence"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.evidence")

        adapter.on_agent_start("task")
        adapter.on_agent_finish("ok")

        result = rt.finish()
        chain = rt.get_evidence_chain()
        assert len(chain) >= 2

    def test_adapter_handles_errors(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.error"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.error")

        adapter.on_agent_start("risky task")
        adapter.on_tool_error("broken_tool", "connection failed")
        adapter.on_agent_error("task failed")

        result = rt.finish()
        assert result.status in ("completed", "completed_with_errors")

    def test_adapter_trust_score(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.trust"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.trust")

        for i in range(20):
            adapter.on_agent_start(f"task_{i}")
            adapter.on_tool_call("search", {"query": f"q{i}"})
            adapter.on_tool_result("search", f"result_{i}")
            adapter.on_agent_finish(f"done_{i}")

        result = rt.finish()
        assert result.trust_score is not None
        assert result.trust_score.score > 0.0

    def test_adapter_replay(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.replay"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.replay")

        adapter.on_agent_start("task")
        adapter.on_agent_finish("ok")

        result = rt.finish()
        assert result.replay_result is not None

    def test_adapter_certificate(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.cert"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.cert")

        for i in range(50):
            adapter.on_agent_start(f"task_{i}")
            adapter.on_tool_call("tool", {"i": i})
            adapter.on_tool_result("tool", f"result_{i}")
            adapter.on_agent_finish(f"done_{i}")

        result = rt.finish()
        # With 200+ events, should get at least BRONZE
        assert result.trust_score.score >= 0.30 or result.certificate is None

    def test_adapter_approval_flow(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.approval"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.approval")

        adapter.on_agent_start("dangerous task")
        adapter.on_approval_request("req_001", "delete_files")
        adapter.on_approval_granted("req_001")
        adapter.on_agent_finish("approved and done")

        result = rt.finish()
        assert result.status in ("completed", "completed_with_errors")

    def test_adapter_file_operations(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.oh.files"))
        adapter = OpenHandsAdapter(rt, agent_id="agent.oh.files")

        adapter.on_agent_start("file task")
        adapter.on_file_read("/tmp/data.txt")
        adapter.on_file_write("/tmp/output.txt", "result")
        adapter.on_agent_finish("files processed")

        result = rt.finish()
        assert result.status in ("completed", "completed_with_errors")
'''

path = r'D:\OpenBase\adapters\tests\test_openhands.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_openhands.py written')
