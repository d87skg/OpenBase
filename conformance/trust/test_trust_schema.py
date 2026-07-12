"""
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
