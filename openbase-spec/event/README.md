# OpenBase Event Specification (OBS)

This directory contains the OpenBase Event Specification — the canonical event format for AI Agent execution.

## Contents

| File | Description |
|:---|:---|
| OBS_SPEC_v1.0.md | Full specification document |
| event.schema.json | JSON Schema for validation |
| event-types.yaml | Registry of canonical event types |
| examples/ | Example events for each type |

## Quick Start

`ash
# Validate an event against the schema
pip install jsonschema
python -c "
import json
from jsonschema import validate
schema = json.load(open('event.schema.json'))
event = json.load(open('examples/agent_start.json'))
validate(event, schema)
print('Valid OBS event')
"
Version
Current version: 1.0 (Draft)
