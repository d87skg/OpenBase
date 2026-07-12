import os

code = '''"""
OpenClaw Reference Runtime
Reference implementation of the OpenBase protocol stack.
"""

from .agent.engine import OpenClawAgent, AgentConfig
from .tools.registry import ToolRegistry, Tool, ReadFileTool, WriteFileTool, ShellTool

__all__ = [
    "OpenClawAgent",
    "AgentConfig",
    "ToolRegistry",
    "Tool",
    "ReadFileTool",
    "WriteFileTool",
    "ShellTool",
]
'''

path = r'D:\OpenBase\openclaw\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('openclaw/__init__.py updated')
