import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'replay')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Replay Specification ---
spec = '# OpenBase Replay Specification v1.0\n\n## Version\n**1.0**\n\n## Status\n**Draft**\n\n---\n\n## 1. Abstract\n\nThe Replay Layer defines how to reconstruct a complete execution trace from an Evidence Chain. Replay is the mechanism that transforms immutable evidence records back into a verifiable timeline of Agent behavior.\n\n## 2. Replay Model\n\n### 2.1 Core Principle\n\nGiven an ordered sequence of Evidence objects linked by hash chain, Replay reconstructs:\n- The exact sequence of events\n- State transitions at each step\n- Causal relationships between events\n- Final execution outcome\n\n### 2.2 Fidelity Levels\n\n| Level | Name | Description |\n|:---|:---|:---|\n| 0 | STRUCTURAL | Validate hash chain integrity only |\n| 1 | CAUSAL | Validate causal ordering via vector clocks |\n| 2 | LOGICAL | Replay state transitions without side effects |\n| 3 | EXACT | Full bit-exact replay including all outputs |\n\n### 2.3 Replay Process\n\n1. Load evidence chain from storage\n2. Verify hash chain integrity (STRUCTURAL)\n3. Verify causal ordering (CAUSAL)\n4. Sort events by vector clock\n5. Apply state transitions sequentially (LOGICAL)\n6. Optionally re-execute for exact match (EXACT)\n\n## 3. Replay Package Format\n\nA Replay Package bundles all evidence needed:\n\n`\nreplay_package/\n  manifest.json\n  chain/\n    evid_0001.json\n    evid_0002.json\n    ...\n  summary.json\n`\n\n## 4. Verification\n\nReplay MUST verify:\n- Hash chain: each hash matches previous\n- Signatures: all Ed25519 signatures valid\n- Vector clocks: monotonically increasing\n- State consistency: no impossible transitions\n\n## 5. Error Codes\n\n| Code | Description |\n|:---|:---|\n| E001 | Evidence chain incomplete |\n| E002 | Hash mismatch at position N |\n| E003 | Signature verification failed |\n| E004 | Vector clock violation |\n| E005 | Invalid state transition |\n| E006 | Missing genesis evidence |\n\n## 6. References\n\n- Evidence v2.0 (hash chain, signatures)\n- OBS v1.0 (event types, state transitions)\n- Vector Clocks (Lamport, Fidge, Mattern)\n'
with open(os.path.join(spec_dir, 'REPLAY_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
    f.write(spec)
print('[1/4] Spec done')

# --- JSON Schema ---
schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/replay/v1.0/replay.schema.json",
    "title": "OpenBase Replay v1.0",
    "description": "Replay package manifest for execution reconstruction",
    "type": "object",
    "required": ["replay_id", "execution_id", "fidelity", "evidence_count", "chain_root", "status", "created"],
    "properties": {
        "replay_id": {"type": "string"},
        "execution_id": {"type": "string"},
        "fidelity": {"type": "string", "enum": ["STRUCTURAL", "CAUSAL", "LOGICAL", "EXACT"]},
        "evidence_count": {"type": "integer", "minimum": 1},
        "chain_root": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "chain_tail": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "status": {"type": "string", "enum": ["pending", "running", "completed", "failed"]},
        "error_code": {"type": "string"},
        "events": {
            "type": "array",
            "items": {"type": "string"}
        },
        "created": {"type": "string", "format": "date-time"},
        "completed_at": {"type": "string", "format": "date-time"},
        "summary": {"type": "object"}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'replay.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
print('[2/4] Schema done')

# --- README ---
readme = '# OpenBase Replay v1.0\n\nDefines the replay protocol for reconstructing Agent execution from evidence chains.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| REPLAY_SPEC_v1.0.md | Full specification |\n| replay.schema.json | JSON Schema |\n| examples/ | Example replay manifests |\n'
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('[3/4] README done')

# --- Examples ---
examples = {
    "replay_manifest_structural.json": {
        "replay_id": "rpl_001",
        "execution_id": "exec_demo_001",
        "fidelity": "STRUCTURAL",
        "evidence_count": 3,
        "chain_root": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "chain_tail": "f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8f9e0a1b2c3d4e5f6a7b8",
        "status": "completed",
        "events": ["evid_a1b2c3d4e5f6", "evid_f7e8d9c0b1a2", "evid_x1y2z3w4v5u6"],
        "created": "2026-07-07T12:05:00Z",
        "completed_at": "2026-07-07T12:05:01Z",
        "summary": {"hash_chain_valid": True, "signatures_valid": True}
    },
    "replay_manifest_logical.json": {
        "replay_id": "rpl_002",
        "execution_id": "exec_demo_001",
        "fidelity": "LOGICAL",
        "evidence_count": 3,
        "chain_root": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "status": "completed",
        "events": ["evid_a1b2c3d4e5f6", "evid_f7e8d9c0b1a2", "evid_x1y2z3w4v5u6"],
        "created": "2026-07-07T12:06:00Z",
        "completed_at": "2026-07-07T12:06:02Z",
        "summary": {
            "hash_chain_valid": True,
            "signatures_valid": True,
            "causal_order_valid": True,
            "final_state": {"agent_status": "finished", "tool_results": 1}
        }
    },
    "replay_manifest_failed.json": {
        "replay_id": "rpl_003",
        "execution_id": "exec_broken_001",
        "fidelity": "STRUCTURAL",
        "evidence_count": 2,
        "chain_root": "deadbeef00000000000000000000000000000000000000000000000000000000",
        "status": "failed",
        "error_code": "E002",
        "events": ["evid_broken_1"],
        "created": "2026-07-07T12:07:00Z",
        "completed_at": "2026-07-07T12:07:01Z",
        "summary": {"hash_chain_valid": False, "error_position": 1}
    }
}
for filename, data in examples.items():
    with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[4/4] Examples done')
