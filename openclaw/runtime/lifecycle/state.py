#!/usr/bin/env python3
"""
Runtime Lifecycle States
"""

from enum import Enum, auto
from typing import Optional


class RuntimeState(Enum):
    """Runtime 生命周期状态"""

    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    EMITTING = "EMITTING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class StateTransition:
    """状态转换规则"""

    ALLOWED_TRANSITIONS = {
        RuntimeState.CREATED: [RuntimeState.INITIALIZING],
        RuntimeState.INITIALIZING: [RuntimeState.RUNNING, RuntimeState.FAILED],
        RuntimeState.RUNNING: [RuntimeState.EMITTING, RuntimeState.FINISHED, RuntimeState.FAILED],
        RuntimeState.EMITTING: [RuntimeState.FINISHED, RuntimeState.FAILED],
        RuntimeState.FINISHED: [],
        RuntimeState.FAILED: [],
    }

    @classmethod
    def can_transition(cls, from_state: RuntimeState, to_state: RuntimeState) -> bool:
        return to_state in cls.ALLOWED_TRANSITIONS.get(from_state, [])

    @classmethod
    def validate(cls, from_state: RuntimeState, to_state: RuntimeState) -> None:
        if not cls.can_transition(from_state, to_state):
            raise ValueError(
                f"❌ 非法状态转换: {from_state.value} → {to_state.value}"
            )