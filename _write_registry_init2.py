import os

code = '''"""
OpenBase Registry Engine
"""

from .engine import Registry, RegistryEntry
from .runtime import OpenBaseRuntime, RuntimeConfig, ExecutionResult

__all__ = [
    "Registry",
    "RegistryEntry",
    "OpenBaseRuntime",
    "RuntimeConfig",
    "ExecutionResult",
]
'''

path = r'D:\OpenBase\openbase_core\registry\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('registry/__init__.py updated with Runtime')
