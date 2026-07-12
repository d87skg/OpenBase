"""
OpenBase Conformance Test Suite
Replay Schema Validation v1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "replay")
SCHEMA_PATH = os.path.join(SPEC_DIR, "replay.schema.json")
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
def structural():
    return load_json(os.path.join(FIXTURES_DIR, "valid_structural_replay.json"))


@pytest.fixture
def logical():
    return load_json(os.path.join(FIXTURES_DIR, "valid_logical_replay.json"))


@pytest.fixture
def failed():
    return load_json(os.path.join(FIXTURES_DIR, "failed_replay.json"))


@pytest.fixture
def pending():
    return load_json(os.path.join(FIXTURES_DIR, "pending_replay.json"))


class TestReplaySchemaValidation:

    def test_schema_loads(self, schema):
        assert schema["title"] == "OpenBase Replay v1.0"

    def test_structural_valid(self, schema, structural):
        validate(instance=structural, schema=schema)

    def test_logical_valid(self, schema, logical):
        validate(instance=logical, schema=schema)

    def test_failed_valid(self, schema, failed):
        validate(instance=failed, schema=schema)

    def test_pending_valid(self, schema, pending):
        validate(instance=pending, schema=schema)

    def test_all_fidelity_levels(self, schema):
        for level in ["STRUCTURAL", "CAUSAL", "LOGICAL", "EXACT"]:
            manifest = {
                "replay_id": f"rpl_test_{level}",
                "execution_id": "exec_test",
                "fidelity": level,
                "evidence_count": 1,
                "chain_root": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
                "status": "completed",
                "events": ["evid_test"],
                "created": "2026-07-07T12:00:00Z",
                "completed_at": "2026-07-07T12:00:01Z"
            }
            validate(instance=manifest, schema=schema)

    def test_missing_replay_id_fails(self, schema, structural):
        invalid = structural.copy()
        del invalid["replay_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_fidelity_fails(self, schema, structural):
        invalid = structural.copy()
        invalid["fidelity"] = "INVALID_LEVEL"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_status_fails(self, schema, structural):
        invalid = structural.copy()
        invalid["status"] = "unknown"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_negative_evidence_count_fails(self, schema, structural):
        invalid = structural.copy()
        invalid["evidence_count"] = -1
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_hash_format_fails(self, schema, structural):
        invalid = structural.copy()
        invalid["chain_root"] = "not-a-hash"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_failed_has_error_code(self, failed):
        assert "error_code" in failed
        assert failed["error_code"] == "E002"

    def test_pending_no_completed_at(self, pending):
        assert "completed_at" not in pending


class TestReplayExamples:

    def test_structural_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "replay_manifest_structural.json"))
        validate(instance=example, schema=schema)

    def test_logical_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "replay_manifest_logical.json"))
        validate(instance=example, schema=schema)

    def test_failed_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "replay_manifest_failed.json"))
        validate(instance=example, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
