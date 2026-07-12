"""
OpenBase Conformance Test Suite
Identity Schema Validation v1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "identity")
SCHEMA_PATH = os.path.join(SPEC_DIR, "identity.schema.json")
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
def valid_agent():
    return load_json(os.path.join(FIXTURES_DIR, "valid_agent_identity.json"))


@pytest.fixture
def valid_runtime():
    return load_json(os.path.join(FIXTURES_DIR, "valid_runtime_identity.json"))


@pytest.fixture
def deprecated():
    return load_json(os.path.join(FIXTURES_DIR, "deprecated_identity.json"))


class TestIdentitySchemaValidation:

    def test_schema_loads(self, schema):
        assert schema["title"] == "OpenBase Identity v1.0"

    def test_valid_agent(self, schema, valid_agent):
        validate(instance=valid_agent, schema=schema)

    def test_valid_runtime(self, schema, valid_runtime):
        validate(instance=valid_runtime, schema=schema)

    def test_deprecated_status(self, schema, deprecated):
        validate(instance=deprecated, schema=schema)

    def test_missing_id_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        del invalid["id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_type_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        invalid["type"] = "invalid_type"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_status_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        invalid["status"] = "unknown_status"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_id_format_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        invalid["id"] = "INVALID_FORMAT"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_public_key_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        del invalid["public_key"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_invalid_public_key_format_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        invalid["public_key"] = "not-a-key"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_missing_created_fails(self, schema, valid_agent):
        invalid = valid_agent.copy()
        del invalid["created"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)

    def test_all_actor_types_valid(self, schema):
        for actor_type in ["agent", "runtime", "model", "tool", "human", "system"]:
            identity = {
                "id": f"{actor_type}.test.entity",
                "type": actor_type,
                "display_name": f"Test {actor_type}",
                "public_key": "ed25519:dGVzdF9hbGxfdHlwZXNfcHVibGljX2tleV9kYXRhX3Rlc3Q=",
                "status": "active",
                "created": "2026-07-07T00:00:00Z"
            }
            validate(instance=identity, schema=schema)

    def test_deprecated_has_date(self, deprecated):
        assert "deprecated_at" in deprecated


class TestIdentityExamples:

    def test_agent_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "agent_identity.json"))
        validate(instance=example, schema=schema)

    def test_runtime_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "runtime_identity.json"))
        validate(instance=example, schema=schema)

    def test_model_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "model_identity.json"))
        validate(instance=example, schema=schema)

    def test_tool_example(self, schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "tool_identity.json"))
        validate(instance=example, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
