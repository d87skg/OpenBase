import os

code = '''"""
OpenClaw Tool System
Minimal tool execution with OpenBase evidence generation.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ToolResult:
    """Result of a tool execution."""
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "success": self.success,
            "result": self.result,
            "error": self.error,
        }


class Tool:
    """Base class for OpenClaw tools."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError


class ReadFileTool(Tool):
    """Tool for reading files."""
    
    def __init__(self):
        super().__init__("read_file", "Read contents of a file")

    def execute(self, path: str, **kwargs) -> ToolResult:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return ToolResult(tool_name=self.name, success=True, result=content)
        except Exception as e:
            return ToolResult(tool_name=self.name, success=False, error=str(e))


class WriteFileTool(Tool):
    """Tool for writing files."""
    
    def __init__(self):
        super().__init__("write_file", "Write content to a file")

    def execute(self, path: str, content: str, **kwargs) -> ToolResult:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return ToolResult(tool_name=self.name, success=True, result=f"Written to {path}")
        except Exception as e:
            return ToolResult(tool_name=self.name, success=False, error=str(e))


class ShellTool(Tool):
    """Tool for executing shell commands."""
    
    def __init__(self):
        super().__init__("shell", "Execute a shell command")

    def execute(self, command: str, **kwargs) -> ToolResult:
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout if result.returncode == 0 else result.stderr
            return ToolResult(
                tool_name=self.name,
                success=result.returncode == 0,
                result=output,
                error=result.stderr if result.returncode != 0 else None,
            )
        except Exception as e:
            return ToolResult(tool_name=self.name, success=False, error=str(e))


class ToolRegistry:
    """Registry of available tools."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> list:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        tool = self.get(tool_name)
        if tool is None:
            return ToolResult(tool_name=tool_name, success=False, error=f"Tool not found: {tool_name}")
        return tool.execute(**kwargs)
'''

path = r'D:\OpenBase\openclaw\tools\registry.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('tools/registry.py written')
