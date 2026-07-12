# PCP Process

**Asset-Type:** Governance
**Category:** Process
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** proposal-policy.md

---

## 1. Purpose

This document defines how a Protocol Change Proposal (PCP) becomes part of OpenBase.

PCPs modify the Protocol Specification, not the implementation.

## 2. Scope

A PCP is required for:

- Evidence Spec changes (fields, types, constraints)
- Execution Semantics changes
- Verification Protocol changes
- Protocol version changes
- Protocol deprecation

PCPs are **not** required for:

- Reference Implementation changes
- SDK changes
- Adapter changes
- Documentation changes

## 3. PCP Lifecycle

 + "`" + 
Protocol Issue
  ↓
Draft PCP
  ↓
Architecture Review (AR)
  ↓
Protocol Review
  ↓
Accepted / Rejected
  ↓
Specification Updated
  ↓
Reference Implementations Updated
  ↓
Released
  ↓
Superseded
  ↓
Archived
 + "`" + 

## 4. Protocol Review

Protocol Review is separate from Architecture Review.

It verifies:

- Backward Compatibility
- Specification Clarity
- Conformance Impact
- Certification Impact

Protocol Review is conducted by the Protocol Steward.

## 5. Decision Criteria

PCP decisions must consider:

1. Does this strengthen the Mission?
2. Does this align with Canon Principles?
3. Does this maintain Layer Contract boundaries?
4. Is Backward Compatibility maintained?
5. Is the Specification clear and unambiguous?
6. Does it affect Conformance Tests?
7. Does it affect Certification criteria?

## 6. Recording a PCP

- PCP must be written using the PCP Template
- PCP must include Protocol Changes section
- PCP must include Compatibility Analysis section
- Status is set to  + "Draft" +  at creation

## 7. Superseding a PCP

- PCPs may be superseded by newer PCPs
- Status is set to  + "Superseded" + 
- Superseded-By field references the new PCP

## 8. References

- Proposal Policy: governance/policies/proposal-policy.md
- PCP Template: governance/templates/pcp-template.md
- RFC Process: governance/processes/rfc.md
- ADR Process: governance/processes/adr.md
