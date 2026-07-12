"""
Tests for OpenClaw Reference Runtime
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
import tempfile
from openclaw import OpenClawAgent, AgentConfig, ToolRegistry, ReadFileTool, WriteFileTool, ShellTool
from openbase_core.replay import ReplayStatus


class TestTools:
    def test_read_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("hello world")
            tmp_path = f.name
        try:
            tool = ReadFileTool()
            result = tool.execute(path=tmp_path)
            assert result.success is True
            assert result.result == "hello world"
        finally:
            os.unlink(tmp_path)

    def test_read_file_not_found(self):
        tool = ReadFileTool()
        result = tool.execute(path="/nonexistent/path/file.txt")
        assert result.success is False

    def test_write_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            tmp_path = f.name
        try:
            tool = WriteFileTool()
            result = tool.execute(path=tmp_path, content="new content")
            assert result.success is True
            with open(tmp_path, 'r') as f:
                assert f.read() == "new content"
        finally:
            os.unlink(tmp_path)

    def test_shell_tool_echo(self):
        tool = ShellTool()
        result = tool.execute(command="echo hello")
        assert result.success is True
        assert "hello" in result.result

    def test_tool_registry(self):
        reg = ToolRegistry()
        reg.register(ReadFileTool())
        reg.register(ShellTool())
        tools = reg.list_tools()
        assert len(tools) == 2
        assert tools[0]["name"] == "read_file"

    def test_tool_registry_execute(self):
        reg = ToolRegistry()
        reg.register(ShellTool())
        result = reg.execute("shell", command="echo test")
        assert result.success is True


class TestOpenClawAgent:
    def test_agent_run_task(self):
        agent = OpenClawAgent(AgentConfig(name="test-agent", verbose=False))
        result = agent.run("shell echo hello")
        assert result.status in ("completed", "completed_with_errors")
        assert len(result.events) >= 2

    def test_agent_produces_evidence(self):
        agent = OpenClawAgent(AgentConfig(name="evidence-test"))
        result = agent.run("shell echo test")
        chain = agent.ob_runtime.get_evidence_chain()
        assert len(chain) >= 2

    def test_agent_trust_score(self):
        agent = OpenClawAgent(AgentConfig(name="trust-test"))
        # Use newlines as separate task lines
        task = "shell echo step1\nshell echo step2\nshell echo step3"
        result = agent.run(task)
        assert result.trust_score is not None
        assert result.trust_score.score > 0.0

    def test_agent_replay(self):
        agent = OpenClawAgent(AgentConfig(name="replay-test"))
        result = agent.run("shell echo hello")
        assert result.replay_result is not None
        assert result.replay_result.status == ReplayStatus.COMPLETED

    def test_agent_with_file_operations(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("original")
            tmp_path = f.name
        try:
            agent = OpenClawAgent(AgentConfig(name="file-test"))
            result = agent.run(f"read {tmp_path}")
            assert result.status in ("completed", "completed_with_errors")
        finally:
            os.unlink(tmp_path)

    def test_agent_summary(self):
        agent = OpenClawAgent(AgentConfig(name="summary-test"))
        result = agent.run("shell echo hello")
        summary = agent.get_summary(result)
        assert summary["agent_name"] == "summary-test"
        assert summary["event_count"] >= 2

    def test_agent_max_steps(self):
        agent = OpenClawAgent(AgentConfig(name="limit-test", max_steps=2))
        result = agent.run("shell echo 1\nshell echo 2\nshell echo 3\nshell echo 4")
        assert result.status in ("completed", "completed_with_errors")

    def test_agent_list_tools(self):
        agent = OpenClawAgent()
        tools = agent.get_tools()
        assert len(tools) == 3

    def test_agent_empty_task_raises(self):
        agent = OpenClawAgent(AgentConfig(name="error-test", task=""))
        with pytest.raises(ValueError):
            agent.run()
