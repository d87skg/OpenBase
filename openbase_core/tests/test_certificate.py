"""
Tests for OpenBase Certificate Engine
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pytest
from openbase_core.event import EventFactory
from openbase_core.evidence import EvidenceSigner
from openbase_core.trust import TrustEngine, TrustScore, TrustDimensions
from openbase_core.certificate import Certificate, CertificateEngine


class TestCertificateEngine:
    def test_issue_certificate_with_high_score(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 300
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 300
        ts = trust.compute_trust("agent.test", "agent", chain)

        cert = cert_engine.issue("agent.test", "agent", ts, level="GOLD")
        assert cert is not None
        assert cert.level == "GOLD"
        assert cert.subject_id == "agent.test"
        assert cert.status == "active"
        assert cert.certificate_id.startswith("cert_")

    def test_issue_fails_when_score_too_low(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")]
        ts = trust.compute_trust("agent.test", "agent", chain)

        cert = cert_engine.issue("agent.test", "agent", ts, level="GOLD")
        assert cert is None  # Score too low for GOLD

    def test_auto_level_from_score(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 100
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 100
        ts = trust.compute_trust("agent.test", "agent", chain)

        cert = cert_engine.issue("agent.test", "agent", ts)  # No level specified
        assert cert is not None
        # Score determines level automatically
        assert cert.level in ["BRONZE", "SILVER", "GOLD", "PLATINUM"]

    def test_verify_valid_certificate(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)
        cert = cert_engine.issue("agent.test", "agent", ts, level="SILVER")

        assert cert_engine.verify(cert) is True

    def test_verify_revoked_fails(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)
        cert = cert_engine.issue("agent.test", "agent", ts, level="SILVER")

        cert_engine.revoke(cert.certificate_id, "testing revocation")
        assert cert_engine.verify(cert) is False

    def test_revoke_certificate(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)
        cert = cert_engine.issue("agent.test", "agent", ts, level="SILVER")

        revoked = cert_engine.revoke(cert.certificate_id, "misconduct")
        assert revoked.status == "revoked"
        assert revoked.revocation_reason == "misconduct"
        assert revoked.revoked_at is not None

    def test_renew_certificate(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)
        cert = cert_engine.issue("agent.test", "agent", ts, level="SILVER")
        original_count = cert.renewal_count

        renewed = cert_engine.renew(cert.certificate_id, ts)
        assert renewed is not None
        assert renewed.renewal_count == original_count + 1

    def test_renew_revoked_fails(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)
        cert = cert_engine.issue("agent.test", "agent", ts, level="SILVER")
        cert_engine.revoke(cert.certificate_id, "test")

        renewed = cert_engine.renew(cert.certificate_id, ts)
        assert renewed is None

    def test_get_active_certificates(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)

        cert_engine.issue("agent.test", "agent", ts, level="SILVER")
        cert_engine.issue("agent.test", "agent", ts, level="GOLD")

        active = cert_engine.get_active_certificates("agent.test")
        assert len(active) == 2

    def test_certificate_to_dict(self):
        cert = Certificate(
            certificate_id="cert_test_001",
            subject_id="agent.test",
            subject_type="agent",
            level="GOLD",
            issuer="registry.openbase.main",
            issued_at="2026-07-07T12:00:00Z",
            expires_at="2026-10-07T12:00:00Z",
            trust_snapshot={"score": 0.85, "evidence_count": 150},
            signature="sha256:abc123",
            status="active",
        )
        d = cert.to_dict()
        assert d["certificate_id"] == "cert_test_001"
        assert d["level"] == "GOLD"
        assert d["status"] == "active"

    def test_certificate_is_expired(self):
        cert = Certificate(
            certificate_id="cert_expired",
            subject_id="agent.test",
            subject_type="agent",
            level="BRONZE",
            issuer="registry",
            issued_at="2025-01-01T00:00:00Z",
            expires_at="2025-02-01T00:00:00Z",
            trust_snapshot={"score": 0.3},
            signature="sha256:def",
        )
        assert cert.is_expired() is True

    def test_certificate_not_expired(self):
        cert = Certificate(
            certificate_id="cert_valid",
            subject_id="agent.test",
            subject_type="agent",
            level="BRONZE",
            issuer="registry",
            issued_at="2026-07-01T00:00:00Z",
            expires_at="2027-07-01T00:00:00Z",
            trust_snapshot={"score": 0.5},
            signature="sha256:ghi",
        )
        assert cert.is_expired() is False

    def test_list_all_certificates(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        trust = TrustEngine(signer)
        cert_engine = CertificateEngine()

        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200
        chain += [signer.sign_event(factory.agent_finished("done"), "exec_001")] * 200
        ts = trust.compute_trust("agent.test", "agent", chain)

        cert_engine.issue("agent.a", "agent", ts, level="BRONZE")
        cert_engine.issue("agent.b", "agent", ts, level="SILVER")

        all_certs = cert_engine.list_all()
        assert len(all_certs) == 2

    def test_update_statuses(self):
        cert_engine = CertificateEngine()
        # Create an expired cert manually
        from datetime import datetime, timezone, timedelta
        expired_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        cert = Certificate(
            certificate_id="cert_will_expire",
            subject_id="agent.test",
            subject_type="agent",
            level="BRONZE",
            issuer="registry",
            issued_at="2026-01-01T00:00:00Z",
            expires_at=expired_date,
            trust_snapshot={"score": 0.3},
            signature="sha256:jkl",
            status="active",
        )
        cert_engine._certificates[cert.certificate_id] = cert

        cert_engine.update_statuses()
        updated = cert_engine.get_certificate("cert_will_expire")
        assert updated.status == "expired"

    def test_get_nonexistent_certificate(self):
        cert_engine = CertificateEngine()
        assert cert_engine.get_certificate("nonexistent") is None

    def test_revoke_nonexistent(self):
        cert_engine = CertificateEngine()
        assert cert_engine.revoke("nonexistent", "reason") is None
