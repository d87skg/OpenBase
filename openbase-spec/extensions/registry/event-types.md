# Event Type Registry

**Asset-Type:** Protocol
**Category:** Registry
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Capability:** CAP-0002

---

This registry defines all valid Event Types for OpenBase Evidence.

## Specification

- Event Types MUST use  + "UPPER_SNAKE_CASE" + 
- Event Types MUST be registered before use in Evidence
- New Event Types may be added via PCP process

## Categories

| Category | Description |
| :--- | :--- |
| Lifecycle | Agent start / stop / lifecycle events |
| LLM | LLM invocation and response |
| Tool | Tool invocation and result |
| State | State and memory updates |
| Policy | Policy evaluation events |
| Runtime | Runtime errors and system events |

## Registered Event Types

| Event Type | Category | Stability | Since |
| :--- | :--- | :--- | :--- |
| AGENT_STARTED | Lifecycle | Stable | 1.0.0 |
| AGENT_FINISHED | Lifecycle | Stable | 1.0.0 |
| LLM_CALL | LLM | Stable | 1.0.0 |
| LLM_RESPONSE | LLM | Stable | 1.0.0 |
| TOOL_CALL | Tool | Stable | 1.0.0 |
| TOOL_RESULT | Tool | Stable | 1.0.0 |
| STATE_UPDATE | State | Stable | 1.0.0 |
| MEMORY_UPDATE | State | Stable | 1.0.0 |
| POLICY_DECISION | Policy | Stable | 1.0.0 |
| ERROR | Runtime | Stable | 1.0.0 |

## Adding New Event Types

1. Submit a PCP (Protocol Change Proposal)
2. Update this registry
3. Create example Evidence using the new type

## References

- Evidence Spec: protocol/specs/evidence.md
- PCP Process: governance/processes/pcp.md
