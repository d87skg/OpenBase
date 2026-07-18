"""
Claude Code Emitter
Wraps Claude Code agent execution with OpenBase tracing.
"""

from adapters.base_emitter import BaseEmitter


class ClaudeCodeEmitter(BaseEmitter):
    """Emitter for Claude Code.

    Usage:
        emitter = ClaudeCodeEmitter(agent_id="agent.claude.demo")
        emitter.on_start("edit main.py")
        emitter.on_file_read("/workspace/main.py")
        emitter.on_tool_call("edit_file", {"path": "/workspace/main.py"})
        emitter.on_file_write("/workspace/main.py")
        emitter.on_finish("Edit complete")
        result = emitter.finish()
    """

    def __init__(self, agent_id: str = "agent.claude.default"):
        super().__init__("claude-code", agent_id=agent_id)

    def on_command_execute(self, command: str, output: str = ""):
        """Capture shell command execution."""
        return self.on_tool_call("shell", {"command": command, "output": output[:200]})
