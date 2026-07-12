# ADR Process

**Asset-Type:** Governance
**Category:** Process
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** proposal-policy.md

---

## 1. Purpose

This document defines how an Architecture Decision Record (ADR) becomes part of OpenBase.

ADRs record **why** a design decision was made, not just **what** was decided.

## 2. Scope

An ADR is required for:

- Architecture changes (Layer Contract, Capability Registry, Domain Model)
- Design decisions with long-term impact
- Decisions that affect multiple layers or modules
- Decisions that set precedent for future decisions

ADRs are **not** required for:

- Routine implementation decisions
- Bug fixes
- Documentation changes
- Performance optimizations without architectural impact

If unsure, write an ADR. It is better to over-document architecture than under-document it.

## 3. When an ADR Is Required

An ADR is required when:

- A decision affects the Architecture Layer
- A decision establishes a new pattern
- A decision changes an existing pattern
- A decision has significant trade-offs
- A decision may be questioned in the future

## 4. ADR Lifecycle

 + "`" + 
Architecture Issue
  ↓
Draft ADR
  ↓
Architecture Review (AR)
  ↓
Accepted / Rejected
  ↓
Implemented
  ↓
Superseded
  ↓
Archived
 + "`" + 

## 5. Architecture Review (AR)

- Chief Architect reviews the ADR
- AR output must be one of: APPROVED, APPROVED WITH CONDITIONS, REQUEST CHANGES, REJECTED
- ADR does not require Community Review
- Review period: minimum 2 days, maximum 7 days

## 6. Decision Criteria

ADR decisions must consider:

- Does this strengthen the Mission?
- Does this align with Canon Principles?
- Does this maintain Layer Contract boundaries?
- What trade-offs are being made?
- What alternatives were rejected and why?

## 7. Recording an ADR

- ADR must be written using the ADR Template
- ADR must include Context, Decision, Rationale, Alternatives, Trade-offs, Consequences
- ADR must be archived in  + "rchitecture/adr/" + 
- Status is set to  + "Draft" +  at creation

## 8. Superseding an ADR

- ADRs may be superseded by newer ADRs
- Status is set to  + "Superseded" + 
- Superseded-By field references the new ADR

## 9. References

- Proposal Policy: governance/policies/proposal-policy.md
- ADR Template: governance/templates/adr-template.md
- RFC Process: governance/processes/rfc.md
- PCP Process: governance/processes/pcp.md
