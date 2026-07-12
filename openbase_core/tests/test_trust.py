"""
Tests for OpenBase Trust Engine
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pytest
from openbase_core.event import EventFactory
from openbase_core.evidence import EvidenceSigner
from openbase_core.trust import TrustEngine, TrustScore, TrustDimensions


class TestTrustEngine:
    def test_empty_chain_gives_zero_volume(self):
        engine = TrustEngine()
        score = engine.compute_trust("agent.test", "agent", [])
        assert score.dimensions.evidence_volume == 0.0
        assert score.evidence_count == 0

    def test_small_chain_partial_volume(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = []
        for i in range(50):
            chain.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_001"))

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.evidence_volume > 0.0
        assert score.dimensions.evidence_volume < 1.0
        assert score.evidence_count == 50

    def test_full_volume_at_threshold(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = []
        for i in range(TrustEngine.MIN_EVIDENCE_FOR_FULL_VOLUME):
            chain.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_001"))

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.evidence_volume == 1.0
        assert score.evidence_count == TrustEngine.MIN_EVIDENCE_FOR_FULL_VOLUME

    def test_quality_with_valid_evidence(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.evidence_quality > 0.0

    def test_consistency_with_successes(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = []
        for i in range(10):
            chain.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_001"))
        chain.append(signer.sign_event(factory.agent_finished("success"), "exec_001"))

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.consistency > 0.5  # more successes than errors

    def test_consistency_with_errors(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = []
        chain.append(signer.sign_event(factory.agent_started("task"), "exec_001"))
        for i in range(5):
            chain.append(signer.sign_event(factory.agent_failed(f"error_{i}"), "exec_001"))

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.consistency < 0.5  # more errors than successes

    def test_recency_not_zero(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert score.dimensions.recency > 0.0

    def test_peer_attestation_with_certificates(self):
        engine = TrustEngine()
        score = engine.compute_trust(
            "agent.certified", "agent", [],
            certificates=["cert_gold_001", "cert_silver_002"],
        )

        assert score.dimensions.peer_attestation > 0.0
        assert len(score.certificates) == 2

    def test_peer_attestation_without_certificates(self):
        engine = TrustEngine()
        score = engine.compute_trust("agent.uncertified", "agent", [])

        assert score.dimensions.peer_attestation == 0.0

    def test_score_in_range(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert 0.0 <= score.score <= 1.0

    def test_confidence_increases_with_evidence(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")

        engine = TrustEngine(signer)

        chain_small = [signer.sign_event(factory.agent_started("task"), "exec_001")]
        score_small = engine.compute_trust("agent.test", "agent", chain_small)

        chain_large = []
        for i in range(200):
            chain_large.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_002"))
        score_large = engine.compute_trust("agent.test", "agent", chain_large)

        assert score_large.confidence > score_small.confidence

    def test_trend_rising(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = TrustEngine(signer)

        # Low previous score
        score = engine.compute_trust(
            "agent.test", "agent",
            [signer.sign_event(factory.agent_started("task"), "exec_001")] * 100,
            previous_score=0.3,
        )
        assert score.trend == "rising"

    def test_trend_stable(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = TrustEngine(signer)

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]
        score = engine.compute_trust("agent.test", "agent", chain)
        current = score.score

        # Same score as previous
        score2 = engine.compute_trust(
            "agent.test", "agent", chain,
            previous_score=current,
        )
        assert score2.trend == "stable"

    def test_score_history_tracks_changes(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = TrustEngine(signer)

        engine.compute_trust("agent.test", "agent", [signer.sign_event(factory.agent_started("t1"), "exec_001")])
        engine.compute_trust("agent.test", "agent", [signer.sign_event(factory.agent_started("t2"), "exec_001")])

        history = engine.get_score_history("agent.test")
        assert len(history) == 2

    def test_get_trust_level(self):
        engine = TrustEngine()
        assert engine.get_trust_level(0.95) == "PLATINUM"
        assert engine.get_trust_level(0.80) == "GOLD"
        assert engine.get_trust_level(0.60) == "SILVER"
        assert engine.get_trust_level(0.40) == "BRONZE"
        assert engine.get_trust_level(0.10) == "UNTRUSTED"

    def test_should_renew_gold_when_score_high(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = TrustEngine(signer)

        # Build a chain with many successful agent completions to boost consistency
        chain = []
        for i in range(200):
            chain.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_001"))
            chain.append(signer.sign_event(factory.agent_finished(f"success_{i}"), "exec_001"))

        score = engine.compute_trust("agent.test", "agent", chain)

        # With 400 evidence (200 start + 200 finish), score should exceed GOLD threshold
        assert score.score >= 0.70, f"Expected score >= 0.70, got {score.score}"
        assert engine.should_renew_certificate(score, "GOLD") is True

    def test_should_not_renew_when_empty(self):
        engine = TrustEngine()
        score = engine.compute_trust("agent.empty", "agent", [])
        assert engine.should_renew_certificate(score, "GOLD") is False

    def test_dimensions_clamp(self):
        dims = TrustDimensions(
            evidence_volume=2.0,
            evidence_quality=-0.5,
            consistency=0.5,
            recency=0.5,
            peer_attestation=0.5,
        )
        dims.clamp()
        assert 0.0 <= dims.evidence_volume <= 1.0
        assert 0.0 <= dims.evidence_quality <= 1.0

    def test_trust_score_to_dict(self):
        score = TrustScore(
            subject_id="agent.test",
            subject_type="agent",
            score=0.75,
            confidence=0.8,
            dimensions=TrustDimensions(0.7, 0.8, 0.6, 0.9, 0.5),
            evidence_count=100,
            certificates=["cert_001"],
            trend="rising",
        )
        d = score.to_dict()
        assert d["subject_id"] == "agent.test"
        assert d["score"] == 0.75
        assert d["trend"] == "rising"
        assert d["certificates"] == ["cert_001"]
