import os

code = '''"""
OpenBase Trust Engine
Trust v1.0 Implementation — computes trust scores from evidence chains.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math


@dataclass
class TrustDimensions:
    """Five dimensions of trust scoring."""
    evidence_volume: float = 0.0     # Quantity of evidence
    evidence_quality: float = 0.0    # Signature/hash validity
    consistency: float = 0.0         # No contradictory events
    recency: float = 0.0            # Freshness of evidence
    peer_attestation: float = 0.0   # Certificates from peers

    def to_dict(self) -> Dict[str, float]:
        return {
            "evidence_volume": round(self.evidence_volume, 4),
            "evidence_quality": round(self.evidence_quality, 4),
            "consistency": round(self.consistency, 4),
            "recency": round(self.recency, 4),
            "peer_attestation": round(self.peer_attestation, 4),
        }

    def clamp(self):
        """Clamp all dimensions to [0.0, 1.0]."""
        for attr in ["evidence_volume", "evidence_quality", "consistency", "recency", "peer_attestation"]:
            setattr(self, attr, max(0.0, min(1.0, getattr(self, attr))))


@dataclass
class TrustScore:
    """Trust score for a subject (Runtime or Agent)."""
    subject_id: str
    subject_type: str  # runtime, agent, model, tool
    score: float
    confidence: float
    dimensions: TrustDimensions
    evidence_count: int
    last_evidence_id: Optional[str] = None
    certificates: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    previous_score: Optional[float] = None
    trend: str = "stable"  # rising, stable, falling

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "score": round(self.score, 4),
            "confidence": round(self.confidence, 4),
            "dimensions": self.dimensions.to_dict(),
            "evidence_count": self.evidence_count,
            "last_evidence_id": self.last_evidence_id,
            "certificates": self.certificates,
            "last_updated": self.last_updated,
            "previous_score": self.previous_score,
            "trend": self.trend,
        }


class TrustEngine:
    """Computes trust scores based on evidence history.

    Dimensions (with weights):
    - evidence_volume:   0.30 — quantity of valid evidence
    - evidence_quality:  0.25 — signature/hash validity
    - consistency:       0.20 — no contradictory events
    - recency:           0.15 — freshness with time decay
    - peer_attestation:  0.10 — certificates from trusted peers
    """

    DIMENSION_WEIGHTS = {
        "evidence_volume": 0.30,
        "evidence_quality": 0.25,
        "consistency": 0.20,
        "recency": 0.15,
        "peer_attestation": 0.10,
    }

    # Score thresholds
    MIN_EVIDENCE_FOR_FULL_VOLUME = 500
    DECAY_LAMBDA = 0.01  # per day

    def __init__(self, signer=None):
        """Initialize TrustEngine.

        Args:
            signer: EvidenceSigner for signature verification.
        """
        self._signer = signer
        self._score_history: Dict[str, List[float]] = {}

    def compute_trust(
        self,
        subject_id: str,
        subject_type: str,
        evidence_chain: list,
        certificates: Optional[List[str]] = None,
        previous_score: Optional[float] = None,
    ) -> TrustScore:
        """Compute a trust score from an evidence chain.

        Args:
            subject_id: Subject identifier (e.g., 'agent.openclaw.demo')
            subject_type: 'runtime', 'agent', 'model', or 'tool'
            evidence_chain: List of Evidence objects
            certificates: List of certificate IDs
            previous_score: Previous trust score for trend tracking

        Returns:
            TrustScore with all dimensions, aggregate score, and confidence.
        """
        certs = certificates or []
        evidence_count = len(evidence_chain)

        # 1. Evidence Volume (0-1)
        volume = min(evidence_count / self.MIN_EVIDENCE_FOR_FULL_VOLUME, 1.0)

        # 2. Evidence Quality (0-1) — based on valid hashes and signatures
        quality = self._compute_quality(evidence_chain)

        # 3. Consistency (0-1) — check for contradictions
        consistency = self._compute_consistency(evidence_chain)

        # 4. Recency (0-1) — time-weighted freshness
        recency = self._compute_recency(evidence_chain)

        # 5. Peer Attestation (0-1) — certificates
        peer = min(len(certs) / 10.0, 1.0) if certs else 0.0

        dimensions = TrustDimensions(
            evidence_volume=volume,
            evidence_quality=quality,
            consistency=consistency,
            recency=recency,
            peer_attestation=peer,
        )

        # Weighted aggregate score
        score = (
            self.DIMENSION_WEIGHTS["evidence_volume"] * volume
            + self.DIMENSION_WEIGHTS["evidence_quality"] * quality
            + self.DIMENSION_WEIGHTS["consistency"] * consistency
            + self.DIMENSION_WEIGHTS["recency"] * recency
            + self.DIMENSION_WEIGHTS["peer_attestation"] * peer
        )

        # Confidence: higher with more evidence
        confidence = min(evidence_count / 100.0, 1.0)

        # Trend
        trend = "stable"
        if previous_score is not None:
            if score > previous_score + 0.01:
                trend = "rising"
            elif score < previous_score - 0.01:
                trend = "falling"

        # Track history
        if subject_id not in self._score_history:
            self._score_history[subject_id] = []
        self._score_history[subject_id].append(score)

        last_evid = evidence_chain[-1].evidence_id if evidence_chain else None

        return TrustScore(
            subject_id=subject_id,
            subject_type=subject_type,
            score=score,
            confidence=confidence,
            dimensions=dimensions,
            evidence_count=evidence_count,
            last_evidence_id=last_evid,
            certificates=certs,
            previous_score=previous_score,
            trend=trend,
        )

    def _compute_quality(self, evidence_chain: list) -> float:
        """Compute evidence quality based on signature validity."""
        if not evidence_chain:
            return 0.0
        if not self._signer:
            return 0.5  # Can't verify without signer

        valid_count = 0
        for evidence in evidence_chain:
            if self._signer.verify_evidence(evidence):
                valid_count += 1

        return valid_count / len(evidence_chain)

    def _compute_consistency(self, evidence_chain: list) -> float:
        """Check for contradictory events (e.g., multiple agent failures without recovery)."""
        if not evidence_chain:
            return 0.0

        error_count = 0
        success_count = 0
        for evidence in evidence_chain:
            et = evidence.event_type
            if hasattr(et, 'value'):
                et = et.value
            if et in ("AGENT_FAILED", "TOOL_ERROR"):
                error_count += 1
            elif et in ("AGENT_FINISHED", "TOOL_RESULT"):
                success_count += 1

        total = error_count + success_count
        if total == 0:
            return 0.5  # Neutral

        # Higher ratio of successes = higher consistency
        return success_count / total

    def _compute_recency(self, evidence_chain: list) -> float:
        """Compute recency with exponential decay."""
        if not evidence_chain:
            return 0.0

        now = datetime.now(timezone.utc)
        scores = []

        for evidence in evidence_chain:
            try:
                ts = datetime.fromisoformat(evidence.timestamp.replace("Z", "+00:00"))
                age_days = (now - ts).total_seconds() / 86400.0
                decay = math.exp(-self.DECAY_LAMBDA * max(age_days, 0))
                scores.append(decay)
            except (ValueError, AttributeError):
                scores.append(0.5)  # Default if timestamp unparseable

        return sum(scores) / len(scores) if scores else 0.0

    def get_trust_level(self, score: float) -> str:
        """Map a numeric score to a trust level label."""
        if score >= 0.90:
            return "PLATINUM"
        elif score >= 0.70:
            return "GOLD"
        elif score >= 0.50:
            return "SILVER"
        elif score >= 0.30:
            return "BRONZE"
        else:
            return "UNTRUSTED"

    def get_score_history(self, subject_id: str) -> List[float]:
        """Get historical scores for a subject."""
        return self._score_history.get(subject_id, [])

    def should_renew_certificate(self, trust_score: TrustScore, current_level: str) -> bool:
        """Determine if a certificate should be renewed."""
        level_thresholds = {
            "PLATINUM": 0.90,
            "GOLD": 0.70,
            "SILVER": 0.50,
            "BRONZE": 0.30,
        }
        threshold = level_thresholds.get(current_level, 0.30)
        return trust_score.score >= threshold and trust_score.evidence_count > 0
'''

path = r'D:\OpenBase\openbase_core\trust\engine.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('trust/engine.py written')
