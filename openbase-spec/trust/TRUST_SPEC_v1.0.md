# OpenBase Trust Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Trust Layer defines how trust scores are computed for Runtimes, Agents, and other actors in the OpenBase ecosystem. Trust is derived from verifiable evidence, not subjective reputation.

## 2. Trust Model

### 2.1 Core Principle

Trust = f(Evidence, Time, Consistency, Peer Verification)

Trust is:
- Evidence-based: only verified evidence counts
- Time-weighted: recent evidence matters more
- Decay-enabled: trust decays without fresh evidence
- Multi-dimensional: not a single number

### 2.2 Trust Dimensions

| Dimension | Weight | Description |
|:---|:---|:---|
| evidence_volume | 0.30 | Quantity of valid evidence |
| evidence_quality | 0.25 | Signature validity, hash integrity |
| consistency | 0.20 | No contradictory events |
| recency | 0.15 | Freshness of evidence |
| peer_attestation | 0.10 | Certificates from trusted peers |

### 2.3 Score Range

- 0.00 - 0.20: Untrusted
- 0.21 - 0.40: Low Trust
- 0.41 - 0.60: Moderate Trust
- 0.61 - 0.80: High Trust
- 0.81 - 1.00: Fully Trusted

### 2.4 Decay Function

score(t) = score(t0) * e^(-lambda * (t - t0))

Where lambda = 0.01 per day (configurable).

## 3. Trust Update Events

Trust scores update on:
- New evidence accepted (+0.02 to +0.05)
- Evidence rejected (-0.05 to -0.10)
- Certificate issued (+0.05 to +0.15)
- Certificate revoked (-0.10 to -0.20)
- Time decay (continuous)

## 4. Trust Graph

Trust is not isolated. A Trust Graph models relationships:

`
Runtime A --vouches_for--> Agent A1
Runtime B --vouches_for--> Agent B1
Agent A1 --delegates_to--> Tool T1
`

Trust propagates through the graph via PageRank-like algorithm.

## 5. References

- Evidence v2.0 (evidence validation)
- Certificate v1.0 (attestation)
- Identity v1.0 (actor identification)
