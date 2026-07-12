"""
OpenBase Conformance Test Suite
Evidence Schema Validation v2.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "evidence")
SCHEMA_PATH = os.path.join(SPEC_DIR, "evidence.schema.json")
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
def genesis_evidence():
    return load_json(os.path.join(FIXTURES_DIR, "genesis_evidence.json"))


@pytest.fixture
def chained_evidence():
    return load_json(os.path.join(FIXTURES_DIR, "chained_evidence.json"))


class TestEvidenceSchemaValidation:

    def test_schema_loads(self, schema):
        assert schema["title"] == "OpenBase Evidence v2.0"
        assert "2.0" in schema["properties"]["spec_version"]["enum"]

    def test_genesis_valid(self, schema, genesis_evidence):
        validate(instance=genesis_evidence, schema=schema)

    def test_chained_valid(self, schema, chained_evidence):
        validate(instance=chained_evidence, schema=schema)

    def test_missing_event_id_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        del invalid["event_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_spec_version_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        invalid["spec_version"] = "1.0"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_hash_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        del invalid["hash"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_hash_format_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        invalid["hash"] = "bad-hash"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_signature_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        del invalid["signature"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_signature_format_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        invalid["signature"] = "bad-sig"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_public_key_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        del invalid["public_key"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_causal_fails(self, schema, genesis_evidence):
        invalid = genesis_evidence.copy()
        del invalid["causal"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_genesis_has_null_parent(self, genesis_evidence):
        assert genesis_evidence["causal"]["parent_id"] is None

    def test_chained_has_parent(self, chained_evidence):
        assert chained_evidence["causal"]["parent_id"] is not None

    def test_vector_clock_monotonic(self, genesis_evidence, chained_evidence):
        vc1 = genesis_evidence["causal"]["vector_clock"]
        vc2 = chained_evidence["causal"]["vector_clock"]
        for actor in vc1:
            if actor in vc2:
                assert vc2[actor] >= vc1[actor]


class TestEvidenceExamples:

    def test_genesis_example_valid(self, schema):
        evidence = load_json(os.path.join(EXAMPLES_DIR, "genesis_evidence.json"))
        validate(instance=evidence, schema=schema)

    def test_chained_example_valid(self, schema):
        evidence = load_json(os.path.join(EXAMPLES_DIR, "chained_evidence.json"))
        validate(instance=evidence, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
