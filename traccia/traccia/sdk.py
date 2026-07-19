"""
Traccia SDK v2
One-line OpenBase integration for any Python Agent.
"""

import functools
import inspect
from typing import Any, Callable, Optional, Dict
from datetime import datetime, timezone

from openbase_core.registry import OpenBaseRuntime, RuntimeConfig, ExecutionResult


# Global runtime registry
_runtimes: Dict[str, OpenBaseRuntime] = {}


def get_runtime(name: str = "default") -> OpenBaseRuntime:
    """Get or create an OpenBaseRuntime."""
    if name not in _runtimes:
        config = RuntimeConfig(
            agent_id=f"agent.traccia.{name}",
            runtime_name="traccia-sdk",
            runtime_version="2.0.0",
        )
        _runtimes[name] = OpenBaseRuntime(config)
    return _runtimes[name]


def observe(func=None, *, name: str = "default", track_args: bool = True):
    """Decorator that wraps any function with OpenBase tracing.

    Usage:
        from traccia_sdk import observe

        @observe
        def my_agent(task: str):
            return process(task)

        result = my_agent("do something")
        # Automatically generates: Event -> Evidence -> Trust -> Certificate

    Args:
        func: The function to decorate.
        name: Runtime name for this agent.
        track_args: Whether to include function arguments in events.

    Returns:
        Wrapped function that returns (original_result, ExecutionResult).
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            rt = get_runtime(name)

            # Emit agent_started
            task_info = {}
            if track_args:
                task_info["args"] = str(args)[:200]
                task_info["kwargs"] = str(kwargs)[:200]
            task_info["function"] = fn.__name__

            rt.agent_started(fn.__name__)

            # Execute the original function
            try:
                result = fn(*args, **kwargs)
                rt.agent_finished({"result": str(result)[:500]})
                execution = rt.finish()
                return result, execution
            except Exception as e:
                rt.agent_failed(str(e))
                execution = rt.finish()
                raise

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


class TracciaAgent:
    """High-level Agent builder with automatic OpenBase tracing.

    Usage:
        from traccia_sdk import TracciaAgent

        agent = TracciaAgent("my-agent")

        @agent.tool
        def search(query: str) -> str:
            return f"Results for {query}"

        @agent.step
        def research(topic: str) -> str:
            return search(f"{topic} papers")

        result, cert = agent.run("research AI safety")
    """

    def __init__(self, name: str = "traccia-agent", verbose: bool = False):
        self.name = name
        self.verbose = verbose
        self._tools: Dict[str, Callable] = {}
        self._steps: list = []
        self._rt = get_runtime(name)

    def tool(self, func: Callable) -> Callable:
        """Register a function as a tool."""
        self._tools[func.__name__] = func
        return func

    def step(self, func: Callable) -> Callable:
        """Register a function as an agent step."""
        self._steps.append(func)
        return func

    def run(self, task: str) -> tuple:
        """Execute the agent with full OpenBase tracing.

        Args:
            task: The task description.

        Returns:
            Tuple of (final_result, ExecutionResult).
        """
        if self.verbose:
            print(f"[Traccia] Agent '{self.name}' starting: {task}")

        self._rt.agent_started(task)

        result = None
        for step_fn in self._steps:
            if self.verbose:
                print(f"[Traccia] Step: {step_fn.__name__}")

            # Emit step as tool_call
            self._rt.tool_call(step_fn.__name__, {"task": task})

            try:
                result = step_fn(task)
                self._rt.tool_result(step_fn.__name__, {"result": str(result)[:200]})
            except Exception as e:
                self._rt.tool_error_event(step_fn.__name__, str(e))
                self._rt.agent_failed(str(e))
                execution = self._rt.finish()
                if self.verbose:
                    print(f"[Traccia] Failed: {e}")
                return None, execution

        self._rt.agent_finished({"final_result": str(result)[:200] if result else None})
        execution = self._rt.finish()

        if self.verbose and execution.trust_score:
            print(f"[Traccia] Trust: {execution.trust_score.score:.2f}")
            if execution.certificate:
                print(f"[Traccia] Certificate: {execution.certificate.level}")

        return result, execution

    def summary(self, execution: ExecutionResult) -> Dict[str, Any]:
        """Get a human-readable summary of the execution."""
        s = execution.to_summary()
        s["agent_name"] = self.name
        s["tools_registered"] = len(self._tools)
        s["steps_executed"] = len(self._steps)
        return s


def quick_start():
    """Print quick start guide."""
    print("""
    Traccia SDK v2 — Quick Start
    ============================

    from traccia_sdk import observe

    @observe
    def my_agent(task: str) -> str:
        return f"Completed: {task}"

    result, execution = my_agent("hello world")
    print(f"Result: {result}")
    print(f"Trust: {execution.trust_score.score}")
    print(f"Evidence: {len(execution.evidence_chain)} events")
    """)
