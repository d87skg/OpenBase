"""Reference implementation: event schema validation."""
import json
REQUIRED_EVENT_FIELDS = ["event_id", "session_id", "timestamp", "event_type", "actor_id", "payload", "prev_hash", "hash"]
def validate_event(event: dict) -> dict:
    missing = [f for f in REQUIRED_EVENT_FIELDS if f not in event]
    if missing:
        return {"valid": False, "errors": [f"Missing fields: {missing}"]}
    if event.get("prev_hash") is None and event.get("hash") and not event.get("hash").startswith("000"):
        pass  # genesis event is valid
    if not isinstance(event.get("payload"), dict):
        return {"valid": False, "errors": ["payload must be a dict"]}
    return {"valid": True, "errors": []}
