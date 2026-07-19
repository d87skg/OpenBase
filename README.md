# OpenBase

**The Open Protocol for Verifiable AI Agent Execution Evidence.**

[![Protocol Version](https://img.shields.io/badge/protocol-v2.0.0-blue)](VERSION)
[![Conformance](https://img.shields.io/badge/conformance-268_tests_passing-00AA00)](openbase_core/tests/)
[![Governance](https://img.shields.io/badge/governance-OBEP_active-purple)](openbase-spec/governance/OBEP_PROCESS.md)

---

## What is OpenBase?

OpenBase defines the **standard for AI agent execution evidence** ¡ª what gets recorded, how it's verified, and how trust is certified.

- **OBS (OpenBase Event Specification)**: 23 standard event types ¡ª the common language for agent actions
- **Evidence Protocol**: SHA-256 hash chain + Ed25519 signatures ¡ª tamper-proof execution records
- **Replay Engine**: 4-level fidelity replay ¡ª reconstruct what happened and why
- **Conformance**: Certification badges ¡ª prove your agent is trustworthy

## Quick Start

`ash
# Install the developer SDK
pip install traccia

# Add verifiable execution to any agent
from traccia import observe

@observe
def my_agent(task):
    return agent.run(task)
Ecosystem
ComponentRoleRepository
OpenBaseProtocol & Standardgithub.com/d87skg/openbase
TracciaDeveloper SDKgithub.com/d87skg/traccia
OpenClawReference Runtimegithub.com/d87skg/openclaw
Architecture
text
Framework / Runtime (LangGraph, OpenAI, Claude, CrewAI, OpenClaw)
    ©¦
Traccia Adoption Layer (install ¡ú intercept ¡ú evidence)
    ©¦
OpenBase Protocol (OBS ¡ú Evidence ¡ú Replay ¡ú Conformance)
    ©¦
Trust Layer (Certificate ¡ú Governance ¡ú Compliance) [future]
Governance
OpenBase follows the OBEP (OpenBase Enhancement Proposal) process. Breaking changes to the Stable Core require formal proposal, community review, and maintainer vote.

OBEP Process ¡ú

License
MIT
