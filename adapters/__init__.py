"""
OpenBase Adapters — Framework/Runtime Emitters

Each adapter wraps a specific Agent framework with OpenBase tracing.
All adapters share the same BaseEmitter interface.

Available adapters:
    - OpenAIEmitter (OpenAI Agents SDK)
    - LangChainEmitter (LangChain)
    - LangGraphEmitter (LangGraph)
    - CrewAIEmitter (CrewAI)
    - ClaudeCodeEmitter (Claude Code)
    - AutoGenEmitter (AutoGen)
    - OpenHandsAdapter (OpenHands — existing)

Usage:
    from adapters.openai import OpenAIEmitter
    emitter = OpenAIEmitter()
    emitter.on_start("task")
    emitter.on_finish("done")
    result = emitter.finish()
"""

from .base_emitter import BaseEmitter

__all__ = ["BaseEmitter"]
