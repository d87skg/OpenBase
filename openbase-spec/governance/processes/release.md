# Release Process

**Asset-Type:** Governance
**Category:** Process
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** proposal-policy.md

---

## 1. Purpose

This document defines how OpenBase releases are planned, gated, and published.

## 2. Release Types

| Type | Object | Frequency |
| :--- | :--- | :--- |
| Identity Release | Charter, Founding, Manifesto, Canon | Rare (v1.0 → v2.0) |
| Protocol Release | OBP, Evidence Spec, Execution Spec | OBP v1.0, v1.1 |
| Reference Release | Python Runtime, SDK, CLI | runtime v0.8, SDK v1.2 |

## 3. Release Gates

Every release must pass all gates:

 + "`" + 
Release Candidate
        ↓
Governance Gate
        ↓
Protocol Gate
        ↓
Conformance Gate
        ↓
Documentation Gate
        ↓
Release
 + "`" + 

### 3.1 Governance Gate

- All related Proposals are Closed
- All related ADRs are complete
- Release has clear owner

### 3.2 Protocol Gate

- Protocol Spec is finalized
- PCPs are complete
- Spec version is updated

### 3.3 Conformance Gate

- Conformance Test Suite passes
- Compatibility Matrix is updated
- All breaking changes are documented

### 3.4 Documentation Gate

- Canon is unchanged or updated
- Spec is updated with changes
- Migration Guide is published

## 4. Release Versioning

- Identity Release: v1.0.0 → v2.0.0 (major)
- Protocol Release: v1.0.0 → v1.1.0 (minor) / v2.0.0 (major)
- Reference Release: follows SemVer

## 5. Capability Mapping

Every release must declare which Capabilities are included:

 + "`yaml" + 
Capabilities:
  - CAP-0002 Evidence
  - CAP-0008 Verification
  - CAP-0013 Conformance
 + "`" + 

## 6. Release Notes

Every release must publish Release Notes using the Release Template.

## 7. References

- Proposal Policy: governance/policies/proposal-policy.md
- Release Template: governance/templates/release-template.md
- PCP Process: governance/processes/pcp.md
