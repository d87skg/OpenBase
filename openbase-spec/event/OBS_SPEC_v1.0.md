# OpenBase Event Specification (OBS)

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The OpenBase Event Specification (OBS) defines the canonical event format for AI Agent execution. All Agent Runtime activities MUST be represented as OpenBase Events to enable evidence generation, replay, verification, and trust computation across heterogeneous Agent systems.

### Key Principles

1. **Runtime-Agnostic** — Any Agent runtime can produce OBS events
2. **Verifiable** — Events are the foundation for evidence chains
3. **Replayable** — Events capture sufficient state for deterministic replay
4. **Minimal** — Core schema is small; extensions are additive

---

## 2. Event Model

### 2.1 Core Concept

An OpenBase Event represents a discrete, timestamped state transition within an Agent execution. Events are immutable once emitted and form a causal chain.

### 2.2 Event Flow
Runtime Activity
│
▼
Canonical OBS Event
│
├──► Evidence (signed snapshot)
├──► Replay (state reconstruction)
└──► Trust (verification basis)

text

### 2.3 Required Fields

| Field | Type | Description |
|:---|:---|:---|
| event_id | string | Globally unique event identifier |
| event_type | string | One of the registered OBS event types |
| ersion | string | OBS spec version (e.g., "1.0") |
| ctor | object | Entity that produced this event |
| untime | object | Execution environment metadata |
| 	imestamp | string | ISO 8601 UTC timestamp |
| payload | object | Event-type-specific data |

### 2.4 Optional Fields

| Field | Type | Description |
|:---|:---|:---|
| state | object | Before/after state snapshot |
| parent_id | string | Causal parent event ID |
| ector_clock | object | Partial ordering vector clock |

---

## 3. Actor Model

Every event has an ctor that identifies the producing entity:

`json
{
  "actor": {
    "id": "agent.openclaw.demo",
    "type": "agent"
  }
}
Actor Types
TypeDescription
agentAn AI agent instance
toolA tool or plugin
humanA human operator
systemInfrastructure component
4. Runtime Metadata
The runtime object identifies the execution environment:

json
{
  "runtime": {
    "name": "openhands",
    "version": "0.15.0"
  }
}
5. Event Types Registry
5.1 Agent Lifecycle
AGENT_CREATED

AGENT_STARTED

AGENT_PAUSED

AGENT_RESUMED

AGENT_FINISHED

AGENT_FAILED

5.2 LLM Interactions
LLM_REQUEST

LLM_RESPONSE

LLM_STREAM_START

LLM_STREAM_END

5.3 Tool Execution
TOOL_CALL

TOOL_RESULT

TOOL_ERROR

5.4 Memory Operations
MEMORY_READ

MEMORY_WRITE

MEMORY_DELETE

5.5 Execution
COMMAND_EXECUTE

FILE_READ

FILE_WRITE

CODE_EXECUTE

5.6 Human Interaction
APPROVAL_REQUEST

APPROVAL_GRANTED

APPROVAL_DENIED

6. State Transitions
Events capture state transitions:

json
{
  "state": {
    "before": "idle",
    "after": "running"
  }
}
7. Versioning
OBS follows Semantic Versioning 2.0.0.

MAJOR — Breaking changes to required fields or event types

MINOR — New event types or optional fields

PATCH — Documentation fixes, non-normative changes

All breaking changes require an OBIP (OpenBase Improvement Proposal).

8. Relationship to Other Layers
LayerRelationship
IdentityProvides actor/runtime identifiers
EvidenceEvidence = Signed OBS Event + Hash
ReplayReplay = OBS Event Stream Replay
TrustTrust = Verification of OBS Event Chain
CertificateCertificate = Attestation of OBS Compliance
9. References
JSON Schema

RFC 3339 (Date and Time)

Semantic Versioning 2.0.0

OpenBase Governance Model

OBIP-0001 (Evidence Schema)
