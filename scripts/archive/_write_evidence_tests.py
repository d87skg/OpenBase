import os

code = '''"""
Tests for OpenBase Evidence Engine
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import json
import pytest
from openbase_core.event import EventFactory
from openbase_core.evidence import Evidence, EvidenceSigner


class TestEvidenceSigner:
    def test_sign_event_creates_evidence(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.openclaw.demo", "openclaw", "0.1.0")
        event = factory.agent_started("test task")

        evidence = signer.sign_event(event, "exec_001")

        assert evidence.event_id == event.event_id
        assert evidence.execution_id == "exec_001"
        assert evidence.spec_version == "2.0"
        assert evidence.hash is not None
        assert len(evidence.hash) == 64  # SHA-256 hex
        assert evidence.signature.startswith("ed25519:")
        assert evidence.public_key.startswith("ed25519:")

    def test_genesis_evidence_has_null_parent(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")

        evidence = signer.sign_event(event, "exec_001")
        assert evidence.causal.parent_id is None

    def test_chain_links_parent_hash(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        e1 = factory.agent_started("task1")
        ev1 = signer.sign_event(e1, "exec_001")

        e2 = factory.tool_call("read", {"path": "/tmp"})
        ev2 = signer.sign_event(e2, "exec_001")

        assert ev1.causal.parent_id is None
        assert ev2.causal.parent_id == ev1.hash

    def test_verify_valid_evidence(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")
        evidence = signer.sign_event(event, "exec_001")

        assert signer.verify_evidence(evidence) is True

    def test_verify_tampered_evidence_fails(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")
        evidence = signer.sign_event(event, "exec_001")

        # Tamper with payload
        tampered_dict = evidence.to_dict()
        tampered_dict["payload"]["task"] = "tampered task"
        tampered = Evidence.from_dict(tampered_dict)

        assert signer.verify_evidence(tampered) is False

    def test_verify_entire_chain(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        chain = []
        for i in range(5):
            event = factory.agent_started(f"task_{i}")
            chain.append(signer.sign_event(event, "exec_001"))

        assert signer.verify_chain(chain) is True

    def test_broken_chain_fails(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        chain = []
        for i in range(3):
            event = factory.agent_started(f"task_{i}")
            chain.append(signer.sign_event(event, "exec_001"))

        # Break chain by removing middle element
        broken_chain = [chain[0], chain[2]]
        assert signer.verify_chain(broken_chain) is False

    def test_vector_clock_increments(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        e1 = factory.agent_started("task1")
        ev1 = signer.sign_event(e1, "exec_001")

        e2 = factory.tool_call("read", {})
        ev2 = signer.sign_event(e2, "exec_001")

        vc1 = ev1.causal.vector_clock
        vc2 = ev2.causal.vector_clock

        assert vc2.get("agent.test", 0) >= vc1.get("agent.test", 0)

    def test_signature_is_valid_ed25519(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")
        evidence = signer.sign_event(event, "exec_001")

        import base64
        sig_part = evidence.signature.replace("ed25519:", "")
        sig_bytes = base64.b64decode(sig_part)
        assert len(sig_bytes) == 64  # Ed25519 signature is 64 bytes

    def test_reset_chain_starts_new(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        e1 = factory.agent_started("run1")
        signer.sign_event(e1, "exec_001")

        signer.reset_chain()

        e2 = factory.agent_started("run2")
        ev2 = signer.sign_event(e2, "exec_002")

        assert ev2.causal.parent_id is None

    def test_evidence_to_dict_and_back(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")
        original = signer.sign_event(event, "exec_001")

        d = original.to_dict()
        restored = Evidence.from_dict(d)

        assert restored.evidence_id == original.evidence_id
        assert restored.hash == original.hash
        assert restored.signature == original.signature

    def test_evidence_to_json(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        event = factory.agent_started("task")
        evidence = signer.sign_event(event, "exec_001")

        json_str = evidence.to_json(indent=2)
        parsed = json.loads(json_str)
        assert parsed["spec_version"] == "2.0"
        assert parsed["event_id"] == event.event_id

    def test_multiple_executions_independent_chains(self):
        signer1 = EvidenceSigner()
        signer2 = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        e1 = factory.agent_started("run1")
        ev1 = signer1.sign_event(e1, "exec_A")

        e2 = factory.agent_started("run2")
        ev2 = signer2.sign_event(e2, "exec_B")

        # Both should be genesis (parent_id = None)
        assert ev1.causal.parent_id is None
        assert ev2.causal.parent_id is None
        # Different chains, different hashes
        assert ev1.hash != ev2.hash
'''

path = r'D:\OpenBase\openbase_core\tests\test_evidence.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_evidence.py written')
