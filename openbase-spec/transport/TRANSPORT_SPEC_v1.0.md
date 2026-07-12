# OpenBase Transport Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Transport Layer defines how Runtimes, Agents, and external systems connect to the OpenBase protocol stack. It provides a unified interface regardless of the underlying transport mechanism.

## 2. Transport Mechanisms

### 2.1 Supported Protocols

| Protocol | Use Case | Status |
|:---|:---|:---|
| REST API | HTTP-based integration | Required |
| gRPC | High-performance streaming | Recommended |
| MCP | Model Context Protocol | Supported |
| WebSocket | Real-time event streaming | Supported |
| SDK | Native language bindings | Recommended |
| Adapter | Framework-specific bridges | Required |

### 2.2 Endpoint Structure

All REST endpoints follow:

`
/api/v1/{resource}/{action}
`

Core resources:
- /events - Event submission
- /evidence - Evidence retrieval
- /trust - Trust score queries
- /certificates - Certificate operations
- /registry - Identity registration
- /replay - Replay package management

## 3. Adapter Interface

### 3.1 Core Methods

Every Adapter MUST implement:

`
capture()  - Intercept runtime events
normalize() - Convert to OBS format
emit()     - Submit to OpenBase
verify()   - Validate evidence chain
`

### 3.2 Adapter Lifecycle

`
Initialize -> Configure -> Connect -> Active -> Disconnect
`

## 4. SDK Interface

### 4.1 Traccia SDK

The reference SDK provides:

`python
from traccia import observe

@observe
def my_agent():
    # Automatically generates OBS events
    pass
`

### 4.2 SDK Requirements

- Zero-config by default
- Automatic event capture
- Evidence generation
- Hash chain management
- Signature handling

## 5. Protocol Buffers (gRPC)

gRPC service definition for high-throughput scenarios.

## 6. MCP Integration

OpenBase can serve as an MCP server, exposing trust data as MCP resources.

## 7. Authentication

All transport endpoints require:
- API Key for SDK access
- Ed25519 signature for evidence submission
- mTLS for service-to-service communication

## 8. References

- OBS v1.0 (event format)
- Evidence v2.0 (evidence format)
- Identity v1.0 (actor identification)
