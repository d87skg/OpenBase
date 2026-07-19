import os

code = '''"""
OpenClaw Agent — Reference Runtime for OpenBase.
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from openclaw.tools.registry import ToolRegistry, ToolResult
from openbase_core.registry import OpenBaseRuntime, RuntimeConfig, ExecutionResult


@dataclass
class AgentConfig:
    name: str = "openclaw-agent"
    task: str = ""
    max_steps: int = 10
    verbose: bool = False


class OpenClawAgent:
    def __init__(self, config=None, tool_registry=None):
        self.config = config or AgentConfig()
        self.tools = tool_registry or self._default_tools()
        runtime_config = RuntimeConfig(
            agent_id=f"agent.openclaw.{self.config.name}",
            runtime_name="openclaw",
            runtime_version="1.0.0",
        )
        self.ob_runtime = OpenBaseRuntime(runtime_config)
        self._step_count = 0
        self._history: List[Dict[str, Any]] = []

    @staticmethod
    def _default_tools():
        from openclaw.tools.registry import ReadFileTool, WriteFileTool, ShellTool
        reg = ToolRegistry()
        reg.register(ReadFileTool())
        reg.register(WriteFileTool())
        reg.register(ShellTool())
        return reg

    def run(self, task=None):
        task = task or self.config.task
        if not task:
            raise ValueError("No task specified")
        if self.config.verbose:
            print(f"OpenClaw [{self.config.name}] task: {task}")
        self.ob_runtime.agent_started(task)
        self._execute_task(task)
        self.ob_runtime.agent_finished({"steps": self._step_count, "history": self._history})
        result = self.ob_runtime.finish()
        if self.config.verbose:
            print(f"Done in {self._step_count} steps")
            if result.trust_score:
                print(f"Trust: {result.trust_score.score:.2f}")
            if result.certificate:
                print(f"Cert: {result.certificate.level}")
        return result

    def _execute_task(self, task):
        self._step_count = 0
        for line in task.strip().split("\\n"):
            if self._step_count >= self.config.max_steps:
                break
            self._step_count += 1
            self._process_instruction(line.strip())

    def _process_instruction(self, instruction):
        if not instruction:
            return
        parts = instruction.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == "read":
            path = arg.strip()
            self.ob_runtime.tool_call("read_file", {"path": path})
            r = self.tools.execute("read_file", path=path)
            self.ob_runtime.tool_result("read_file", r.to_dict())
            self._history.append({"tool": "read_file", "path": path, "success": r.success})
        elif cmd == "write":
            wp = arg.split(" ", 1)
            if len(wp) >= 2:
                p, c = wp[0], wp[1]
                self.ob_runtime.tool_call("write_file", {"path": p, "content": c})
                r = self.tools.execute("write_file", path=p, content=c)
                self.ob_runtime.tool_result("write_file", r.to_dict())
                self._history.append({"tool": "write_file", "path": p, "success": r.success})
        elif cmd == "shell":
            self.ob_runtime.tool_call("shell", {"command": arg})
            r = self.tools.execute("shell", command=arg)
            self.ob_runtime.tool_result("shell", r.to_dict())
            self._history.append({"tool": "shell", "command": arg, "success": r.success})
        elif cmd == "think":
            self.ob_runtime.llm_request("claude-sonnet-4", [{"role": "user", "content": arg}])
            self._history.append({"tool": "think", "thought": arg})
        else:
            self._history.append({"tool": "unknown", "instruction": instruction})

    def get_tools(self):
        return self.tools.list_tools()

    def get_summary(self, result):
        s = result.to_summary()
        s["agent_name"] = self.config.name
        s["tools_used"] = len(set(h.get("tool", "") for h in self._history))
        return s
'''

path = r'D:\OpenBase\openclaw\agent\engine.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('agent/engine.py written')
