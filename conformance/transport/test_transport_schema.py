"""
OpenBase Conformance Test Suite
Transport Schema Validation v1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "transport")
ADAPTER_SCHEMA_PATH = os.path.join(SPEC_DIR, "adapter-config.schema.json")
SDK_SCHEMA_PATH = os.path.join(SPEC_DIR, "sdk-config.schema.json")
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")
EXAMPLES_DIR = os.path.join(SPEC_DIR, "examples")


def load_adapter_schema():
    with open(ADAPTER_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_sdk_schema():
    with open(SDK_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def adapter_schema():
    return load_adapter_schema()


@pytest.fixture
def sdk_schema():
    return load_sdk_schema()


@pytest.fixture
def adapter_rest():
    return load_json(os.path.join(FIXTURES_DIR, "adapter_rest_active.json"))


@pytest.fixture
def adapter_grpc():
    return load_json(os.path.join(FIXTURES_DIR, "adapter_grpc_connected.json"))


@pytest.fixture
def adapter_error():
    return load_json(os.path.join(FIXTURES_DIR, "adapter_error.json"))


@pytest.fixture
def sdk_traccia():
    return load_json(os.path.join(FIXTURES_DIR, "sdk_traccia.json"))


@pytest.fixture
def sdk_minimal():
    return load_json(os.path.join(FIXTURES_DIR, "sdk_minimal.json"))


class TestAdapterSchema:

    def test_schema_loads(self, adapter_schema):
        assert adapter_schema["title"] == "OpenBase Adapter Configuration v1.0"

    def test_rest_valid(self, adapter_schema, adapter_rest):
        validate(instance=adapter_rest, schema=adapter_schema)

    def test_grpc_valid(self, adapter_schema, adapter_grpc):
        validate(instance=adapter_grpc, schema=adapter_schema)

    def test_error_valid(self, adapter_schema, adapter_error):
        validate(instance=adapter_error, schema=adapter_schema)

    def test_all_protocols(self, adapter_schema):
        for proto in ["REST", "gRPC", "MCP", "WebSocket"]:
            cfg = {
                "adapter_id": f"adapter-test-{proto}",
                "runtime_name": "test-runtime",
                "target_protocol": proto,
                "endpoint": "https://test.openbase.dev",
                "status": "configured",
                "created": "2026-07-07T12:00:00Z"
            }
            validate(instance=cfg, schema=adapter_schema)

    def test_all_auth_types(self, adapter_schema):
        for auth_type in ["api_key", "ed25519", "mtls", "none"]:
            cfg = {
                "adapter_id": f"adapter-auth-{auth_type}",
                "runtime_name": "test-runtime",
                "target_protocol": "REST",
                "endpoint": "https://test.openbase.dev",
                "auth": {"type": auth_type},
                "status": "configured",
                "created": "2026-07-07T12:00:00Z"
            }
            validate(instance=cfg, schema=adapter_schema)

    def test_missing_adapter_id_fails(self, adapter_schema, adapter_rest):
        invalid = adapter_rest.copy()
        del invalid["adapter_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=adapter_schema)

    def test_invalid_protocol_fails(self, adapter_schema, adapter_rest):
        invalid = adapter_rest.copy()
        invalid["target_protocol"] = "FTP"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=adapter_schema)

    def test_invalid_status_fails(self, adapter_schema, adapter_rest):
        invalid = adapter_rest.copy()
        invalid["status"] = "unknown"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=adapter_schema)

    def test_invalid_auth_type_fails(self, adapter_schema, adapter_rest):
        invalid = adapter_rest.copy()
        invalid["auth"]["type"] = "password"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=adapter_schema)


class TestSDKSchema:

    def test_schema_loads(self, sdk_schema):
        assert sdk_schema["title"] == "OpenBase SDK Configuration v1.0"

    def test_traccia_valid(self, sdk_schema, sdk_traccia):
        validate(instance=sdk_traccia, schema=sdk_schema)

    def test_minimal_valid(self, sdk_schema, sdk_minimal):
        validate(instance=sdk_minimal, schema=sdk_schema)

    def test_all_sdk_names(self, sdk_schema):
        for name in ["traccia", "openbase-python", "openbase-js", "openbase-go"]:
            cfg = {
                "sdk_name": name,
                "sdk_version": "1.0.0",
                "openbase_endpoint": "https://registry.openbase.dev",
                "created": "2026-07-07T12:00:00Z"
            }
            validate(instance=cfg, schema=sdk_schema)

    def test_invalid_sdk_name_fails(self, sdk_schema, sdk_traccia):
        invalid = sdk_traccia.copy()
        invalid["sdk_name"] = "unknown-sdk"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=sdk_schema)

    def test_missing_endpoint_fails(self, sdk_schema, sdk_traccia):
        invalid = sdk_traccia.copy()
        del invalid["openbase_endpoint"]
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=sdk_schema)

    def test_invalid_log_level_fails(self, sdk_schema, sdk_traccia):
        invalid = sdk_traccia.copy()
        invalid["features"]["log_level"] = "verbose"
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=sdk_schema)


class TestTransportExamples:

    def test_adapter_rest_example(self, adapter_schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "adapter_config_rest.json"))
        validate(instance=example, schema=adapter_schema)

    def test_adapter_grpc_example(self, adapter_schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "adapter_config_grpc.json"))
        validate(instance=example, schema=adapter_schema)

    def test_sdk_traccia_example(self, sdk_schema):
        example = load_json(os.path.join(EXAMPLES_DIR, "sdk_config_traccia.json"))
        validate(instance=example, schema=sdk_schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
