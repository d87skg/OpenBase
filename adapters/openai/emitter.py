"""
OpenAI Agents SDK Emitter
Wraps OpenAI Agents SDK with OpenBase tracing.
"""

from typing import Dict, Any, Optional
from adapters.base_emitter import BaseEmitter


class OpenAIEmitter(BaseEmitter):
    """Emitter for OpenAI Agents SDK.

    Usage:
        emitter = OpenAIEmitter(agent_id="agent.openai.demo")

        # Wrap your agent execution:
        emitter.on_start("research AI safety")
        emitter.on_tool_call("web_search", {"query": "AI safety"})
        emitter.on_tool_result("web_search", "Found 10 papers")
        emitter.on_llm_request("gpt-5", [{"role": "user", "content": "..."}])
        emitter.on_llm_response("Based on the research...")
        emitter.on_finish("Research complete")

        result = emitter.finish()
        print(result.trust_score.score)
    """

    def __init__(self, agent_id: str = "agent.openai.default"):
        super().__init__("openai-agents-sdk", agent_id=agent_id)
