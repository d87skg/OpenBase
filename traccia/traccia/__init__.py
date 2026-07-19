"""
Traccia SDK v2.0
Official Developer SDK for OpenBase — Add verifiable execution to any AI agent.

Quick Start:
    from traccia_sdk import observe

    @observe
    def my_agent(task):
        return agent.run(task)

    result, execution = my_agent("hello world")
    print(f"Trust: {execution.trust_score.score}")
"""

from .sdk import observe, TracciaAgent, get_runtime, quick_start
from .session.manager import Session, SessionStatus
from .renderer.timeline import TimelineRenderer
from .package.exporter import export_package
from .openbase_adapter import to_obs, is_valid_obs, OpenBaseSignerBridge

__version__ = "2.0.0"
__all__ = [
    "observe",
    "TracciaAgent",
    "get_runtime",
    "quick_start",
    "Session",
    "SessionStatus",
    "TimelineRenderer",
    "export_package",
    "to_obs",
    "is_valid_obs",
    "OpenBaseSignerBridge",
]
