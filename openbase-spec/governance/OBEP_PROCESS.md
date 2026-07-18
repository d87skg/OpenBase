# OpenBase Enhancement Proposal (OBEP) Process

**Version**: 1.0
**Status**: Active
**Adopted**: 2026-07-18

---

## What is an OBEP?

An OBEP (OpenBase Enhancement Proposal) is a formal document that proposes a change to the OpenBase Protocol Stable Core. OBEPs are the only mechanism for modifying frozen protocol layers.

## When is an OBEP Required?

An OBEP is **required** for:
- Breaking changes to any Stable Core schema (OBS, Evidence, Replay, Conformance)
- New required fields in existing schemas
- Removal or renaming of event types in OBS
- Changes to hash or signature algorithms
- Changes to Replay fidelity level definitions

An OBEP is **not required** for:
- New optional fields in existing schemas
- New event types added to OBS registry (non-breaking additions)
- New transport protocol support
- Documentation improvements
- Bug fixes that do not change schema behavior

## OBEP Lifecycle
Draft → Review → Accepted → RFC → Implemented → Released
↓ ↓ ↓
Withdrawn Deferred Rejected

text

### Stage 1: Draft
- Author writes OBEP using the RFC template
- Submitted as GitHub Issue with label OBEP

### Stage 2: Review
- Minimum 2-week community discussion period
- Core maintainers provide technical review
- Author may revise based on feedback

### Stage 3: Decision
- Core maintainers vote
- ≥2/3 majority required for acceptance
- Possible outcomes: Accepted, Rejected, Deferred (revisit in 6 months)

### Stage 4: RFC
- Accepted OBEP becomes a formal RFC document
- Published in openbase-spec/rfc/ directory
- Assigned permanent RFC number

### Stage 5: Implementation
- RFC implemented in reference implementation
- Conformance tests updated
- Documentation updated

### Stage 6: Release
- Included in next minor or major release
- Minimum 6-month deprecation period for breaking changes

## OBEP Numbering

OBEPs are numbered sequentially: OBEP-0001, OBEP-0002, etc.

## Current OBEPs

| Number | Title | Status |
|--------|-------|--------|
| OBEP-0001 | Evidence Schema v2.0 | Implemented |
| OBEP-0002 | Replay Protocol v1.0 | Implemented |
| OBEP-0003 | Trust Model v1.0 | Implemented |
| OBEP-0004 | Certificate Schema v1.0 | Implemented |
| OBEP-0005 | Registry Protocol | Draft |
| OBEP-0006 | Wire Protocol | Draft |
| OBEP-0007 | Compatibility Policy | Implemented |
| OBEP-0008 | Conformance Suite | Implemented |
| OBEP-0009 | Versioning Policy | Implemented |
| OBEP-0010 | Governance Model | Implemented |
