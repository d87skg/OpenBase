"""Reference implementation: replay output validation."""
REQUIRED_REPLAY_FIELDS = ["timeline_id", "session_id", "generated_at", "entries"]
REQUIRED_ENTRY_FIELDS = ["timestamp", "event_id", "event_type", "title", "actor_id", "evidence_count"]
def validate_replay(replay: dict) -> dict:
    missing = [f for f in REQUIRED_REPLAY_FIELDS if f not in replay]
    if missing:
        return {"valid": False, "errors": [f"Missing replay fields: {missing}"]}
    for i, entry in enumerate(replay.get("entries", [])):
        entry_missing = [f for f in REQUIRED_ENTRY_FIELDS if f not in entry]
        if entry_missing:
            return {"valid": False, "errors": [f"Entry[{i}] missing: {entry_missing}"]}
    return {"valid": True, "errors": []}
