import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'identity')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Identity Specification ---
spec = '''# OpenBase Identity Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Identity Layer defines the canonical identity model for all entities
that produce or consume events in the OpenBase protocol stack.

Every OBS Event has an ctor field. This specification defines what
actors are, how they are identified, and how identities are verified.

---

## 2. Identity Model

### 2.1 Core Principle

An Identity is a **stable, verifiable identifier** for an entity in the
Agent execution ecosystem. Identities are globally unique and immutable.

### 2.2 Actor Types

| Type | Description | Example ID |
|:---|:---|:---|
| gent | An AI agent instance | gent.acme.research-bot |
| untime | Execution environment | untime.openhands.0.15.0 |
| model | AI model identifier | model.anthropic.claude-sonnet-4 |
| 	ool | A tool or plugin | 	ool.filesystem.read |
| human | A human operator | human.alice@acme.com |
| system | Infrastructure component | system.scheduler.main |

### 2.3 Identity Format
<type>.<namespace>.<name>

text

Examples:
- gent.openclaw.demo-assistant
- untime.langgraph.v0.3
- model.openai.gpt-5
- 	ool.github.create-issue

---

## 3. Identity Lifecycle
Created → Registered → Active → Deprecated → Retired

text

- **Created**: Identity claimed by entity
- **Registered**: Identity published to Registry
- **Active**: Identity in operational use
- **Deprecated**: Identity still valid but superseded
- **Retired**: Identity no longer valid

---

## 4. Identity Verification

Identities are verified through:
1. **Public Key**: Each identity has an Ed25519 key pair
2. **Registry Lookup**: Identities are resolvable via Registry
3. **Chain of Trust**: Parent runtime vouches for child agents

---

## 5. Identity Schema

`json
{
  "id": "agent.openclaw.demo",
  "type": "agent",
  "display_name": "Demo Assistant",
  "public_key": "ed25519:<base64>",
  "parent_runtime": "runtime.openclaw.0.1.0",
  "status": "active",
  "created": "2026-07-07T00:00:00Z"
}
6. References
OBS v1.0 (Event actor field)

Registry v1.0 (Identity registration)

Certificate v1.0 (Identity attestation)
'''
with open(os.path.join(spec_dir, 'IDENTITY_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
f.write(spec)
print('[1/4] Spec done')

--- JSON Schema ---
schema = {
"id": "https://openbase.dev/schemas/identity/v1.0/identity.schema.json",
"title": "OpenBase Identity v1.0",
"description": "Identity model for all actors in the OpenBase protocol",
"type": "object",
"required": ["id", "type", "display_name", "public_key", "status", "created"],
"properties": {
"id": {
"type": "string",
"pattern": "^[a-z]+\.[a-z0-9_-]+\.[a-z0-9_-]+" }, "type": { "type": "string", "enum": ["agent", "runtime", "model", "tool", "human", "system"] }, "display_name": {"type": "string"}, "public_key": { "type": "string", "pattern": "^ed25519:[A-Za-z0-9+/=]+"
},
"parent_runtime": {"type": "string"},
"status": {
"type": "string",
"enum": ["created", "registered", "active", "deprecated", "retired"]
},
"created": {"type": "string", "format": "date-time"},
"deprecated_at": {"type": "string", "format": "date-time"},
"retired_at": {"type": "string", "format": "date-time"},
"metadata": {"type": "object"}
},
"additionalProperties": False
}
with open(os.path.join(spec_dir, 'identity.schema.json'), 'w', encoding='utf-8') as f:
json.dump(schema, f, indent=2)
print('[2/4] Schema done')

--- README ---
readme = "# OpenBase Identity v1.0\n\nDefines the identity model for all actors in the OpenBase protocol stack.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| IDENTITY_SPEC_v1.0.md | Full specification |\n| identity.schema.json | JSON Schema |\n| examples/ | Example identities |\n"
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
f.write(readme)
print('[3/4] README done')

--- Examples ---
examples = {
"agent_identity.json": {
"id": "agent.openclaw.demo",
"type": "agent",
"display_name": "Demo Assistant",
"public_key": "ed25519:dGVzdF9wdWJsaWNfa2V5X2RhdGFfZm9yX2RlbW9uc3RyYXRpb24=",
"parent_runtime": "runtime.openclaw.0.1.0",
"status": "active",
"created": "2026-07-07T00:00:00Z"
},
"runtime_identity.json": {
"id": "runtime.openclaw.0.1.0",
"type": "runtime",
"display_name": "OpenClaw Reference Runtime",
"public_key": "ed25519:dGVzdF9ydW50aW1lX3B1YmxpY19rZXlfZGF0YV9oZXJlX3Rlc3Q=",
"status": "active",
"created": "2026-07-01T00:00:00Z",
"metadata": {
"version": "0.1.0",
"language": "go",
"repo": "https://github.com/openbase/openclaw"
}
},
"model_identity.json": {
"id": "model.anthropic.claude-sonnet-4",
"type": "model",
"display_name": "Claude Sonnet 4",
"public_key": "ed25519:dGVzdF9tb2RlbF9wdWJsaWNfa2V5X2RhdGFfaGVyZV90ZXN0",
"status": "active",
"created": "2026-05-01T00:00:00Z",
"metadata": {
"provider": "Anthropic",
"context_window": 200000
}
},
"tool_identity.json": {
"id": "tool.filesystem.read",
"type": "tool",
"display_name": "Filesystem Read Tool",
"public_key": "ed25519:dGVzdF90b29sX3B1YmxpY19rZXlfZGF0YV9oZXJlX3Rlc3Q=",
"parent_runtime": "runtime.openclaw.0.1.0",
"status": "active",
"created": "2026-07-07T00:00:00Z",
"metadata": {
"category": "filesystem",
"risk_level": "low"
}
}
}
for filename, data in examples.items():
with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
json.dump(data, f, indent=2)
print('[4/4] Examples done')
