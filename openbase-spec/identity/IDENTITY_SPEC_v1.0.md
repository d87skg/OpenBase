# OpenBase Identity Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Identity Layer defines the canonical identity model for all entities that produce or consume events in the OpenBase protocol stack.

Every OBS Event has an actor field. This specification defines what actors are, how they are identified, and how identities are verified.

## 2. Identity Model

### 2.1 Core Principle

An Identity is a stable, verifiable identifier for an entity in the Agent execution ecosystem. Identities are globally unique and immutable.

### 2.2 Actor Types

| Type | Description | Example ID |
|:---|:---|:---|
| agent | An AI agent instance | agent.acme.research-bot |
| runtime | Execution environment | runtime.openhands.0.15.0 |
| model | AI model identifier | model.anthropic.claude-sonnet-4 |
| tool | A tool or plugin | tool.filesystem.read |
| human | A human operator | human.alice@acme.com |
| system | Infrastructure component | system.scheduler.main |

### 2.3 Identity Format

<type>.<namespace>.<name>

Examples:
- agent.openclaw.demo-assistant
- runtime.langgraph.v0.3
- model.openai.gpt-5
- tool.github.create-issue

## 3. Identity Lifecycle

Created -> Registered -> Active -> Deprecated -> Retired

- Created: Identity claimed by entity
- Registered: Identity published to Registry
- Active: Identity in operational use
- Deprecated: Identity still valid but superseded
- Retired: Identity no longer valid

## 4. Identity Verification

Identities are verified through:
1. Public Key: Each identity has an Ed25519 key pair
2. Registry Lookup: Identities are resolvable via Registry
3. Chain of Trust: Parent runtime vouches for child agents

## 5. References

- OBS v1.0 (Event actor field)
- Registry v1.0 (Identity registration)
- Certificate v1.0 (Identity attestation)
