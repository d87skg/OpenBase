import os

code = '''"""
Tests for OpenBase Replay Engine
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pytest
from openbase_core.event import EventFactory
from openbase_core.evidence import EvidenceSigner
from openbase_core.replay import (
    ReplayEngine, FidelityLevel, ReplayStatus, ReplayErrorCode
)


class TestReplayEngine:
    def test_replay_empty_chain_fails(self):
        engine = ReplayEngine()
        result = engine.replay([], "exec_001", FidelityLevel.STRUCTURAL)
        assert result.status == ReplayStatus.FAILED
        assert result.error_code == ReplayErrorCode.E006

    def test_replay_structural_valid_chain(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.tool_call("read", {"path": "/tmp"}), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("done"), "exec_001"))

        result = engine.replay(chain, "exec_001", FidelityLevel.STRUCTURAL)
        assert result.status == ReplayStatus.COMPLETED
        assert result.total_steps == 3

    def test_replay_broken_hash_chain_fails(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.tool_call("read", {}), "exec_001"))

        # Tamper with the first evidence's hash
        tampered_dict = chain[1].to_dict()
        tampered_dict["causal"]["parent_id"] = "deadbeef00000000000000000000000000000000000000000000000000000000"
        from openbase_core.evidence import Evidence
        tampered = Evidence.from_dict(tampered_dict)
        broken_chain = [chain[0], tampered]

        result = engine.replay(broken_chain, "exec_001", FidelityLevel.STRUCTURAL)
        assert result.status == ReplayStatus.FAILED
        assert result.error_code == ReplayErrorCode.E002

    def test_replay_logical_reconstructs_state(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("test task"), "exec_001"))
        chain.append(signer.sign_event(factory.tool_call("read_file", {"path": "/tmp"}), "exec_001"))
        chain.append(signer.sign_event(factory.tool_result("read_file", "file contents"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("success"), "exec_001"))

        result = engine.replay(chain, "exec_001", FidelityLevel.LOGICAL)
        assert result.status == ReplayStatus.COMPLETED
        assert result.final_state["status"] == "completed"
        assert result.final_state["events_processed"] == 4

    def test_replay_causal_detects_clock_violation(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.tool_call("read", {}), "exec_001"))

        # Manually set vector clock backwards on second evidence
        d = chain[1].to_dict()
        d["causal"]["vector_clock"] = {"agent.test": 0}  # Should be >= 1
        from openbase_core.evidence import Evidence
        broken = Evidence.from_dict(d)
        broken_chain = [chain[0], broken]

        result = engine.replay(broken_chain, "exec_001", FidelityLevel.CAUSAL)
        assert result.status == ReplayStatus.FAILED
        assert result.error_code == ReplayErrorCode.E004

    def test_replay_generates_trace_steps(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("done"), "exec_001"))

        result = engine.replay(chain, "exec_001", FidelityLevel.LOGICAL)
        assert len(result.steps) == 2
        assert result.steps[0].event_type == "AGENT_STARTED"
        assert result.steps[1].event_type == "AGENT_FINISHED"
        assert result.steps[0].state_before["status"] == "created"
        assert result.steps[0].state_after["status"] == "running"
        assert result.steps[1].state_after["status"] == "completed"

    def test_execution_summary_completed(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("done"), "exec_001"))

        result = engine.replay(chain, "exec_001", FidelityLevel.LOGICAL)
        summary = engine.get_execution_summary(result)
        assert summary["status"] == "completed"
        assert summary["total_steps"] == 2
        assert summary["all_hashes_valid"] is True

    def test_execution_summary_failed(self):
        engine = ReplayEngine()
        result = engine.replay([], "exec_001")
        summary = engine.get_execution_summary(result)
        assert summary["status"] == "failed"
        assert summary["error_code"] == "E006"

    def test_replay_agent_failed_state(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_failed("crash"), "exec_001"))

        result = engine.replay(chain, "exec_001", FidelityLevel.LOGICAL)
        assert result.final_state["status"] == "failed"
        assert result.final_state["error"] == "crash"

    def test_replay_result_to_dict(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = ReplayEngine(signer)

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]
        result = engine.replay(chain, "exec_001", FidelityLevel.STRUCTURAL)

        d = result.to_dict()
        assert d["replay_id"].startswith("rpl_")
        assert d["status"] == "completed"
        assert d["total_steps"] == 1

    def test_replay_without_signer_structural_only(self):
        """Without a signer, hash verification is skipped but chain structure still checked."""
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine_no_signer = ReplayEngine()  # No signer

        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("done"), "exec_001"))

        result = engine_no_signer.replay(chain, "exec_001", FidelityLevel.STRUCTURAL)
        # Structural should pass (chain links correct, just no individual hash verify)
        assert result.status == ReplayStatus.COMPLETED
'''

path = r'D:\OpenBase\openbase_core\tests\test_replay.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_replay.py written')
