# Traccia SDK

**One-line OpenBase integration for AI Agents.**

 `python
from traccia import observe

@observe
def my_agent(task: str) -> str:
    return f"Done: {task}"

result, execution = my_agent("hello world")
print(f"Trust: {execution.trust_score.score}")
 `

## Install

 `bash
pip install traccia
 `

## Quick Start

 `python
from traccia import TracciaAgent

agent = TracciaAgent("my-agent")

@agent.step
def research(topic: str) -> str:
    return f"Research on {topic}"

result, execution = agent.run("AI safety")
 `

## CLI

 `bash
traccia init
traccia run app.py
traccia replay
traccia verify
 `

## Powered by OpenBase

Traccia is the developer SDK for OpenBase, the Open Protocol Stack for Trusted AI Agent Interoperability.

## License

MIT
