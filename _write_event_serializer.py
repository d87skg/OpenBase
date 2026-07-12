import os

code = '''"""
EventSerializer — serialize/deserialize OBS Events with RFC 8785 canonical JSON.
"""

import json
from typing import List
from .models import Event


class EventSerializer:
    """Handles JSON serialization of OBS Events."""

    @staticmethod
    def to_json(event: Event, indent: int = None) -> str:
        """Serialize event to JSON string."""
        return event.to_json(indent=indent)

    @staticmethod
    def from_json(json_str: str) -> Event:
        """Deserialize event from JSON string."""
        return Event.from_dict(json.loads(json_str))

    @staticmethod
    def to_canonical(event: Event) -> bytes:
        """Serialize to RFC 8785 canonical JSON bytes.
        
        Canonical JSON rules:
        - No whitespace
        - Object keys sorted
        - UTF-8 encoded
        - No trailing commas
        """
        d = event.to_dict()
        return json.dumps(d, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

    @staticmethod
    def serialize_chain(events: List[Event], indent: int = None) -> str:
        """Serialize a list of events as a JSON array."""
        return json.dumps([e.to_dict() for e in events], indent=indent, ensure_ascii=False)

    @staticmethod
    def deserialize_chain(json_str: str) -> List[Event]:
        """Deserialize a JSON array of events."""
        data = json.loads(json_str)
        return [Event.from_dict(item) for item in data]
'''

path = r'D:\OpenBase\openbase-core\event\serializer.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('serializer.py written')
