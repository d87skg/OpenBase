"""
LangGraph Emitter
Wraps LangGraph graph execution with OpenBase tracing.
"""

from adapters.base_emitter import BaseEmitter


class LangGraphEmitter(BaseEmitter):
    """Emitter for LangGraph.

    Captures node transitions and state changes as OpenBase events.

    Usage:
        emitter = LangGraphEmitter(agent_id="agent.langgraph.demo")
        emitter.on_start("execute graph workflow")
        emitter.on_tool_call("search_node", {"query": "AI"})
        emitter.on_tool_result("search_node", "results")
        emitter.on_finish("Graph execution complete")
        result = emitter.finish()
    """

    def __init__(self, agent_id: str = "agent.langgraph.default"):
        super().__init__("langgraph", agent_id=agent_id)

    def on_node_enter(self, node_name: str, state: dict = None):
        """Capture graph node entry."""
        return self.on_tool_call(f"node:{node_name}", {"state": state or {}})

    def on_node_exit(self, node_name: str, result: dict = None):
        """Capture graph node exit."""
        return self.on_tool_result(f"node:{node_name}", result or {})
