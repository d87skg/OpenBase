import os, json

base = r'D:\OpenBase'
conf_dir = os.path.join(base, 'conformance', 'evidence')
fixtures_dir = os.path.join(conf_dir, 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

# --- Fixtures ---
genesis = {
    "evidence_id": "evid_a1b2c3d4e5f6",
    "spec_version": "2.0",
    "event_id": "evt_a1b2c3d4",
    "execution_id": "exec_demo_001",
    "agent_id": "agent.openclaw.demo",
    "event_type": "AGENT_STARTED",
    "timestamp": "2026-07-07T12:00:00Z",
    "causal": {
        "parent_id": None,
        "vector_clock": {"agent.openclaw.demo": 1}
    },
    "payload": {"task": "hello world"},
    "hash": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
    "signature": "ed25519:dGVzdF9zaWduYXR1cmVfZGF0YV9mb3JfZGVtb25zdHJhdGlvbg==",
    "public_key": "ed25519:dGVzdF9wdWJsaWNfa2V5X2RhdGFfZm9yX2RlbW9uc3RyYXRpb24="
}
with open(os.path.join(fixtures_dir, 'genesis_evidence.json'), 'w', encoding='utf-8') as f:
    json.dump(genesis, f, indent=2)

chained = {
    "evidence_id": "evid_f7e8d9c0b1a2",
    "spec_version": "2.0",
    "event_id": "evt_e5f6g7h8",
    "execution_id": "exec_demo_001",
    "agent_id": "agent.openclaw.demo",
    "event_type": "TOOL_CALL",
    "timestamp": "2026-07-07T12:00:05Z",
    "causal": {
        "parent_id": "evid_a1b2c3d4e5f6",
        "vector_clock": {"agent.openclaw.demo": 2}
    },
    "payload": {
        "tool_name": "read_file",
        "tool_input": {"path": "/workspace/README.md"}
    },
    "hash": "f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8f9e0a1b2c3d4e5f6a7b8",
    "signature": "ed25519:dGVzdF9zaWduYXR1cmVfZGF0YV9mb3JfZGVtb25zdHJhdGlvbg==",
    "public_key": "ed25519:dGVzdF9wdWJsaWNfa2V5X2RhdGFfZm9yX2RlbW9uc3RyYXRpb24="
}
with open(os.path.join(fixtures_dir, 'chained_evidence.json'), 'w', encoding='utf-8') as f:
    json.dump(chained, f, indent=2)
print('[1/2] Fixtures done')

# --- Conformance Test ---
test_code = '''"""
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
'''
with open(os.path.join(conf_dir, 'test_evidence_schema.py'), 'w', encoding='utf-8') as f:
    f.write(test_code)
print('[2/2] Conformance test written')
