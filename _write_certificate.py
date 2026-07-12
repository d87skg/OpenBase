import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'certificate')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Certificate Specification ---
spec = '# OpenBase Certificate Specification v1.0\n\n## Version\n**1.0**\n\n## Status\n**Draft**\n\n---\n\n## 1. Abstract\n\nThe Certificate Layer defines formal trust credentials issued to Runtimes and Agents. A Certificate is a signed, verifiable attestation that a subject meets specific trust criteria at a point in time.\n\n## 2. Certificate Model\n\n### 2.1 Core Principle\n\nA Certificate is:\n- Issued based on verifiable Trust Score\n- Signed by the OpenBase Registry\n- Time-bounded with explicit expiry\n- Revocable if trust conditions degrade\n\n### 2.2 Certificate Levels\n\n| Level | Min Score | Min Evidence | Description |\n|:---|:---|:---|:---|\n| BRONZE | 0.30 | 10 | Basic participation |\n| SILVER | 0.50 | 50 | Consistent good behavior |\n| GOLD | 0.70 | 100 | High trust, peer verified |\n| PLATINUM | 0.90 | 500 | Exceptional trust record |\n\n### 2.3 Certificate Lifecycle\n\n`\nIssued → Active → Expiring → Expired\n                 ↓\n              Revoked\n`\n\n- Issued: Created after trust threshold met\n- Active: Valid and usable\n- Expiring: Within renewal window\n- Expired: Past validity period\n- Revoked: Explicitly invalidated before expiry\n\n## 3. Certificate Structure\n\nA Certificate contains:\n- Subject identity\n- Issuer identity\n- Trust level achieved\n- Evidence snapshot (scores at issuance time)\n- Validity period (issued_at, expires_at)\n- Digital signature from Registry\n\n## 4. Verification\n\nAnyone can verify a Certificate by:\n1. Check signature against Registry public key\n2. Verify subject identity exists in Registry\n3. Confirm certificate not expired or revoked\n4. Optionally: re-verify current Trust Score meets level\n\n## 5. Renewal\n\nCertificates auto-renew if:\n- Current Trust Score still meets level threshold\n- Subject is active (evidence in last 30 days)\n- Certificate not revoked\n\n## 6. Revocation\n\nGrounds for revocation:\n- Trust Score drops below level threshold\n- Evidence of malicious behavior\n- Subject voluntarily requests revocation\n- Subject identity deprecated or retired\n\n## 7. References\n\n- Trust v1.0 (trust score computation)\n- Identity v1.0 (subject identification)\n- Evidence v2.0 (evidence verification)\n- Registry v1.0 (issuer authority)\n'
with open(os.path.join(spec_dir, 'CERTIFICATE_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
    f.write(spec)
print('[1/4] Spec done')

# --- JSON Schema ---
schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/certificate/v1.0/certificate.schema.json",
    "title": "OpenBase Certificate v1.0",
    "description": "Formal trust credential issued to a Runtime or Agent",
    "type": "object",
    "required": ["certificate_id", "subject_id", "subject_type", "level", "issuer", "issued_at", "expires_at", "trust_snapshot", "signature", "status"],
    "properties": {
        "certificate_id": {"type": "string"},
        "subject_id": {"type": "string"},
        "subject_type": {"type": "string", "enum": ["runtime", "agent", "model", "tool"]},
        "level": {"type": "string", "enum": ["BRONZE", "SILVER", "GOLD", "PLATINUM"]},
        "issuer": {"type": "string"},
        "issued_at": {"type": "string", "format": "date-time"},
        "expires_at": {"type": "string", "format": "date-time"},
        "revoked_at": {"type": "string", "format": "date-time"},
        "revocation_reason": {"type": "string"},
        "trust_snapshot": {
            "type": "object",
            "required": ["score", "evidence_count"],
            "properties": {
                "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "evidence_count": {"type": "integer", "minimum": 0},
                "dimensions": {"type": "object"}
            }
        },
        "signature": {"type": "string", "pattern": "^ed25519:[A-Za-z0-9+/=]+$"},
        "status": {"type": "string", "enum": ["active", "expiring", "expired", "revoked"]},
        "renewal_count": {"type": "integer", "minimum": 0},
        "metadata": {"type": "object"}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'certificate.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
print('[2/4] Schema done')

# --- README ---
readme = '# OpenBase Certificate v1.0\n\nDefines formal trust credentials for Runtimes and Agents.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| CERTIFICATE_SPEC_v1.0.md | Full specification |\n| certificate.schema.json | JSON Schema |\n| examples/ | Example certificates |\n'
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('[3/4] README done')

# --- Examples ---
examples = {
    "certificate_gold.json": {
        "certificate_id": "cert_gold_001",
        "subject_id": "runtime.openclaw.0.1.0",
        "subject_type": "runtime",
        "level": "GOLD",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-07-07T12:00:00Z",
        "expires_at": "2026-10-07T12:00:00Z",
        "trust_snapshot": {
            "score": 0.85,
            "evidence_count": 150,
            "dimensions": {
                "evidence_volume": 0.90,
                "evidence_quality": 0.95,
                "consistency": 0.88,
                "recency": 0.80,
                "peer_attestation": 0.75
            }
        },
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "active",
        "renewal_count": 2
    },
    "certificate_silver.json": {
        "certificate_id": "cert_silver_002",
        "subject_id": "agent.newcomer.bot",
        "subject_type": "agent",
        "level": "SILVER",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-07-01T00:00:00Z",
        "expires_at": "2026-10-01T00:00:00Z",
        "trust_snapshot": {
            "score": 0.55,
            "evidence_count": 60
        },
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "active",
        "renewal_count": 0
    },
    "certificate_revoked.json": {
        "certificate_id": "cert_bronze_003",
        "subject_id": "agent.untrusted.bot",
        "subject_type": "agent",
        "level": "BRONZE",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-06-01T00:00:00Z",
        "expires_at": "2026-09-01T00:00:00Z",
        "revoked_at": "2026-07-05T00:00:00Z",
        "revocation_reason": "Trust score dropped below BRONZE threshold",
        "trust_snapshot": {
            "score": 0.15,
            "evidence_count": 3
        },
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "revoked",
        "renewal_count": 1
    },
    "certificate_expiring.json": {
        "certificate_id": "cert_platinum_004",
        "subject_id": "agent.perfect.bot",
        "subject_type": "agent",
        "level": "PLATINUM",
        "issuer": "registry.openbase.main",
        "issued_at": "2025-10-07T12:00:00Z",
        "expires_at": "2026-07-14T12:00:00Z",
        "trust_snapshot": {
            "score": 0.92,
            "evidence_count": 520
        },
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "expiring",
        "renewal_count": 3
    }
}
for filename, data in examples.items():
    with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[4/4] Examples done')
