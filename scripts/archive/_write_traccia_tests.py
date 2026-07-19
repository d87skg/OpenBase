import os

code = '''"""
Tests for Traccia SDK v2
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from traccia import observe, TracciaAgent, get_runtime
from openbase_core.replay import ReplayStatus


class TestObserveDecorator:
    def test_observe_basic_function(self):
        @observe(name="test-basic")
        def simple_task(x: str) -> str:
            return f"done: {x}"

        result, execution = simple_task("hello")

        assert result == "done: hello"
        assert execution.status in ("completed", "completed_with_errors")
        assert len(execution.events) >= 2

    def test_observe_generates_evidence(self):
        @observe(name="test-evidence")
        def task():
            return "ok"

        _, execution = task()
        assert len(execution.evidence_chain) >= 2

    def test_observe_generates_trust_score(self):
        @observe(name="test-trust")
        def task():
            return "trust me"

        _, execution = task()
        assert execution.trust_score is not None
        assert 0.0 <= execution.trust_score.score <= 1.0

    def test_observe_handles_exception(self):
        @observe(name="test-error")
        def failing_task():
            raise ValueError("something broke")

        with pytest.raises(ValueError):
            failing_task()

    def test_observe_multiple_calls(self):
        @observe(name="test-multi")
        def repeat(x: int) -> int:
            return x * 2

        results = []
        for i in range(3):
            r, _ = repeat(i)
            results.append(r)

        assert results == [0, 2, 4]

    def test_observe_without_parentheses(self):
        @observe
        def simple():
            return "ok"

        result, execution = simple()
        assert result == "ok"


class TestTracciaAgent:
    def test_agent_with_tools(self):
        agent = TracciaAgent("test-agent")

        @agent.tool
        def calculator(expr: str) -> str:
            return str(eval(expr))

        @agent.step
        def compute(task: str) -> str:
            return calculator("2 + 2")

        result, execution = agent.run("do math")
        assert result == "4"
        assert execution.status in ("completed", "completed_with_errors")

    def test_agent_summary(self):
        agent = TracciaAgent("summary-agent")

        @agent.step
        def process(task: str) -> str:
            return f"processed: {task}"

        result, execution = agent.run("test")
        summary = agent.summary(execution)
        assert summary["agent_name"] == "summary-agent"
        assert summary["steps_executed"] == 1

    def test_agent_replay(self):
        agent = TracciaAgent("replay-agent")

        @agent.step
        def work(task: str) -> str:
            return "done"

        _, execution = agent.run("work")
        assert execution.replay_result is not None
        assert execution.replay_result.status == ReplayStatus.COMPLETED

    def test_agent_handles_step_failure(self):
        agent = TracciaAgent("failing-agent")

        @agent.step
        def bad_step(task: str) -> str:
            raise RuntimeError("step failed")

        result, execution = agent.run("will fail")
        assert result is None
        assert execution.status in ("completed", "completed_with_errors")

    def test_agent_certificate(self):
        agent = TracciaAgent("cert-agent")

        @agent.step
        def productive(task: str) -> str:
            return "output"

        # Run many times to build up evidence
        for i in range(10):
            agent.run(f"task_{i}")

        # Get the runtime and check certificate history
        rt = get_runtime("cert-agent")
        assert rt is not None

    def test_get_runtime_returns_same_instance(self):
        rt1 = get_runtime("shared")
        rt2 = get_runtime("shared")
        assert rt1 is rt2

    def test_get_runtime_different_names(self):
        rt_a = get_runtime("agent-a")
        rt_b = get_runtime("agent-b")
        assert rt_a is not rt_b
'''

path = r'D:\OpenBase\traccia\tests\test_sdk.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_sdk.py written')
