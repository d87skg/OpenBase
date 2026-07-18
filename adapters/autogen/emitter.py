"""
AutoGen Emitter
Wraps AutoGen conversational agent execution with OpenBase tracing.
"""

from adapters.base_emitter import BaseEmitter


class AutoGenEmitter(BaseEmitter):
    """Emitter for AutoGen multi-agent conversations.

    Usage:
        emitter = AutoGenEmitter(agent_id="agent.autogen.demo")
        emitter.on_start("start conversation")
        emitter.on_llm_request("gpt-5", [{"role": "user", "content": "..."}])
        emitter.on_llm_response("I think we should...")
        emitter.on_finish("Conversation complete")
        result = emitter.finish()
    """

    def __init__(self, agent_id: str = "agent.autogen.default"):
        super().__init__("autogen", agent_id=agent_id)

    def on_message(self, sender: str, receiver: str, content: str):
        """Capture inter-agent message."""
        return self.on_tool_call(f"message:{sender}->{receiver}", {"content": content[:200]})
