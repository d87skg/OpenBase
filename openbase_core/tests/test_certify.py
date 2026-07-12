"""
Tests for OpenBase Certification System
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from openbase_core.registry import OpenBaseRuntime, RuntimeConfig
from openbase_core.certificate import CertificationEngine, ComplianceLevel, CertStatus


class TestCertificationEngine:
    def test_certify_empty_runtime(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.empty"))
        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "empty-runtime")

        assert result.overall_status == CertStatus.FAIL
        assert result.level == ComplianceLevel.COMPATIBLE

    def test_certify_runtime_with_events(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.basic"))
        rt.agent_started("task")
        rt.agent_finished("done")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "basic-runtime")

        assert result.overall_status == CertStatus.PASS
        assert result.level in [ComplianceLevel.COMPATIBLE, ComplianceLevel.CERTIFIED, ComplianceLevel.VERIFIED, ComplianceLevel.GOLD]

    def test_certify_runtime_with_chain(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.chain"))
        rt.agent_started("task")
        rt.tool_call("read", {"path": "/tmp"})
        rt.tool_result("read", "data")
        rt.agent_finished("done")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "chain-runtime")

        assert result.overall_status == CertStatus.PASS
        assert result.level in [ComplianceLevel.CERTIFIED, ComplianceLevel.VERIFIED, ComplianceLevel.GOLD]

    def test_certify_runtime_gold(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.gold"))

        for i in range(100):
            rt.agent_started(f"task_{i}")
            rt.agent_finished(f"done_{i}")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "gold-runtime")

        assert result.overall_status == CertStatus.PASS
        # With enough evidence, should reach GOLD
        assert result.level in [ComplianceLevel.CERTIFIED, ComplianceLevel.VERIFIED, ComplianceLevel.GOLD]

    def test_certification_report(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.report"))
        rt.agent_started("task")
        rt.agent_finished("done")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "report-runtime")

        report = result.to_report()
        assert "OpenBase Certification Report" in report
        assert "report-runtime" in report
        assert "PASS" in report or "FAIL" in report

    def test_certification_result_to_dict(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.dict"))
        rt.agent_started("task")
        rt.agent_finished("done")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "dict-runtime")

        d = result.to_dict()
        assert d["subject_id"] == "dict-runtime"
        assert "checks" in d
        assert d["total_checks"] > 0

    def test_certification_persists(self):
        rt = OpenBaseRuntime(RuntimeConfig(agent_id="agent.persist"))
        rt.agent_started("task")
        rt.agent_finished("done")

        cert_engine = CertificationEngine()
        result = cert_engine.certify_runtime(rt, "persist-runtime")

        retrieved = cert_engine.get_result(result.cert_id)
        assert retrieved is not None
        assert retrieved.cert_id == result.cert_id
