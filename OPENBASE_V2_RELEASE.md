# OpenBase v2.0 Release

## The Open Trust Protocol Stack for AI Agents

**Release Date**: 2026-07-09
**Status**: Stable
**Protocol Version**: 2.0.0

---

## 1. Protocol Freeze Declaration

From v2.0, the following layers enter **Stable Core**:

| Layer | Version | Status |
|:---|:---|:---|
| Identity | v1.0 | Frozen |
| Event (OBS) | v1.0 | Frozen |
| Evidence | v2.0 | Frozen |
| Replay | v1.0 | Frozen |
| Trust | v1.0 | Frozen |
| Certificate | v1.0 | Frozen |
| Transport | v1.0 | Frozen |

Any breaking change to Stable Core MUST follow the OBEP process:
OBEP Proposal -> Discussion -> Vote -> RFC -> Implementation -> Release.

---

## 2. Compatibility Promise

All v2.x releases guarantee backward compatibility with v2.0.

Prohibited without OBEP:
- Event Schema breaking changes
- Evidence format breaking changes
- Replay incompatibility
- Certificate schema changes

Allowed in minor releases:
- New event types added to OBS registry
- New optional fields
- New transport protocol support
- Performance improvements

---

## 3. Core Philosophy

OpenBase is a Protocol Layer, not a Framework, Runtime, or Cloud Service.
We define how trust is established between AI Agents.
We do not define how Agents work.
We are Runtime-agnostic and Model-agnostic.

---

## 4. Architecture

Certificate Layer: BRONZE / SILVER / GOLD / PLATINUM
Trust Layer: 5-Dimension Score / Decay / Trend
Replay Layer: STRUCTURAL / CAUSAL / LOGICAL / EXACT
Evidence Layer: SHA-256 Hash Chain / Ed25519 Signature
Event Layer (OBS): 23 Canonical Event Types
Identity Layer: Agent / Runtime / Model / Tool / Human
Transport Layer: REST / gRPC / MCP / SDK / Adapter

---

## 5. Developer Entry

Traccia SDK:
  pip install traccia
  @observe decorator for one-line integration

---

## 6. Conformance

openbase certify <runtime> -> PASS/FAIL report

---

## 7. Testing

268 Conformance Tests, 100% passing.

---

## 8. License

MIT License
