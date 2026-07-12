"""
OpenBase Conformance Test Suite
Event Schema Validation
Version: 1.0
"""

import json
import os
import pytest
from jsonschema import validate, ValidationError


# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, "..", "..", "openbase-spec", "event")
SCHEMA_PATH = os.path.join(SPEC_DIR, "event.schema.json")
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")


# --- Helpers ---
def load_schema():
    """Load the OBS event schema."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_fixture(filename):
    """Load a test fixture."""
    with open(os.path.join(FIXTURES_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


# --- Fixtures ---
@pytest.fixture
def schema():
    return load_schema()


@pytest.fixture
def valid_agent_event():
    return load_fixture("valid_agent_event.json")


# --- Tests ---
class TestEventSchemaValidation:
    """Test OBS event schema validation."""

    def test_schema_loads(self, schema):
        """Schema file should be valid JSON."""
        assert schema is not None
        assert schema["title"] == "OpenBase Event (OBS v1.0)"
        assert schema["type"] == "object"

    def test_valid_event_passes(self, schema, valid_agent_event):
        """A valid event should pass schema validation."""
        try:
            validate(instance=valid_agent_event, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Valid event failed validation: {e}")

    def test_missing_required_field_fails(self, schema, valid_agent_event):
        """Event missing a required field should fail validation."""
        invalid_event = valid_agent_event.copy()
        del invalid_event["event_id"]
        with pytest.raises(ValidationError):
            validate(instance=invalid_event, schema=schema)

    def test_invalid_event_type_fails(self, schema, valid_agent_event):
        """Event with an unregistered event_type should fail validation."""
        invalid_event = valid_agent_event.copy()
        invalid_event["event_type"] = "INVALID_TYPE_XYZ"
        with pytest.raises(ValidationError):
            validate(instance=invalid_event, schema=schema)

    def test_invalid_actor_type_fails(self, schema, valid_agent_event):
        """Event with an invalid actor type should fail validation."""
        invalid_event = valid_agent_event.copy()
        invalid_event["actor"]["type"] = "invalid_actor_type"
        with pytest.raises(ValidationError):
            validate(instance=invalid_event, schema=schema)

    def test_all_registered_event_types(self, schema):
        """All registered event types should be in the schema enum."""
        import yaml
        registry_path = os.path.join(SPEC_DIR, "event-types.yaml")
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)

        # Collect all registered types
        registered_types = []
        for category in registry["events"].values():
            registered_types.extend(category["types"])

        schema_types = schema["properties"]["event_type"]["enum"]
        
        for event_type in registered_types:
            assert event_type in schema_types, \
                f"Event type '{event_type}' in registry but not in schema enum"


class TestEventFixtures:
    """Test that all fixtures are valid."""

    def test_agent_start_fixture(self, schema):
        """AGENT_STARTED fixture should be valid."""
        event = load_fixture("valid_agent_event.json")
        validate(instance=event, schema=schema)

    def test_fixture_has_required_actor_fields(self, valid_agent_event):
        """Fixture actor should have id and type."""
        assert "id" in valid_agent_event["actor"]
        assert "type" in valid_agent_event["actor"]
        assert valid_agent_event["actor"]["type"] in ["agent", "tool", "human", "system"]

    def test_fixture_timestamp_is_iso8601(self, valid_agent_event):
        """Fixture timestamp should be ISO 8601 format."""
        from datetime import datetime
        try:
            datetime.fromisoformat(valid_agent_event["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            pytest.fail("Timestamp is not valid ISO 8601")


# --- Run ---
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
