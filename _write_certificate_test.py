import os, json

base = r'D:\OpenBase'
conf_dir = os.path.join(base, 'conformance', 'certificate')
fixtures_dir = os.path.join(conf_dir, 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

# --- Fixtures ---
fixtures = {
    "certificate_active_gold.json": {
        "certificate_id": "cert_gold_001",
        "subject_id": "runtime.openclaw.0.1.0",
        "subject_type": "runtime",
        "level": "GOLD",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-07-07T12:00:00Z",
        "expires_at": "2026-10-07T12:00:00Z",
        "trust_snapshot": {"score": 0.85, "evidence_count": 150},
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "active",
        "renewal_count": 2
    },
    "certificate_active_silver.json": {
        "certificate_id": "cert_silver_002",
        "subject_id": "agent.newcomer.bot",
        "subject_type": "agent",
        "level": "SILVER",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-07-01T00:00:00Z",
        "expires_at": "2026-10-01T00:00:00Z",
        "trust_snapshot": {"score": 0.55, "evidence_count": 60},
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
        "revocation_reason": "Trust score below threshold",
        "trust_snapshot": {"score": 0.15, "evidence_count": 3},
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
        "trust_snapshot": {"score": 0.92, "evidence_count": 520},
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "expiring",
        "renewal_count": 3
    },
    "certificate_model.json": {
        "certificate_id": "cert_model_005",
        "subject_id": "model.anthropic.claude-sonnet-4",
        "subject_type": "model",
        "level": "GOLD",
        "issuer": "registry.openbase.main",
        "issued_at": "2026-07-07T12:00:00Z",
        "expires_at": "2026-10-07T12:00:00Z",
        "trust_snapshot": {"score": 0.78, "evidence_count": 200},
        "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
        "status": "active",
        "renewal_count": 1
    }
}
for filename, data in fixtures.items():
    with open(os.path.join(fixtures_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[1/2] Fixtures done')

# --- Conformance Test ---
test_code = '''"""
OpenBase Conformance Test Suite
Certificate Schema Validation v1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "certificate")
SCHEMA_PATH = os.path.join(SPEC_DIR, "certificate.schema.json")
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")
EXAMPLES_DIR = os.path.join(SPEC_DIR, "examples")


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def schema():
    return load_schema()


@pytest.fixture
def cert_gold():
    return load_json(os.path.join(FIXTURES_DIR, "certificate_active_gold.json"))


@pytest.fixture
def cert_silver():
    return load_json(os.path.join(FIXTURES_DIR, "certificate_active_silver.json"))


@pytest.fixture
def cert_revoked():
    return load_json(os.path.join(FIXTURES_DIR, "certificate_revoked.json"))


@pytest.fixture
def cert_expiring():
    return load_json(os.path.join(FIXTURES_DIR, "certificate_expiring.json"))


@pytest.fixture
def cert_model():
    return load_json(os.path.join(FIXTURES_DIR, "certificate_model.json"))


class TestCertificateSchemaValidation:

    def test_schema_loads(self, schema):
        assert schema["title"] == "OpenBase Certificate v1.0"

    def test_gold_valid(self, schema, cert_gold):
        validate(instance=cert_gold, schema=schema)

    def test_silver_valid(self, schema, cert_silver):
        validate(instance=cert_silver, schema=schema)

    def test_revoked_valid(self, schema, cert_revoked):
        validate(instance=cert_revoked, schema=schema)

    def test_expiring_valid(self, schema, cert_expiring):
        validate(instance=cert_expiring, schema=schema)

    def test_model_valid(self, schema, cert_model):
        validate(instance=cert_model, schema=schema)

    def test_all_levels(self, schema):
        for level in ["BRONZE", "SILVER", "GOLD", "PLATINUM"]:
            cert = {
                "certificate_id": f"cert_test_{level}",
                "subject_id": "agent.test.bot",
                "subject_type": "agent",
                "level": level,
                "issuer": "registry.openbase.main",
                "issued_at": "2026-07-07T12:00:00Z",
                "expires_at": "2026-10-07T12:00:00Z",
                "trust_snapshot": {"score": 0.5, "evidence_count": 10},
                "signature": "ed25519:dGVzdF9jZXJ0X3NpZ25hdHVyZV9kYXRhX2Zvcl9kZW1vbnN0cmF0aW9u",
                "status": "active",
                "renewal_count": 0
            }
            validate(instance=cert, schema=schema)

    def test_missing_certificate_id_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        del invalid["certificate_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_level_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        invalid["level"] = "DIAMOND"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_status_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        invalid["status"] = "suspended"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_signature_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        invalid["signature"] = "bad-signature"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_trust_snapshot_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        del invalid["trust_snapshot"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_revoked_has_reason(self, cert_revoked):
        assert "revocation_reason" in cert_revoked
        assert len(cert_revoked["revocation_reason"]) > 0

    def test_expiring_status(self, cert_expiring):
        assert cert_expiring["status"] == "expiring"

    def test_negative_renewal_fails(self, schema, cert_gold):
        invalid = cert_gold.copy()
        invalid["renewal_count"] = -1
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_trust_snapshot_has_required(self, cert_gold):
        snap = cert_gold["trust_snapshot"]
        assert "score" in snap
        assert "evidence_count" in snap
        assert 0.0 <= snap["score"] <= 1.0


class TestCertificateExamples:

    def test_gold_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "certificate_gold.json"))
        validate(instance=example, schema=schema)

    def test_silver_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "certificate_silver.json"))
        validate(instance=example, schema=schema)

    def test_revoked_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "certificate_revoked.json"))
        validate(instance=example, schema=schema)

    def test_expiring_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "certificate_expiring.json"))
        validate(instance=example, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
with open(os.path.join(conf_dir, 'test_certificate_schema.py'), 'w', encoding='utf-8') as f:
    f.write(test_code)
print('[2/2] Conformance test written')
