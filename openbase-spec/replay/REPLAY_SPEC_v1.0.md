# OpenBase Replay Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Replay Layer defines how to reconstruct a complete execution trace from an Evidence Chain. Replay is the mechanism that transforms immutable evidence records back into a verifiable timeline of Agent behavior.

## 2. Replay Model

### 2.1 Core Principle

Given an ordered sequence of Evidence objects linked by hash chain, Replay reconstructs:
- The exact sequence of events
- State transitions at each step
- Causal relationships between events
- Final execution outcome

### 2.2 Fidelity Levels

| Level | Name | Description |
|:---|:---|:---|
| 0 | STRUCTURAL | Validate hash chain integrity only |
| 1 | CAUSAL | Validate causal ordering via vector clocks |
| 2 | LOGICAL | Replay state transitions without side effects |
| 3 | EXACT | Full bit-exact replay including all outputs |

### 2.3 Replay Process

1. Load evidence chain from storage
2. Verify hash chain integrity (STRUCTURAL)
3. Verify causal ordering (CAUSAL)
4. Sort events by vector clock
5. Apply state transitions sequentially (LOGICAL)
6. Optionally re-execute for exact match (EXACT)

## 3. Replay Package Format

A Replay Package bundles all evidence needed:

`
replay_package/
  manifest.json
  chain/
    evid_0001.json
    evid_0002.json
    ...
  summary.json
`

## 4. Verification

Replay MUST verify:
- Hash chain: each hash matches previous
- Signatures: all Ed25519 signatures valid
- Vector clocks: monotonically increasing
- State consistency: no impossible transitions

## 5. Error Codes

| Code | Description |
|:---|:---|
| E001 | Evidence chain incomplete |
| E002 | Hash mismatch at position N |
| E003 | Signature verification failed |
| E004 | Vector clock violation |
| E005 | Invalid state transition |
| E006 | Missing genesis evidence |

## 6. References

- Evidence v2.0 (hash chain, signatures)
- OBS v1.0 (event types, state transitions)
- Vector Clocks (Lamport, Fidge, Mattern)
