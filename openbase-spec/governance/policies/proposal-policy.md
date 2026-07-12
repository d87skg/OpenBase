# Proposal Policy

**Asset-Type:** Governance
**Category:** Policy
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03
**Owner:** Chief Architect
**Reviewer:** Protocol Steward

---

## 1. Purpose

This policy defines when a proposal is required, who can submit, who approves, the lifecycle of a proposal, and how it is archived.

It applies to all proposal types, including:

- RFC (Request for Comments)
- ADR (Architecture Decision Record)
- PCP (Protocol Change Proposal)
- Any future proposal format

## 2. When a Proposal Is Required

A proposal is required when a change affects any of the following:

- Protocol specification (Evidence, Execution, Verification)
- Architecture (Layer Contract, Capability Registry, Domain Model)
- Governance (Constitution, Policy, Process)
- Public API or SDK interface
- Certification or Conformance criteria
- Stability, Compatibility, or Versioning policy

A proposal is **not** required for:

- Bug fixes that do not change behavior
- Documentation improvements
- Test additions
- Internal refactoring with no external impact

If unsure, file a proposal. It is better to over-document than under-document.

## 3. Who Can Submit

Anyone can submit a proposal.

- Contributors may submit RFCs and ADRs
- Maintainers may submit PCPs and Policy changes
- Chief Architect may submit Architecture changes
- Protocol Steward may submit Constitutional changes

## 4. Who Approves

| Change Type | Approver |
| :--- | :--- |
| Protocol Change | Protocol Steward + Chief Architect |
| Architecture Change | Chief Architect |
| Governance Change | Protocol Steward |
| Policy Change | Chief Architect |
| Release Decision | Maintainer |
| Certification Change | Protocol Steward |

## 5. Proposal Lifecycle

All proposals follow the same lifecycle:

 + "`" + 
Draft
   ↓
Review
   ↓
Accepted
   ↓
Implemented
   ↓
Released
   ↓
Deprecated
   ↓
Archived
 + "`" + 

### 5.1 Draft

- Author writes the proposal using the appropriate template
- Proposal is submitted as a PR or issue
- Status is set to  + "Draft" + 

### 5.2 Review

- Proposal enters review period (minimum 5 days for RFCs, 3 days for ADRs)
- Comments are collected from the community
- Author may revise the proposal based on feedback
- Status is set to  + "Review" + 

### 5.3 Accepted

- Approver(s) accept the proposal
- Status is set to  + "Accepted" + 
- Implementation may begin

### 5.4 Implemented

- Implementation is complete
- Tests are added
- Documentation is updated
- Status is set to  + "Implemented" + 

### 5.5 Released

- Implementation is included in a release
- Status is set to  + "Released" + 

### 5.6 Deprecated

- Proposal is superseded by a newer proposal
- Status is set to  + "Deprecated" + 
- Replacement proposal is referenced

### 5.7 Archived

- Proposal is no longer relevant
- Status is set to  + "Archived" + 
- Moved to archive/ directory

## 6. Proposal Types

| Type | Purpose | Template |
| :--- | :--- | :--- |
| RFC | New capability or major change | rfc-template.md |
| ADR | Architecture decision | adr-template.md |
| PCP | Protocol specification change | pcp-template.md |
| AR | Architecture review (internal) | ar-template.md |

## 7. Versioning

All proposals must include a version number.

- Initial version: 0.1.0
- Accepted version: 1.0.0
- Minor changes: increment minor version
- Major changes: increment major version

## 8. Archiving

Proposals are archived when:

- They are Deprecated
- They are Rejected
- They are Superseded

Archived proposals are moved to  + "rchive/" +  with a README explaining the reason.

## 9. Governance References

- Constitution: governance/constitution.md
- RFC Process: governance/processes/rfc.md
- ADR Process: governance/processes/adr.md
- PCP Process: governance/processes/pcp.md
