# Domain Model

**Asset-Type:** Architecture
**Category:** Domain Model
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03

## Core Value Chain

Execution
   ↓
Evidence
   ↓
Verification
   ↓
Trust
   ↓
Certification

This is the OpenBase value chain. Every component exists to support this chain.

## Core Concepts

### Agent
An entity that performs autonomous tasks.

**Relationships:**
- Agent executes an Execution
- Agent produces Evidence
- Agent is subject to Verification

### Execution
A complete run of an Agent from start to finish.

**Relationships:**
- Execution produces Evidence
- Execution can be replayed
- Execution can be verified

### Evidence
A standardized record of execution facts.

**Relationships:**
- Evidence is produced by Execution
- Evidence is verified by Verification
- Evidence supports Audit
- Evidence forms a chain (Merkle/signature)

### Verification
The process of independently validating Evidence.

**Relationships:**
- Verification validates Evidence
- Verification supports Trust
- Verification is part of Certification

### Replay
The reconstruction of an Execution from Evidence.

**Relationships:**
- Replay uses Evidence
- Replay reconstructs Execution
- Replay supports Verification

### Audit
A review of Evidence for compliance or trust purposes.

**Relationships:**
- Audit uses Evidence
- Audit supports Governance
- Audit is part of Certification

### Trust
Confidence based on verifiable Evidence, not reputation.

**Relationships:**
- Trust is built on Verification
- Trust is used by Governance
- Trust is part of Certification

### Protocol
An open specification independent of any implementation.

**Relationships:**
- Protocol defines Evidence format
- Protocol defines Execution semantics
- Protocol defines Verification method

### Reference Implementation
The official implementation of the Protocol.

**Relationships:**
- Reference implements Protocol
- Reference is verified by Certification
- Reference includes Runtime, SDK, CLI

## Conceptual Map

Agent
  |
  +-- executes -> Execution
  |               |
  |               +-- produces -> Evidence
  |               |               |
  |               |               +-- verified by -> Verification
  |               |               |               |
  |               |               |               +-- supports -> Trust
  |               |               |               |
  |               |               |               +-- used by -> Certification
  |               |               |
  |               |               +-- used by -> Replay
  |               |               |
  |               |               +-- used by -> Audit
  |               |
  |               +-- defined by -> Protocol
  |
  +-- governed by -> Governance
  |
  +-- implemented by -> Reference Implementation
