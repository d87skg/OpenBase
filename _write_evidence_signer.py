import os

code = '''"""
EvidenceSigner — creates signed Evidence from OBS Events.
Implements SHA-256 hash chain + Ed25519 signatures.
"""

import hashlib
import json
from typing import Optional, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from .models import Evidence, Causal


class EvidenceSigner:
    """Creates and verifies signed Evidence objects."""

    def __init__(self):
        self._private_key = ed25519.Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()
        self._public_key_b64 = self._encode_public_key()
        self._previous_hash: Optional[str] = None
        self._clock: Dict[str, int] = {}
        self._evidence_count = 0

    def _encode_public_key(self) -> str:
        """Encode public key as ed25519:<base64> string."""
        raw = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        import base64
        return f"ed25519:{base64.b64encode(raw).decode('ascii')}"

    def _canonical_json(self, data: dict) -> bytes:
        """RFC 8785 canonical JSON serialization."""
        return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

    def _compute_hash(self, previous_hash: Optional[str], canonical_data: bytes) -> str:
        """Compute SHA-256 hash for evidence chain."""
        if previous_hash is None:
            previous_hash = "0" * 64  # Genesis: 64 zero bytes
        combined = previous_hash.encode('ascii') + canonical_data
        return hashlib.sha256(combined).hexdigest()

    def _sign(self, evidence_hash: str, execution_id: str) -> str:
        """Create Ed25519 signature: sign(hash + execution_id)."""
        message = (evidence_hash + execution_id).encode('ascii')
        raw_sig = self._private_key.sign(message)
        import base64
        return f"ed25519:{base64.b64encode(raw_sig).decode('ascii')}"

    def sign_event(self, event, execution_id: str, vector_clock: Optional[Dict[str, int]] = None) -> Evidence:
        """Convert an OBS Event into a signed Evidence object."""
        from uuid import uuid4

        # Update vector clock
        if vector_clock:
            self._clock = vector_clock.copy()
        actor = event.actor.id
        self._clock[actor] = self._clock.get(actor, 0) + 1

        # Build evidence data (without hash and signature)
        self._evidence_count += 1
        evidence_data = {
            "evidence_id": f"evid_{uuid4().hex[:12]}",
            "spec_version": "2.0",
            "event_id": event.event_id,
            "execution_id": execution_id,
            "agent_id": event.actor.id,
            "event_type": event.event_type.value if hasattr(event.event_type, 'value') else event.event_type,
            "timestamp": event.timestamp,
            "causal": {
                "parent_id": self._previous_hash,
                "vector_clock": self._clock,
            },
            "payload": event.payload,
            "public_key": self._public_key_b64,
        }

        # Compute hash
        canonical = self._canonical_json(evidence_data)
        evidence_hash = self._compute_hash(self._previous_hash, canonical)

        # Sign
        signature = self._sign(evidence_hash, execution_id)

        # Create evidence
        evidence = Evidence(
            evidence_id=evidence_data["evidence_id"],
            event_id=evidence_data["event_id"],
            execution_id=evidence_data["execution_id"],
            agent_id=evidence_data["agent_id"],
            event_type=evidence_data["event_type"],
            timestamp=evidence_data["timestamp"],
            causal=Causal(
                parent_id=self._previous_hash,
                vector_clock=self._clock.copy(),
            ),
            payload=evidence_data["payload"],
            hash=evidence_hash,
            signature=signature,
            public_key=self._public_key_b64,
        )

        # Update chain state
        self._previous_hash = evidence_hash

        return evidence

    def verify_evidence(self, evidence: Evidence) -> bool:
        """Verify an evidence object's hash and signature."""
        import base64

        # Rebuild data without hash/sig
        verify_data = {
            "evidence_id": evidence.evidence_id,
            "spec_version": evidence.spec_version,
            "event_id": evidence.event_id,
            "execution_id": evidence.execution_id,
            "agent_id": evidence.agent_id,
            "event_type": evidence.event_type,
            "timestamp": evidence.timestamp,
            "causal": evidence.causal.to_dict(),
            "payload": evidence.payload,
            "public_key": evidence.public_key,
        }

        # Verify hash
        canonical = self._canonical_json(verify_data)
        parent = evidence.causal.parent_id
        computed_hash = self._compute_hash(parent, canonical)
        if computed_hash != evidence.hash:
            return False

        # Verify signature
        try:
            # Decode public key
            pk_b64 = evidence.public_key.replace("ed25519:", "")
            pk_bytes = base64.b64decode(pk_b64)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(pk_bytes)

            # Decode signature
            sig_b64 = evidence.signature.replace("ed25519:", "")
            sig_bytes = base64.b64decode(sig_b64)

            # Verify
            message = (evidence.hash + evidence.execution_id).encode('ascii')
            public_key.verify(sig_bytes, message)
            return True
        except Exception:
            return False

    def verify_chain(self, evidence_list: list) -> bool:
        """Verify an entire evidence chain."""
        for i, evidence in enumerate(evidence_list):
            if not self.verify_evidence(evidence):
                return False
            # Check chain continuity
            if i > 0:
                expected_parent = evidence_list[i - 1].hash
                if evidence.causal.parent_id != expected_parent:
                    return False
        return True

    def reset_chain(self):
        """Reset chain state for a new execution."""
        self._previous_hash = None
        self._clock = {}
        self._evidence_count = 0
'''

path = r'D:\OpenBase\openbase_core\evidence\signer.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('evidence/signer.py written')
