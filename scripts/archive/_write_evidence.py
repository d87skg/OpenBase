import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'evidence')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- JSON Schema ---
schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/evidence/v2.0/evidence.schema.json",
    "title": "OpenBase Evidence v2.0",
    "description": "Signed snapshot of an OBS event with hash chain and signature",
    "type": "object",
    "required": ["evidence_id","spec_version","event_id","execution_id","agent_id","event_type","timestamp","causal","payload","hash","signature","public_key"],
    "properties": {
        "evidence_id": {"type": "string"},
        "spec_version": {"type": "string", "enum": ["2.0"]},
        "event_id": {"type": "string"},
        "execution_id": {"type": "string"},
        "agent_id": {"type": "string"},
        "event_type": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "causal": {
            "type": "object",
            "required": ["parent_id", "vector_clock"],
            "properties": {
                "parent_id": {"type": ["string", "null"]},
                "vector_clock": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 1}}
            }
        },
        "payload": {"type": "object"},
        "hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "signature": {"type": "string", "pattern": "^ed25519:[A-Za-z0-9+/=]+$"},
        "public_key": {"type": "string", "pattern": "^ed25519:[A-Za-z0-9+/=]+$"}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'evidence.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
print('[1/5] Schema done')

# --- README ---
readme = """# OpenBase Evidence v2.0

Evidence v2.0 redefines Evidence as a signed snapshot of an OBS Event.

## Contents

| File | Description |
|:---|:---|
| OBS_EVIDENCE_SPEC_v2.0.md | Full specification |
| evidence.schema.json | JSON Schema |
| examples/ | Example evidence objects |

## Quick Start

`ash
pip install jsonschema
python -c "import json; from jsonschema import validate; schema = json.load(open('evidence.schema.json')); evidence = json.load(open('examples/genesis_evidence.json')); validate(evidence, schema); print('Valid')"
"""
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
f.write(readme)
print('[2/5] README done')

--- Genesis example ---
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
with open(os.path.join(examples_dir, 'genesis_evidence.json'), 'w', encoding='utf-8') as f:
json.dump(genesis, f, indent=2)
print('[3/5] Genesis example done')

--- Chained example ---
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
with open(os.path.join(examples_dir, 'chained_evidence.json'), 'w', encoding='utf-8') as f:
json.dump(chained, f, indent=2)
print('[4/5] Chained example done')

print('[5/5] All Evidence spec files written!')
