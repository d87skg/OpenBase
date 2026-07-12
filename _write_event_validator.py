import os

code = '''"""
EventValidator — validates OBS Events against the JSON Schema.
"""

import json
import os
from typing import Dict, Any, List
from jsonschema import validate, ValidationError
from .models import Event


class EventValidator:
    """Validates OBS Events against the official schema."""

    def __init__(self, schema_path: str = None):
        if schema_path is None:
            schema_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "openbase-spec", "event", "event.schema.json"
            )
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def validate_event(self, event: Event) -> List[str]:
        """Validate an Event object. Returns list of errors (empty = valid)."""
        errors = []
        try:
            validate(instance=event.to_dict(), schema=self.schema)
        except ValidationError as e:
            errors.append(str(e))
        return errors

    def validate_dict(self, data: Dict[str, Any]) -> List[str]:
        """Validate a raw dict. Returns list of errors (empty = valid)."""
        errors = []
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            errors.append(str(e))
        return errors

    def is_valid(self, event: Event) -> bool:
        """Check if event is valid against schema."""
        return len(self.validate_event(event)) == 0

    def is_valid_dict(self, data: Dict[str, Any]) -> bool:
        """Check if dict is valid against schema."""
        return len(self.validate_dict(data)) == 0
'''

path = r'D:\OpenBase\openbase-core\event\validator.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('validator.py written')
