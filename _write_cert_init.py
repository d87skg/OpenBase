import os

code = '''"""
OpenBase Certificate Engine
Certificate v1.0 Implementation
"""

from .engine import Certificate, CertificateEngine

__all__ = [
    "Certificate",
    "CertificateEngine",
]
'''

path = r'D:\OpenBase\openbase_core\certificate\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('certificate/__init__.py updated')
