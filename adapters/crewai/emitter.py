"""
CrewAI Emitter
Wraps CrewAI multi-agent execution with OpenBase tracing.
"""

from adapters.base_emitter import BaseEmitter


class CrewAIEmitter(BaseEmitter):
    """Emitter for CrewAI multi-agent systems.

    Usage:
        emitter = CrewAIEmitter(agent_id="crew.research")
        emitter.on_start("execute crew task")
        emitter.on_agent_delegate("researcher", "search AI safety")
        emitter.on_tool_call("web_search", {"query": "AI"})
        emitter.on_tool_result("web_search", "results")
        emitter.on_finish("Crew task complete")
        result = emitter.finish()
    """

    def __init__(self, agent_id: str = "crew.default"):
        super().__init__("crewai", agent_id=agent_id)

    def on_agent_delegate(self, target_agent: str, task: str):
        """Capture agent-to-agent delegation."""
        return self.on_tool_call(f"delegate:{target_agent}", {"task": task})
