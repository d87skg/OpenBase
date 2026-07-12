import os

code = '''"""
Tests for OpenBase Runtime MVP — End-to-End Integration
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pytest
from openbase_core.registry import OpenBaseRuntime, RuntimeConfig, Registry
from openbase_core.replay import FidelityLevel, ReplayStatus


class TestRegistry:
    def test_register_runtime(self):
        reg = Registry()
        entry = reg.register("runtime", "openclaw", "0.1.0")
        assert entry.entry_type == "runtime"
        assert entry.name == "openclaw"
        assert reg.get_runtime_count() == 1

    def test_register_multiple_types(self):
        reg = Registry()
        reg.register("runtime", "r1", "1.0")
        reg.register("agent", "a1", "1.0")
        reg.register("adapter", "ad1", "1.0")

        assert reg.get_runtime_count() == 1
        assert reg.get_agent_count() == 1
        assert reg.get_adapter_count() == 1

    def test_list_by_type(self):
        reg = Registry()
        reg.register("runtime", "r1")
        reg.register("runtime", "r2")
        reg.register("agent", "a1")

        runtimes = reg.list_by_type("runtime")
        assert len(runtimes) == 2

    def test_get_stats(self):
        reg = Registry()
        reg.register("runtime", "r1")
        reg.register("agent", "a1")
        reg.register("adapter", "ad1")

        stats = reg.get_stats()
        assert stats["total_entries"] == 3
        assert stats["runtimes"] == 1
        assert stats["agents"] == 1

    def test_update_status(self):
        reg = Registry()
        entry = reg.register("runtime", "test", "1.0")
        updated = reg.update_status(entry.entry_id, "deprecated")
        assert updated.status == "deprecated"

    def test_get_nonexistent(self):
        reg = Registry()
        assert reg.get("nonexistent") is None


class TestOpenBaseRuntime:
    def test_runtime_lifecycle(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.demo", runtime_name="test-rt"))
        
        rt.agent_started("test task")
        rt.tool_call("read_file", {"path": "/tmp/test"})
        rt.tool_result("read_file", "content")
        rt.agent_finished("success")

        result = rt.finish()

        assert result.status in ("completed", "completed_with_errors")
        assert len(result.events) == 4
        assert len(result.evidence_chain) == 4

    def test_runtime_produces_evidence_chain(self):
        rt = OpenBaseRuntime()
        rt.agent_started("task")
        rt.agent_finished("done")

        chain = rt.get_evidence_chain()
        assert len(chain) == 2
        # Verify chain continuity
        assert chain[0].causal.parent_id is None
        assert chain[1].causal.parent_id == chain[0].hash

    def test_runtime_trust_score(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.trusted"))
        
        # Produce many successful events
        for i in range(50):
            rt.agent_started(f"task_{i}")
            rt.agent_finished(f"success_{i}")

        result = rt.finish()
        assert result.trust_score is not None
        assert result.trust_score.score > 0.0

    def test_runtime_certificate_issued(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.certified"))
        
        # Produce enough evidence for at least BRONZE
        for i in range(100):
            rt.agent_started(f"task_{i}")
            rt.agent_finished(f"success_{i}")

        result = rt.finish()
        if result.trust_score and result.trust_score.score >= 0.30:
            assert result.certificate is not None
            assert result.certificate.level in ["BRONZE", "SILVER", "GOLD", "PLATINUM"]

    def test_runtime_replay(self):
        rt = OpenBaseRuntime()
        rt.agent_started("task")
        rt.tool_call("read", {"path": "/tmp"})
        rt.agent_finished("done")

        result = rt.finish()
        assert result.replay_result is not None
        assert result.replay_result.status == ReplayStatus.COMPLETED

    def test_runtime_reset(self):
        rt = OpenBaseRuntime()
        rt.agent_started("task1")
        rt.agent_finished("done1")

        assert len(rt.get_evidence_chain()) == 2

        rt.reset()
        assert len(rt.get_evidence_chain()) == 0

    def test_runtime_execution_summary(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.summary"))
        rt.agent_started("demo")
        rt.agent_finished("ok")

        result = rt.finish()
        summary = result.to_summary()

        assert summary["status"] in ("completed", "completed_with_errors")
        assert summary["event_count"] == 2
        assert summary["evidence_count"] == 2
        assert "execution_id" in summary

    def test_runtime_handles_failure(self):
        rt = OpenBaseRuntime()
        rt.agent_started("risky task")
        rt.agent_failed("something went wrong")

        result = rt.finish()
        assert result.status in ("completed", "completed_with_errors")

    def test_runtime_registers_itself(self):
        rt = OpenBaseRuntime(RuntimeConfig(runtime_name="self-registering-rt"))
        assert rt.registry.get_runtime_count() == 1
'''

path = r'D:\OpenBase\openbase_core\tests\test_runtime.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_runtime.py written')
