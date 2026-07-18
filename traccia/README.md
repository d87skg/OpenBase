# Traccia SDK

**Official Developer SDK for OpenBase — Add verifiable execution to any AI agent in 5 lines.**

[![PyPI](https://img.shields.io/badge/pypi-traccia_sdk-blue)](https://pypi.org/project/traccia-sdk/)
[![OpenBase](https://img.shields.io/badge/OpenBase-Compatible-00AA00)](https://github.com/d87skg/openbase)

## Install

`ash
pip install traccia
Quick Start
python
from traccia import observe

@observe
def my_agent(task: str) -> str:
    return f"Done: {task}"

result, execution = my_agent("hello world")
print(f"Trust: {execution.trust_score.score:.2f}")
print(f"Certificate: {execution.certificate.level}")
Features
@observe: One-line decorator — automatic Event → Evidence → Trust → Certificate

Session: Manage agent execution sessions with full traceability

Timeline Renderer: Convert evidence to human-readable text/markdown/json

Package Export: Export .evidence ZIP packages for audit

OpenBase Adapter: Automatic conversion to OBS 23 standard event types

CLI
bash
traccia intercept app.py     # Record agent execution
traccia diagnose evidence/   # Analyze execution trace
traccia guard --policy rule.yaml  # Security policy gateway
Architecture
text
Your Agent Code
    │
    ▼
Traccia (@observe / Session / Adapter)
    │
    ▼
OpenBase Protocol (OBS → Evidence → Replay → Certificate)
Powered by OpenBase
Traccia is the adoption engine for OpenBase, the open protocol stack for trusted AI agent interoperability.

License
MIT
