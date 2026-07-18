# OpenBase Conformance Governance

**Version**: 1.0
**Status**: Active
**Adopted**: 2026-07-18

---

## Conformance Levels

| Level | Requirements | Badge |
|-------|-------------|-------|
| **COMPATIBLE** | Emits valid OBS events | Bronze |
| **CERTIFIED** | COMPATIBLE + Evidence chain with signatures | Silver |
| **VERIFIED** | CERTIFIED + Replay verification passes | Gold |
| **GOLD** | VERIFIED + Trust score ≥ 0.70 + Certificate issued | Platinum |

## Certification Process

1. Runtime implements OBS event emission
2. Runtime produces evidence using Evidence Schema v2.0
3. Runtime submits evidence package to openbase certify
4. CertificationEngine runs 7 compliance checks
5. Badge issued at achieved level

## Badge Usage

Certified projects may display the OpenBase badge:

`markdown
[![OpenBase Certified](https://img.shields.io/badge/OpenBase-Certified_GOLD-FFD700)](https://github.com/d87skg/openbase)
Revocation
Certification may be revoked if:

Breaking changes to event format without OBEP

Evidence of falsified execution records

Security vulnerability in signature implementation

Future: Conformance Committee
When the ecosystem reaches 1000+ certified runtimes, a formal Conformance Committee will be established with:

Independent certification authority

Regular conformance suite updates

Third-party certification labs
