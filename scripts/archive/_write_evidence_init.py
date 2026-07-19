import os

code = '''"""
OpenBase Evidence Engine
Evidence v2.0 Implementation
"""

from .models import Evidence, Causal
from .signer import EvidenceSigner

__all__ = [
    "Evidence",
    "Causal",
    "EvidenceSigner",
]
'''

path = r'D:\OpenBase\openbase_core\evidence\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('evidence/__init__.py updated')
