# RFC Process

**Asset-Type:** Governance
**Category:** Process
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** proposal-policy.md

---

## 1. Purpose

This document defines how a Request for Comments (RFC) becomes part of OpenBase.

## 2. Scope

An RFC is required for:

- New capabilities
- Major changes to existing capabilities
- Changes to Architecture that are not Protocol-level
- Changes to Governance policies or processes

For Protocol-level changes, use PCP instead.

## 3. RFC Lifecycle

 + "`" + 
Idea
  ↓
Draft RFC
  ↓
Architecture Review (AR)
  ↓
Community Review
  ↓
Accepted / Rejected
  ↓
Implementation
  ↓
Release
  ↓
Superseded / Archived
 + "`" + 

## 4. Submission

- Author writes RFC using the RFC Template
- RFC is submitted as a PR to the  + "fc/" +  directory
- PR is labeled  + "fc" + 
- Status is set to  + "Draft" + 

## 5. Architecture Review (AR)

- Chief Architect reviews the RFC for architectural fit
- AR must be completed before Community Review begins
- If AR is rejected, the RFC is closed

## 6. Community Review

- Review period: 5 days minimum, 14 days maximum
- Comments are collected from the community
- Author may revise the RFC based on feedback
- Status is set to  + "Review" + 

## 7. Decision

- Approver decides to Accept or Reject
- Accept criteria:
  - AR approved
  - Community consensus reached (or no unresolved objections)
  - Feasibility confirmed
- If Rejected, the RFC is closed and archived

## 8. Implementation

- Accepted RFCs enter implementation phase
- Status is set to  + "Implemented" + 
- Tests and documentation are required

## 9. Release

- Implemented RFCs are included in a Release
- Status is set to  + "Released" + 

## 10. Superseding an RFC

- RFCs may be superseded by newer RFCs
- Status is set to  + "Superseded" + 
- Superseded-By field references the new RFC

## 11. References

- Proposal Policy: governance/policies/proposal-policy.md
- RFC Template: governance/templates/rfc-template.md
- ADR Process: governance/processes/adr.md
- PCP Process: governance/processes/pcp.md
