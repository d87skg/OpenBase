# Layer Contract

**Asset-Type:** Architecture
**Category:** Layer Contract
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03

## 1. Identity Layer

**Responsibility:** Defines why OpenBase exists and what it stands for.

**Assets:**
- Charter
- Founding
- Manifesto
- Canon

**Dependency:** None. Identity is the foundation.

---

## 2. Governance Layer

**Responsibility:** Defines how OpenBase is governed.

**Assets:**
- Constitution
- Policies
- Processes
- Templates

**Dependency:** May reference Identity Layer. Must not reference Architecture or Protocol.

---

## 3. Architecture Layer

**Responsibility:** Defines the structural constraints of OpenBase.

**Assets:**
- Layer Contract
- Dependency Rule
- Capability Registry
- Domain Model

**Dependency:** May reference Identity and Governance Layers. Must not reference Protocol or Reference.

---

## 4. Protocol Layer

**Responsibility:** Defines the open specifications (OBP).

**Assets:**
- Evidence Spec
- Execution Semantics
- Verification Protocol

**Dependency:** May reference Architecture, Governance, and Identity Layers. Must not reference Reference.

---

## 5. Reference Layer

**Responsibility:** Implements the Protocol.

**Assets:**
- Python Runtime
- CLI
- SDK
- Adapters

**Dependency:** May reference Protocol, Architecture, Governance, and Identity Layers.

---

## 6. Certification Layer

**Responsibility:** Defines conformance and certification criteria.

**Assets:**
- Conformance Test Suite
- Certification Criteria
- Compatibility Matrix

**Dependency:** May reference Protocol and Reference Layers. Must not depend on Governance or Identity.

---

## 7. Ecosystem Layer

**Responsibility:** Defines external integration and community.

**Assets:**
- Adapters
- SDKs (multi-language)
- Community
- Knowledge

**Dependency:** May reference all layers below.

## Layer Dependency Summary

Identity
   ↓
Governance
   ↓
Architecture
   ↓
Protocol
   ↓
Reference
   ↓
Certification
   ↓
Ecosystem

## Layer Rule

> No layer may depend on a layer above it.
