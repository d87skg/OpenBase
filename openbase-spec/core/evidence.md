# Evidence Specification v1.0

**Asset-Type:** Protocol
**Category:** Specification
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Capability:** CAP-0002
**Related:** protocol/README.md, canon/terminology.md

---

## 1. Purpose

This specification defines the structure, semantics, and validity rules for **Evidence** in the OpenBase Protocol.

Evidence is a standardized, verifiable record of execution facts produced by an autonomous agent.

All Evidence MUST be:
- **Self-contained** — Contains all information needed for verification.
- **Cryptographically verifiable** — Supports hash chaining and digital signatures.
- **Causally ordered** — Supports reconstruction of execution order.
- **Implementation-independent** — No runtime-specific semantics.

## 2. Scope

This specification covers:
- Evidence data model (required and optional fields)
- Field types and constraints
- Evidence chaining (hash chain)
- Cryptographic signing and verification
- Causal ordering via vector clocks
- Versioning and extensibility rules

This specification does **not** cover:
- Storage or transmission of Evidence
- Specific cryptographic algorithms (except required properties)
- Execution semantics (covered in Execution Semantics specification)

## 3. Core Concepts

### Evidence

An Evidence object is a JSON document that records a single execution fact.

**Key properties:**
- It is **immutable** after creation.
- It **links** to previous Evidence via hash chain.
- It is **cryptographically signed** by the executing agent.
- It carries a **vector clock** for causal ordering.

### Evidence Chain

A sequence of Evidence objects where each object references the previous one via hash.

The chain enables:
- Tamper detection
- Execution reconstruction
- Audit trails

### Evidence Stream

An unordered collection of Evidence objects from multiple agents or executions.

Streams are ordered using vector clocks.

## 4. Evidence Object

### 4.1 Required Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| spec_version | string | Evidence spec version (1.0.0) |
| event_id | string | Unique identifier (UUID) |
| execution_id | string | Execution context identifier (UUID) |
| gent_id | string | Agent identifier |
| event_type | string | Type of event (see Event Types) |
| 	imestamp | string | ISO 8601 UTC timestamp |
| causal | object | Causal metadata |
| causal.parent_id | string | UUID of previous event (null if first) |
| causal.vector_clock | object | Map of node_id → counter |
| payload | object | Event-specific data |
| hash | string | SHA-256 hash of this event |
| signature | string | Ed25519 signature (base64) |
| public_key | string | Ed25519 public key (base64) |

### 4.2 Optional Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| metadata | object | Additional metadata |
| metadata.agent_version | string | Agent version |
| metadata.model | string | LLM model identifier |
| metadata.cost | number | Estimated cost |
| metadata.duration | number | Duration in milliseconds |
| 	ags | array | String tags for categorization |
| environment | string | e.g., dev, staging, production |

### 4.3 Event Types

| Event Type | Description |
| :--- | :--- |
| AGENT_STARTED | Agent execution began |
| AGENT_FINISHED | Agent execution completed |
| LLM_CALL | LLM was invoked |
| LLM_RESPONSE | LLM returned a response |
| TOOL_CALL | Tool was invoked |
| TOOL_RESULT | Tool returned a result |
| STATE_UPDATE | Agent state changed |
| MEMORY_UPDATE | Memory was updated |
| POLICY_DECISION | Policy evaluation occurred |
| ERROR | An error occurred |

Extensions may define additional event types.

### 4.4 Payload Requirements

Each event type defines its own payload structure.

All payloads MUST:
- Be valid JSON
- Be deterministic in serialization (key order, escaping)
- Contain all data required for replay

## 5. Evidence Chaining

### 5.1 Hash Chain

Each Evidence object MUST include a hash field.

The hash is computed as:
hash = SHA-256( previous_hash + canonical_json(event_without_hash) )

Where:
- previous_hash is the hash field of the parent event
- canonical_json is JSON serialized with sorted keys

### 5.2 Chain Integrity

An Evidence chain is valid if:
1. Every parent_id references an existing event
2. Every hash matches the computed hash
3. The chain is connected (no gaps)

## 6. Cryptographic Signing

### 6.1 Signing

Evidence MUST be signed using Ed25519.

The signature covers:
signature = Ed25519.sign( hash + execution_id )

### 6.2 Verification

Verification requires:
1. The public key must be valid
2. The signature must verify against the hash + execution_id
3. The public key must correspond to the agent identity (if verified)

## 7. Causal Ordering

### 7.1 Vector Clock

Each Evidence object MUST include a causal.vector_clock field.

The vector clock is a map:
{
  "node-A": 5,
  "node-B": 3
}

### 7.2 Ordering Rules

Given two events A and B:

- If c(A) < vc(B) → A happened before B
- If c(A) > vc(B) → B happened before A
- If c(A) || vc(B) → A and B are concurrent

## 8. Extensibility

### 8.1 Adding New Event Types

New event types may be added by extending the Event Type registry.

### 8.2 Adding New Fields

New optional fields may be added without breaking existing validators.

### 8.3 Backward Compatibility

Protocol changes MUST maintain:
- Backward compatibility with existing Evidence objects
- Ability for older validators to ignore new fields

## 9. Versioning

| Version | Status | Changes |
| :--- | :--- | :--- |
| 1.0.0 | Frozen | Initial specification |

Future versions:
- MUST follow semantic versioning
- MUST maintain backward compatibility for major version

## 10. Conformance

An implementation is conformant if it:
1. Produces Evidence following this specification
2. Verifies Evidence following this specification
3. Supports all required fields
4. Passes the conformance test suite

## 11. Examples

### Minimal Evidence

{
  "spec_version": "1.0.0",
  "event_id": "e8b2c3d4-5f6g-7h8i-9j0k-1l2m3n4o5p6",
  "execution_id": "a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6",
  "agent_id": "weather-bot-v1",
  "event_type": "AGENT_STARTED",
  "timestamp": "2026-07-03T10:00:00.000Z",
  "causal": {
    "parent_id": null,
    "vector_clock": {
      "agent-1": 1
    }
  },
  "payload": {
    "input": "What is the weather?"
  },
  "hash": "abc123...",
  "signature": "def456...",
  "public_key": "ghi789..."
}

## 12. References

- Canon Terminology: canon/terminology.md
- Architecture Domain Model: architecture/domain-model.md
- Execution Semantics: protocol/specs/execution.md (future)
- Verification Protocol: protocol/specs/verification.md (future)
- PCP Process: governance/processes/pcp.md
