import os

code = '''"""
OpenBase Registry Engine
"""

from .engine import Registry, RegistryEntry

__all__ = ["Registry", "RegistryEntry"]
'''

path = r'D:\OpenBase\openbase_core\registry\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('registry/__init__.py updated')
