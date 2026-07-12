# OpenBase Replay Specification v1.0

## Status
Core — immutable.

## Definition
Replay converts OpenBase Evidence into a human-readable timeline.

## Canonical Timeline Format
```json
{
  "timeline_id": "uuid",
  "session_id": "uuid",
  "generated_at": "ISO8601",
  "entries": [
    {
      "timestamp": "ISO8601",
      "event_id": "uuid",
      "event_type": "canonical_event_type",
      "title": "human-readable title",
      "summary": "human-readable summary",
      "actor_id": "string",
      "evidence_count": 0
    }
  ]
}
Renderer Output Formats
Text (default)

Markdown

JSON

Relationship to SDK
Replay is a Core capability. SDKs (Traccia, future SDKs) implement Renderers that consume Replay output.
