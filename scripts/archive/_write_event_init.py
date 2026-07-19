import os

code = '''"""
OpenBase Event Engine
OBS v1.0 Implementation
"""

from .models import Event, Actor, ActorType, Runtime, EventType, StateTransition
from .factory import EventFactory
from .validator import EventValidator
from .serializer import EventSerializer

__all__ = [
    "Event",
    "Actor",
    "ActorType",
    "Runtime",
    "EventType",
    "StateTransition",
    "EventFactory",
    "EventValidator",
    "EventSerializer",
]
'''

path = r'D:\OpenBase\openbase-core\event\__init__.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('__init__.py updated')
