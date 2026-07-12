import os, json

base = r'D:\OpenBase'
conf_dir = os.path.join(base, 'conformance', 'replay')
fixtures_dir = os.path.join(conf_dir, 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

# --- Fixtures ---
fixtures = {
    "valid_structural_replay.json": {
        "replay_id": "rpl_001",
        "execution_id": "exec_demo_001",
        "fidelity": "STRUCTURAL",
        "evidence_count": 3,
        "chain_root": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "chain_tail": "f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8f9e0a1b2c3d4e5f6a7b8",
        "status": "completed",
        "events": ["evid_a1b2c3d4e5f6", "evid_f7e8d9c0b1a2"],
        "created": "2026-07-07T12:05:00Z",
        "completed_at": "2026-07-07T12:05:01Z",
        "summary": {"hash_chain_valid": True}
    },
    "valid_logical_replay.json": {
        "replay_id": "rpl_002",
        "execution_id": "exec_demo_001",
        "fidelity": "LOGICAL",
        "evidence_count": 3,
        "chain_root": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "status": "completed",
        "events": ["evid_a1b2c3d4e5f6", "evid_f7e8d9c0b1a2"],
        "created": "2026-07-07T12:06:00Z",
        "completed_at": "2026-07-07T12:06:02Z",
        "summary": {"hash_chain_valid": True, "causal_order_valid": True}
    },
    "failed_replay.json": {
        "replay_id": "rpl_003",
        "execution_id": "exec_broken_001",
        "fidelity": "STRUCTURAL",
        "evidence_count": 1,
        "chain_root": "deadbeef00000000000000000000000000000000000000000000000000000000",
        "status": "failed",
        "error_code": "E002",
        "events": ["evid_broken_1"],
        "created": "2026-07-07T12:07:00Z",
        "completed_at": "2026-07-07T12:07:01Z",
        "summary": {"hash_chain_valid": False}
    },
    "pending_replay.json": {
        "replay_id": "rpl_004",
        "execution_id": "exec_pending_001",
        "fidelity": "EXACT",
        "evidence_count": 5,
        "chain_root": "0000000000000000000000000000000000000000000000000000000000000000",
        "status": "pending",
        "events": [],
        "created": "2026-07-07T12:08:00Z"
    }
}
for filename, data in fixtures.items():
    with open(os.path.join(fixtures_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[1/2] Fixtures done')

# --- Conformance Test ---
test_code = '''"""
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
'''
with open(os.path.join(conf_dir, 'test_replay_schema.py'), 'w', encoding='utf-8') as f:
    f.write(test_code)
print('[2/2] Conformance test written')
