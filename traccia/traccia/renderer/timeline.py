"""
Timeline Renderer
Converts OpenBase evidence chain to human-readable timelines.
"""

from typing import Dict, Any, List
from datetime import datetime

EVENT_LABELS_ZH = {
    "AGENT_STARTED": "Agent 启动",
    "AGENT_FINISHED": "Agent 完成",
    "AGENT_FAILED": "Agent 失败",
    "TOOL_CALL": "调用工具",
    "TOOL_RESULT": "工具返回",
    "TOOL_ERROR": "工具错误",
    "LLM_REQUEST": "LLM 请求",
    "LLM_RESPONSE": "LLM 响应",
    "FILE_READ": "读取文件",
    "FILE_WRITE": "写入文件",
    "COMMAND_EXECUTE": "执行命令",
    "APPROVAL_REQUEST": "请求审批",
    "APPROVAL_GRANTED": "审批通过",
    "APPROVAL_DENIED": "审批拒绝",
    "MEMORY_READ": "读取记忆",
    "MEMORY_WRITE": "写入记忆",
}


class TimelineRenderer:
    """Render evidence chain as human-readable timeline."""

    def __init__(self, evidence_chain: list):
        self.chain = evidence_chain

    def render_text(self) -> str:
        lines = ["=" * 60, "  Agent Execution Timeline", "=" * 60, ""]
        for i, ev in enumerate(self.chain):
            et = ev.get("event_type", "UNKNOWN")
            label = EVENT_LABELS_ZH.get(et, et)
            ts = ev.get("timestamp", "")[:19]
            agent = ev.get("agent_id", "unknown")
            lines.append(f"[{i+1:03d}] {ts} | {label} | {agent}")
            payload = ev.get("payload", {})
            if payload:
                for k, v in payload.items():
                    if isinstance(v, str) and len(v) < 80:
                        lines.append(f"      {k}: {v}")
            lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    def render_markdown(self) -> str:
        lines = ["# Agent Execution Timeline", ""]
        lines.append("| # | Time | Event | Agent | Details |")
        lines.append("|---|------|-------|-------|---------|")
        for i, ev in enumerate(self.chain):
            et = ev.get("event_type", "UNKNOWN")
            label = EVENT_LABELS_ZH.get(et, et)
            ts = ev.get("timestamp", "")[:19]
            agent = ev.get("agent_id", "unknown")
            payload = ev.get("payload", {})
            details = ", ".join(f"{k}={v}" for k, v in payload.items() if isinstance(v, (str, int, float)))
            lines.append(f"| {i+1} | {ts} | {label} | {agent} | {details[:60]} |")
        return "\n".join(lines)

    def render_json(self) -> str:
        import json
        return json.dumps(self.chain, indent=2, ensure_ascii=False)

    def summary(self) -> Dict[str, Any]:
        event_types = [ev.get("event_type", "UNKNOWN") for ev in self.chain]
        return {
            "total_events": len(self.chain),
            "duration": f"{self.chain[0].get('timestamp', '?')} → {self.chain[-1].get('timestamp', '?')}",
            "event_types": list(set(event_types)),
            "agents": list(set(ev.get("agent_id", "unknown") for ev in self.chain)),
        }
