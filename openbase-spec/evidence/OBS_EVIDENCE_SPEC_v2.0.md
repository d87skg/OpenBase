# OpenBase Evidence Specification v2.0

## Version
**2.0**

## Status
**Draft**

## Predecessor
Evidence v1.0 (deprecated)

---

## 1. Abstract

Evidence v2.0 redefines Evidence as a Signed Snapshot of an OBS Event.
Every Evidence object MUST reference exactly one OBS event via event_id.
Evidence forms an append-only hash chain, enabling tamper detection and
causal ordering verification.

## Key Changes from v1.0

| v1.0 | v2.0 |
|:---|:---|
| Standalone entity | Derived from OBS Event |
| No event linkage | Required event_id field |
| Simple hash | SHA-256 hash chain |
| Placeholder signature | Ed25519 real signature |
| No causal ordering | Vector clock support |
| No public key | Required public_key field |

## 2. Evidence Model

### 2.1 Data Flow

OBS Event (event_id: evt_001) goes through canonical JSON serialization,
then SHA-256 hash with previous_hash, then Ed25519 signature, resulting
in the Evidence Object. From there it enables Hash Chain Verification,
Replay Reconstruction, and Trust Score Computation.

### 2.2 Required Fields

evidence_id, spec_version, event_id, execution_id, agent_id, event_type,
timestamp, causal (parent_id + vector_clock), payload, hash, signature,
public_key.

## 3. Hash Chain Specification

hash = SHA-256(previous_hash + canonical_json(event_without_hash_and_signature))
Genesis evidence uses 64 zero bytes as previous_hash.
Chain verification: computed hash must equal stored hash for each link.

## 4. Signature Specification

Algorithm: Ed25519. Format: ed25519:<base64>. Signed data: hash + execution_id.

## 5. Vector Clock Specification

Standard vector clock for partial ordering. A happened-before B iff
vc(A)[actor] <= vc(B)[actor] for all actors, with strict inequality for one.

## 6. Evidence Lifecycle

Event Produced -> Canonical Serialization -> Hash Computation ->
Signature Generation -> Evidence Stored -> Hash Chain Verification ->
Trust Score Update

## 7. Storage

Append-only structure: .evidence/chain/ with JSON files, index.json, and HEAD.

## 8. Migration from v1.0

Use: openbase migrate evidence --from v1.0 --to v2.0

## 9. References

OBS v1.0, RFC 8785, RFC 8032, SHA-256 FIPS 180-4, Vector Clocks