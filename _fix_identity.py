import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'identity')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Identity Specification ---
spec = '# OpenBase Identity Specification v1.0\n\n## Version\n**1.0**\n\n## Status\n**Draft**\n\n---\n\n## 1. Abstract\n\nThe Identity Layer defines the canonical identity model for all entities that produce or consume events in the OpenBase protocol stack.\n\nEvery OBS Event has an actor field. This specification defines what actors are, how they are identified, and how identities are verified.\n\n## 2. Identity Model\n\n### 2.1 Core Principle\n\nAn Identity is a stable, verifiable identifier for an entity in the Agent execution ecosystem. Identities are globally unique and immutable.\n\n### 2.2 Actor Types\n\n| Type | Description | Example ID |\n|:---|:---|:---|\n| agent | An AI agent instance | agent.acme.research-bot |\n| runtime | Execution environment | runtime.openhands.0.15.0 |\n| model | AI model identifier | model.anthropic.claude-sonnet-4 |\n| tool | A tool or plugin | tool.filesystem.read |\n| human | A human operator | human.alice@acme.com |\n| system | Infrastructure component | system.scheduler.main |\n\n### 2.3 Identity Format\n\n<type>.<namespace>.<name>\n\nExamples:\n- agent.openclaw.demo-assistant\n- runtime.langgraph.v0.3\n- model.openai.gpt-5\n- tool.github.create-issue\n\n## 3. Identity Lifecycle\n\nCreated -> Registered -> Active -> Deprecated -> Retired\n\n- Created: Identity claimed by entity\n- Registered: Identity published to Registry\n- Active: Identity in operational use\n- Deprecated: Identity still valid but superseded\n- Retired: Identity no longer valid\n\n## 4. Identity Verification\n\nIdentities are verified through:\n1. Public Key: Each identity has an Ed25519 key pair\n2. Registry Lookup: Identities are resolvable via Registry\n3. Chain of Trust: Parent runtime vouches for child agents\n\n## 5. References\n\n- OBS v1.0 (Event actor field)\n- Registry v1.0 (Identity registration)\n- Certificate v1.0 (Identity attestation)\n'
with open(os.path.join(spec_dir, 'IDENTITY_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
    f.write(spec)
print('[1/4] Spec done')

# --- JSON Schema ---
schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/identity/v1.0/identity.schema.json",
    "title": "OpenBase Identity v1.0",
    "description": "Identity model for all actors in the OpenBase protocol",
    "type": "object",
    "required": ["id", "type", "display_name", "public_key", "status", "created"],
    "properties": {
        "id": {"type": "string", "pattern": "^[a-z]+\\.[a-z0-9_-]+\\.[a-z0-9_-]+$"},
        "type": {"type": "string", "enum": ["agent", "runtime", "model", "tool", "human", "system"]},
        "display_name": {"type": "string"},
        "public_key": {"type": "string", "pattern": "^ed25519:[A-Za-z0-9+/=]+$"},
        "parent_runtime": {"type": "string"},
        "status": {"type": "string", "enum": ["created", "registered", "active", "deprecated", "retired"]},
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

# --- README ---
readme = '# OpenBase Identity v1.0\n\nDefines the identity model for all actors in the OpenBase protocol stack.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| IDENTITY_SPEC_v1.0.md | Full specification |\n| identity.schema.json | JSON Schema |\n| examples/ | Example identities |\n'
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('[3/4] README done')

# --- Examples ---
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
        "metadata": {"version": "0.1.0", "language": "go", "repo": "https://github.com/openbase/openclaw"}
    },
    "model_identity.json": {
        "id": "model.anthropic.claude-sonnet-4",
        "type": "model",
        "display_name": "Claude Sonnet 4",
        "public_key": "ed25519:dGVzdF9tb2RlbF9wdWJsaWNfa2V5X2RhdGFfaGVyZV90ZXN0",
        "status": "active",
        "created": "2026-05-01T00:00:00Z",
        "metadata": {"provider": "Anthropic", "context_window": 200000}
    },
    "tool_identity.json": {
        "id": "tool.filesystem.read",
        "type": "tool",
        "display_name": "Filesystem Read Tool",
        "public_key": "ed25519:dGVzdF90b29sX3B1YmxpY19rZXlfZGF0YV9oZXJlX3Rlc3Q=",
        "parent_runtime": "runtime.openclaw.0.1.0",
        "status": "active",
        "created": "2026-07-07T00:00:00Z",
        "metadata": {"category": "filesystem", "risk_level": "low"}
    }
}
for filename, data in examples.items():
    with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[4/4] Examples done')
