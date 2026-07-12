"""
OpenBase Certification System
Conformance testing and certification for Runtimes and Agents.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid


class CertStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    PENDING = "PENDING"


class ComplianceLevel(str, Enum):
    COMPATIBLE = "COMPATIBLE"      # Basic OBS event emission
    CERTIFIED = "CERTIFIED"        # Full evidence chain
    VERIFIED = "VERIFIED"          # All checks + replay
    GOLD = "GOLD"                  # All checks + high trust + certificates


@dataclass
class ComplianceCheck:
    """A single compliance check result."""
    check_id: str
    name: str
    description: str
    status: CertStatus
    details: str = ""
    evidence_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "details": self.details,
            "evidence_count": self.evidence_count,
        }


@dataclass
class CertificationResult:
    """Result of a certification run."""
    cert_id: str
    subject_id: str
    subject_type: str
    level: ComplianceLevel
    checks: List[ComplianceCheck] = field(default_factory=list)
    overall_status: CertStatus = CertStatus.PENDING
    issued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    valid_until: Optional[str] = None
    signature: Optional[str] = None

    @property
    def passed_checks(self) -> int:
        return sum(1 for c in self.checks if c.status == CertStatus.PASS)

    @property
    def total_checks(self) -> int:
        return len(self.checks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cert_id": self.cert_id,
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "level": self.level.value,
            "overall_status": self.overall_status.value,
            "passed_checks": self.passed_checks,
            "total_checks": self.total_checks,
            "checks": [c.to_dict() for c in self.checks],
            "issued_at": self.issued_at,
            "valid_until": self.valid_until,
        }

    def to_report(self) -> str:
        """Generate a human-readable certification report."""
        lines = [
            "=" * 60,
            f"  OpenBase Certification Report",
            "=" * 60,
            f"  Subject:     {self.subject_id}",
            f"  Type:        {self.subject_type}",
            f"  Level:       {self.level.value}",
            f"  Status:      {self.overall_status.value}",
            f"  Passed:      {self.passed_checks}/{self.total_checks}",
            f"  Issued:      {self.issued_at}",
            "=" * 60,
            "",
            "  Compliance Checks:",
        ]
        for check in self.checks:
            icon = "PASS" if check.status == CertStatus.PASS else "FAIL" if check.status == CertStatus.FAIL else "PART"
            lines.append(f"    [{icon}] {check.name}: {check.description}")
        if self.valid_until:
            lines.append(f"\n  Valid until: {self.valid_until}")
        lines.append("=" * 60)
        return "\n".join(lines)


class CertificationEngine:
    """Tests Runtimes and Agents for OpenBase compliance.

    Compliance Levels:
    - COMPATIBLE: Can emit valid OBS events
    - CERTIFIED:  OBS + Evidence chain with signatures
    - VERIFIED:   CERTIFIED + Replay verification
    - GOLD:       VERIFIED + Trust score >= 0.70 + Certificate issued
    """

    def __init__(self):
        self._results: Dict[str, CertificationResult] = {}

    def certify_runtime(self, openbase_runtime, runtime_name: str) -> CertificationResult:
        """Run full certification suite against a runtime.

        Args:
            openbase_runtime: An OpenBaseRuntime instance that has been used
                              to execute an agent with events.
            runtime_name: Name of the runtime being certified.

        Returns:
            CertificationResult with all checks and level.
        """
        cert_id = f"ocert_{uuid.uuid4().hex[:8]}"
        result = CertificationResult(
            cert_id=cert_id,
            subject_id=runtime_name,
            subject_type="runtime",
            level=ComplianceLevel.COMPATIBLE,
        )

        events = openbase_runtime._events
        evidence_chain = openbase_runtime.get_evidence_chain()
        execution = openbase_runtime.finish() if openbase_runtime._events else None

        # Check 1: Event Emission
        check1 = self._check_event_emission(events)
        result.checks.append(check1)

        # Check 2: Event Validity
        check2 = self._check_event_validity(events)
        result.checks.append(check2)

        # Check 3: Evidence Generation
        check3 = self._check_evidence_generation(evidence_chain)
        result.checks.append(check3)

        # Check 4: Hash Chain Integrity
        check4 = self._check_hash_chain(evidence_chain)
        result.checks.append(check4)

        # Check 5: Replay Capability
        check5 = self._check_replay(execution) if execution else None
        if check5:
            result.checks.append(check5)

        # Check 6: Trust Score
        check6 = self._check_trust(execution) if execution else None
        if check6:
            result.checks.append(check6)

        # Check 7: Certificate Issuance
        check7 = self._check_certificate(execution) if execution else None
        if check7:
            result.checks.append(check7)

        # Determine level
        result.level = self._determine_level(result)
        result.overall_status = CertStatus.PASS if self._all_critical_pass(result) else CertStatus.FAIL

        self._results[cert_id] = result
        return result

    def _check_event_emission(self, events: list) -> ComplianceCheck:
        passed = len(events) > 0
        return ComplianceCheck(
            check_id="REQ-EVENT-001",
            name="Event Emission",
            description="Runtime can emit events",
            status=CertStatus.PASS if passed else CertStatus.FAIL,
            details=f"Emitted {len(events)} events" if passed else "No events emitted",
            evidence_count=len(events),
        )

    def _check_event_validity(self, events: list) -> ComplianceCheck:
        if not events:
            return ComplianceCheck(
                check_id="REQ-EVENT-002",
                name="Event Validity",
                description="Events conform to OBS schema",
                status=CertStatus.FAIL,
                details="No events to validate",
            )

        from openbase_core.event import EventValidator
        validator = EventValidator()
        valid_count = sum(1 for e in events if validator.is_valid(e))

        all_valid = valid_count == len(events)
        return ComplianceCheck(
            check_id="REQ-EVENT-002",
            name="Event Validity",
            description="Events conform to OBS schema",
            status=CertStatus.PASS if all_valid else CertStatus.PARTIAL,
            details=f"{valid_count}/{len(events)} events valid",
            evidence_count=valid_count,
        )

    def _check_evidence_generation(self, chain: list) -> ComplianceCheck:
        passed = len(chain) > 0
        return ComplianceCheck(
            check_id="REQ-EVID-001",
            name="Evidence Generation",
            description="Runtime generates evidence from events",
            status=CertStatus.PASS if passed else CertStatus.FAIL,
            details=f"Generated {len(chain)} evidence records" if passed else "No evidence generated",
            evidence_count=len(chain),
        )

    def _check_hash_chain(self, chain: list) -> ComplianceCheck:
        if len(chain) < 2:
            return ComplianceCheck(
                check_id="REQ-EVID-002",
                name="Hash Chain Integrity",
                description="Evidence forms a valid hash chain",
                status=CertStatus.PASS if len(chain) == 1 else CertStatus.FAIL,
                details="Single evidence (no chain to verify)" if len(chain) == 1 else "No evidence",
                evidence_count=len(chain),
            )

        # Check parent_id linkage
        valid = True
        for i in range(1, len(chain)):
            if chain[i].causal.parent_id != chain[i-1].hash:
                valid = False
                break

        return ComplianceCheck(
            check_id="REQ-EVID-002",
            name="Hash Chain Integrity",
            description="Evidence forms a valid hash chain",
            status=CertStatus.PASS if valid else CertStatus.FAIL,
            details="Hash chain verified" if valid else "Hash chain broken",
            evidence_count=len(chain),
        )

    def _check_replay(self, execution) -> Optional[ComplianceCheck]:
        if not execution or not execution.replay_result:
            return None

        from openbase_core.replay import ReplayStatus
        replay = execution.replay_result
        passed = replay.status == ReplayStatus.COMPLETED

        return ComplianceCheck(
            check_id="REQ-REPLAY-001",
            name="Replay Capability",
            description="Execution can be replayed from evidence",
            status=CertStatus.PASS if passed else CertStatus.FAIL,
            details=f"Replay {replay.status.value}, {len(replay.steps)} steps",
            evidence_count=len(replay.steps),
        )

    def _check_trust(self, execution) -> Optional[ComplianceCheck]:
        if not execution or not execution.trust_score:
            return None

        ts = execution.trust_score
        passed = ts.score >= 0.30

        return ComplianceCheck(
            check_id="REQ-TRUST-001",
            name="Trust Score",
            description="Trust score meets minimum threshold",
            status=CertStatus.PASS if passed else CertStatus.FAIL,
            details=f"Score: {ts.score:.2f} (threshold: 0.30)",
            evidence_count=ts.evidence_count,
        )

    def _check_certificate(self, execution) -> Optional[ComplianceCheck]:
        if not execution:
            return None

        has_cert = execution.certificate is not None
        return ComplianceCheck(
            check_id="REQ-CERT-001",
            name="Certificate Issuance",
            description="Certificate can be issued based on trust",
            status=CertStatus.PASS if has_cert else CertStatus.PARTIAL,
            details=f"Certificate: {execution.certificate.level}" if has_cert else "No certificate (score too low)",
            evidence_count=0,
        )

    def _determine_level(self, result: CertificationResult) -> ComplianceLevel:
        """Determine certification level based on checks passed."""
        passed_ids = {c.check_id for c in result.checks if c.status == CertStatus.PASS}

        if "REQ-CERT-001" in passed_ids and "REQ-TRUST-001" in passed_ids:
            return ComplianceLevel.GOLD
        elif "REQ-REPLAY-001" in passed_ids:
            return ComplianceLevel.VERIFIED
        elif "REQ-EVID-002" in passed_ids:
            return ComplianceLevel.CERTIFIED
        elif "REQ-EVENT-001" in passed_ids:
            return ComplianceLevel.COMPATIBLE
        return ComplianceLevel.COMPATIBLE

    def _all_critical_pass(self, result: CertificationResult) -> bool:
        """Critical checks: EVENT-001, EVID-001 must pass."""
        critical = {"REQ-EVENT-001", "REQ-EVID-001"}
        for check in result.checks:
            if check.check_id in critical and check.status != CertStatus.PASS:
                return False
        return True

    def get_result(self, cert_id: str) -> Optional[CertificationResult]:
        return self._results.get(cert_id)
