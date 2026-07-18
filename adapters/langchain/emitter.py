"""
LangChain Emitter
Wraps LangChain agent execution with OpenBase tracing.
"""

from adapters.base_emitter import BaseEmitter


class LangChainEmitter(BaseEmitter):
    """Emitter for LangChain.

    Usage:
        emitter = LangChainEmitter(agent_id="agent.langchain.demo")
        emitter.on_start("execute chain")
        emitter.on_tool_call("calculator", {"expression": "2+2"})
        emitter.on_tool_result("calculator", 4)
        emitter.on_finish("Chain complete")
        result = emitter.finish()
    """

    def __init__(self, agent_id: str = "agent.langchain.default"):
        super().__init__("langchain", agent_id=agent_id)
