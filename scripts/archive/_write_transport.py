import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'transport')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Transport Specification ---
spec = '# OpenBase Transport Specification v1.0\n\n## Version\n**1.0**\n\n## Status\n**Draft**\n\n---\n\n## 1. Abstract\n\nThe Transport Layer defines how Runtimes, Agents, and external systems connect to the OpenBase protocol stack. It provides a unified interface regardless of the underlying transport mechanism.\n\n## 2. Transport Mechanisms\n\n### 2.1 Supported Protocols\n\n| Protocol | Use Case | Status |\n|:---|:---|:---|\n| REST API | HTTP-based integration | Required |\n| gRPC | High-performance streaming | Recommended |\n| MCP | Model Context Protocol | Supported |\n| WebSocket | Real-time event streaming | Supported |\n| SDK | Native language bindings | Recommended |\n| Adapter | Framework-specific bridges | Required |\n\n### 2.2 Endpoint Structure\n\nAll REST endpoints follow:\n\n`\n/api/v1/{resource}/{action}\n`\n\nCore resources:\n- /events - Event submission\n- /evidence - Evidence retrieval\n- /trust - Trust score queries\n- /certificates - Certificate operations\n- /registry - Identity registration\n- /replay - Replay package management\n\n## 3. Adapter Interface\n\n### 3.1 Core Methods\n\nEvery Adapter MUST implement:\n\n`\ncapture()  - Intercept runtime events\nnormalize() - Convert to OBS format\nemit()     - Submit to OpenBase\nverify()   - Validate evidence chain\n`\n\n### 3.2 Adapter Lifecycle\n\n`\nInitialize -> Configure -> Connect -> Active -> Disconnect\n`\n\n## 4. SDK Interface\n\n### 4.1 Traccia SDK\n\nThe reference SDK provides:\n\n`python\nfrom traccia_sdk import observe\n\n@observe\ndef my_agent():\n    # Automatically generates OBS events\n    pass\n`\n\n### 4.2 SDK Requirements\n\n- Zero-config by default\n- Automatic event capture\n- Evidence generation\n- Hash chain management\n- Signature handling\n\n## 5. Protocol Buffers (gRPC)\n\ngRPC service definition for high-throughput scenarios.\n\n## 6. MCP Integration\n\nOpenBase can serve as an MCP server, exposing trust data as MCP resources.\n\n## 7. Authentication\n\nAll transport endpoints require:\n- API Key for SDK access\n- Ed25519 signature for evidence submission\n- mTLS for service-to-service communication\n\n## 8. References\n\n- OBS v1.0 (event format)\n- Evidence v2.0 (evidence format)\n- Identity v1.0 (actor identification)\n'
with open(os.path.join(spec_dir, 'TRANSPORT_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
    f.write(spec)
print('[1/5] Spec done')

# --- JSON Schema: Adapter Config ---
adapter_schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/transport/v1.0/adapter-config.schema.json",
    "title": "OpenBase Adapter Configuration v1.0",
    "description": "Configuration for a Runtime Adapter connecting to OpenBase",
    "type": "object",
    "required": ["adapter_id", "runtime_name", "target_protocol", "endpoint"],
    "properties": {
        "adapter_id": {"type": "string"},
        "runtime_name": {"type": "string"},
        "runtime_version": {"type": "string"},
        "target_protocol": {"type": "string", "enum": ["REST", "gRPC", "MCP", "WebSocket"]},
        "endpoint": {"type": "string", "format": "uri"},
        "auth": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["api_key", "ed25519", "mtls", "none"]},
                "api_key": {"type": "string"},
                "public_key": {"type": "string"}
            }
        },
        "options": {
            "type": "object",
            "properties": {
                "auto_emit": {"type": "boolean"},
                "batch_size": {"type": "integer", "minimum": 1},
                "retry_max": {"type": "integer", "minimum": 0},
                "timeout_ms": {"type": "integer", "minimum": 100}
            }
        },
        "status": {"type": "string", "enum": ["configured", "connected", "active", "error", "disconnected"]},
        "created": {"type": "string", "format": "date-time"},
        "last_connected": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'adapter-config.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(adapter_schema, f, indent=2)
print('[2/5] Adapter schema done')

# --- JSON Schema: SDK Config ---
sdk_schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/transport/v1.0/sdk-config.schema.json",
    "title": "OpenBase SDK Configuration v1.0",
    "description": "Configuration for Traccia SDK or other OpenBase SDK",
    "type": "object",
    "required": ["sdk_name", "sdk_version", "openbase_endpoint"],
    "properties": {
        "sdk_name": {"type": "string", "enum": ["traccia", "openbase-python", "openbase-js", "openbase-go"]},
        "sdk_version": {"type": "string"},
        "openbase_endpoint": {"type": "string", "format": "uri"},
        "auth": {
            "type": "object",
            "properties": {
                "api_key": {"type": "string"},
                "key_path": {"type": "string"}
            }
        },
        "features": {
            "type": "object",
            "properties": {
                "auto_observe": {"type": "boolean"},
                "auto_evidence": {"type": "boolean"},
                "auto_replay": {"type": "boolean"},
                "log_level": {"type": "string", "enum": ["debug", "info", "warn", "error"]}
            }
        },
        "created": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'sdk-config.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(sdk_schema, f, indent=2)
print('[3/5] SDK schema done')

# --- README ---
readme = '# OpenBase Transport v1.0\n\nDefines how Runtimes and SDKs connect to the OpenBase protocol stack.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| TRANSPORT_SPEC_v1.0.md | Full specification |\n| adapter-config.schema.json | Adapter configuration schema |\n| sdk-config.schema.json | SDK configuration schema |\n| examples/ | Example configurations |\n'
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('[4/5] README done')

# --- Examples ---
examples = {
    "adapter_config_rest.json": {
        "adapter_id": "adapter-openhands-rest",
        "runtime_name": "openhands",
        "runtime_version": "0.15.0",
        "target_protocol": "REST",
        "endpoint": "https://registry.openbase.dev/api/v1",
        "auth": {"type": "api_key", "api_key": "ob_sk_test_abc123"},
        "options": {"auto_emit": True, "batch_size": 10, "retry_max": 3, "timeout_ms": 5000},
        "status": "active",
        "created": "2026-07-07T12:00:00Z",
        "last_connected": "2026-07-07T12:00:05Z"
    },
    "adapter_config_grpc.json": {
        "adapter_id": "adapter-claude-code-grpc",
        "runtime_name": "claude-code",
        "runtime_version": "2.5.0",
        "target_protocol": "gRPC",
        "endpoint": "grpc.registry.openbase.dev:443",
        "auth": {"type": "mtls"},
        "options": {"auto_emit": True, "batch_size": 50, "retry_max": 5, "timeout_ms": 3000},
        "status": "connected",
        "created": "2026-07-06T00:00:00Z",
        "last_connected": "2026-07-07T11:55:00Z"
    },
    "sdk_config_traccia.json": {
        "sdk_name": "traccia",
        "sdk_version": "0.2.0",
        "openbase_endpoint": "https://registry.openbase.dev",
        "auth": {"api_key": "ob_sk_traccia_demo"},
        "features": {"auto_observe": True, "auto_evidence": True, "auto_replay": False, "log_level": "info"},
        "created": "2026-07-07T12:00:00Z"
    }
}
for filename, data in examples.items():
    with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[5/5] Examples done')
