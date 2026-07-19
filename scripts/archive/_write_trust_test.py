import os, json

base = r'D:\OpenBase'
conf_dir = os.path.join(base, 'conformance', 'trust')
fixtures_dir = os.path.join(conf_dir, 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

# --- Fixtures ---
fixtures = {
    "trust_high_runtime.json": {
        "subject_id": "runtime.openclaw.0.1.0",
        "subject_type": "runtime",
        "score": 0.85,
        "confidence": 0.90,
        "dimensions": {
            "evidence_volume": 0.90,
            "evidence_quality": 0.95,
            "consistency": 0.88,
            "recency": 0.80,
            "peer_attestation": 0.75
        },
        "evidence_count": 150,
        "last_updated": "2026-07-07T12:00:00Z",
        "previous_score": 0.83,
        "trend": "rising"
    },
    "trust_new_agent.json": {
        "subject_id": "agent.newcomer.bot",
        "subject_type": "agent",
        "score": 0.50,
        "confidence": 0.30,
        "dimensions": {
            "evidence_volume": 0.50,
            "evidence_quality": 0.50,
            "consistency": 0.50,
            "recency": 0.50,
            "peer_attestation": 0.50
        },
        "evidence_count": 5,
        "last_updated": "2026-07-07T10:00:00Z",
        "trend": "stable"
    },
    "trust_boundary_zero.json": {
        "subject_id": "agent.zero.bot",
        "subject_type": "agent",
        "score": 0.0,
        "confidence": 1.0,
        "dimensions": {
            "evidence_volume": 0.0,
            "evidence_quality": 0.0,
            "consistency": 0.0,
            "recency": 0.0,
            "peer_attestation": 0.0
        },
        "evidence_count": 0,
        "last_updated": "2026-07-07T00:00:00Z",
        "trend": "stable"
    },
    "trust_boundary_one.json": {
        "subject_id": "agent.perfect.bot",
        "subject_type": "agent",
        "score": 1.0,
        "confidence": 0.95,
        "dimensions": {
            "evidence_volume": 1.0,
            "evidence_quality": 1.0,
            "consistency": 1.0,
            "recency": 1.0,
            "peer_attestation": 1.0
        },
        "evidence_count": 1000,
        "last_updated": "2026-07-07T12:00:00Z",
        "previous_score": 0.99,
        "trend": "rising"
    },
    "trust_with_certificates.json": {
        "subject_id": "agent.certified.bot",
        "subject_type": "agent",
        "score": 0.72,
        "dimensions": {
            "evidence_volume": 0.70,
            "evidence_quality": 0.80,
            "consistency": 0.75,
            "recency": 0.60,
            "peer_attestation": 0.85
        },
        "evidence_count": 80,
        "certificates": ["cert_gold_001", "cert_silver_002"],
        "last_updated": "2026-07-07T11:30:00Z",
        "trend": "rising"
    }
}
for filename, data in fixtures.items():
    with open(os.path.join(fixtures_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[1/2] Fixtures done')

# --- Conformance Test ---
test_code = '''"""
OpenBase Conformance Test Suite
Trust Schema Validation v1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "trust")
SCHEMA_PATH = os.path.join(SPEC_DIR, "trust.schema.json")
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
def trust_high():
    return load_json(os.path.join(FIXTURES_DIR, "trust_high_runtime.json"))


@pytest.fixture
def trust_new():
    return load_json(os.path.join(FIXTURES_DIR, "trust_new_agent.json"))


@pytest.fixture
def trust_zero():
    return load_json(os.path.join(FIXTURES_DIR, "trust_boundary_zero.json"))


@pytest.fixture
def trust_one():
    return load_json(os.path.join(FIXTURES_DIR, "trust_boundary_one.json"))


@pytest.fixture
def trust_certified():
    return load_json(os.path.join(FIXTURES_DIR, "trust_with_certificates.json"))


class TestTrustSchemaValidation:

    def test_schema_loads(self, schema):
        assert schema["title"] == "OpenBase Trust v1.0"

    def test_high_trust_valid(self, schema, trust_high):
        validate(instance=trust_high, schema=schema)

    def test_new_agent_valid(self, schema, trust_new):
        validate(instance=trust_new, schema=schema)

    def test_zero_score_valid(self, schema, trust_zero):
        validate(instance=trust_zero, schema=schema)

    def test_one_score_valid(self, schema, trust_one):
        validate(instance=trust_one, schema=schema)

    def test_certified_valid(self, schema, trust_certified):
        validate(instance=trust_certified, schema=schema)

    def test_all_subject_types(self, schema):
        for st in ["runtime", "agent", "model", "tool"]:
            trust = {
                "subject_id": f"{st}.test.entity",
                "subject_type": st,
                "score": 0.5,
                "dimensions": {
                    "evidence_volume": 0.5, "evidence_quality": 0.5,
                    "consistency": 0.5, "recency": 0.5, "peer_attestation": 0.5
                },
                "evidence_count": 10,
                "last_updated": "2026-07-07T12:00:00Z"
            }
            validate(instance=trust, schema=schema)

    def test_score_below_zero_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        invalid["score"] = -0.1
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_score_above_one_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        invalid["score"] = 1.1
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_subject_id_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        del invalid["subject_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_subject_type_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        invalid["subject_type"] = "invalid_type"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_trend_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        invalid["trend"] = "crashing"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_negative_evidence_count_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        invalid["evidence_count"] = -5
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_dimensions_fails(self, schema, trust_new):
        invalid = trust_new.copy()
        del invalid["dimensions"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_zero_has_zero_score(self, trust_zero):
        assert trust_zero["score"] == 0.0

    def test_one_has_one_score(self, trust_one):
        assert trust_one["score"] == 1.0

    def test_certified_has_certificates(self, trust_certified):
        assert len(trust_certified["certificates"]) >= 1


class TestTrustExamples:

    def test_high_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "trust_high.json"))
        validate(instance=example, schema=schema)

    def test_moderate_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "trust_moderate.json"))
        validate(instance=example, schema=schema)

    def test_low_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "trust_low.json"))
        validate(instance=example, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
with open(os.path.join(conf_dir, 'test_trust_schema.py'), 'w', encoding='utf-8') as f:
    f.write(test_code)
print('[2/2] Conformance test written')
