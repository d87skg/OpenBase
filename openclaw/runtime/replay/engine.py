#!/usr/bin/env python3
"""
Replay Engine

从证据重建执行过程
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class ReplayEngine:
    """重放引擎：从证据重建执行"""

    def __init__(self, evidence_dir: str = "./evidence"):
        self.evidence_dir = Path(evidence_dir)
        self.evidence: List[Dict[str, Any]] = []

    def load(self) -> "ReplayEngine":
        """加载所有证据文件"""
        if not self.evidence_dir.exists():
            print(f"❌ 证据目录不存在: {self.evidence_dir}")
            return self

        files = list(self.evidence_dir.glob("*.json"))
        if not files:
            print(f"⚠️ 未找到证据文件: {self.evidence_dir}")
            return self

        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    evidence = json.load(fp)
                    self.evidence.append(evidence)
            except Exception as e:
                print(f"⚠️ 跳过文件 {f.name}: {e}")

        # 按时间排序
        self.evidence.sort(key=lambda x: x.get("timestamp", ""))

        print(f"✅ 加载了 {len(self.evidence)} 条证据")
        return self

    def replay(self) -> Dict[str, Any]:
        """重放执行过程"""
        if not self.evidence:
            return {
                "status": "FAILED",
                "reason": "No evidence loaded",
                "events": []
            }

        events = []
        state = {}

        for ev in self.evidence:
            event_type = ev.get("event_type", "UNKNOWN")
            timestamp = ev.get("timestamp", "")
            payload = ev.get("payload", {})
            evidence_id = ev.get("evidence_id", "unknown")

            event = {
                "sequence": len(events) + 1,
                "evidence_id": evidence_id,
                "event_type": event_type,
                "timestamp": timestamp,
                "payload": payload
            }

            # 更新状态
            if event_type == "AGENT_STARTED":
                state["status"] = "running"
                state["agent_id"] = ev.get("agent_id", "unknown")
                state["run_id"] = ev.get("run_id", "unknown")
            elif event_type == "AGENT_FINISHED":
                state["status"] = "completed"
                state["output"] = payload.get("output")
            elif event_type == "LLM_CALL":
                state["last_model"] = payload.get("model")
            elif event_type == "TOOL_CALL":
                state["last_tool"] = payload.get("tool")

            events.append(event)

        return {
            "status": "SUCCESS",
            "run_id": state.get("run_id", "unknown"),
            "agent_id": state.get("agent_id", "unknown"),
            "total_events": len(events),
            "events": events,
            "state": state
        }

    def print_replay(self, result: Dict[str, Any]) -> None:
        """打印重放结果"""
        if result["status"] != "SUCCESS":
            print(f"❌ 重放失败: {result.get('reason', 'Unknown error')}")
            return

        print(f"\n🔄 重放执行过程")
        print(f"   📋 Run ID: {result['run_id']}")
        print(f"   🤖 Agent: {result['agent_id']}")
        print(f"   📄 共 {result['total_events']} 个事件")
        print()

        for ev in result["events"]:
            print(f"   [{ev['sequence']}] {ev['event_type']}")
            print(f"       ⏱️  {ev['timestamp']}")
            if ev['event_type'] == "AGENT_STARTED":
                print(f"       📥 输入: {ev['payload'].get('input', {})}")
            elif ev['event_type'] == "AGENT_FINISHED":
                print(f"       📤 输出: {ev['payload'].get('output', {})}")
            elif ev['event_type'] == "LLM_CALL":
                print(f"       🧠 模型: {ev['payload'].get('model')}")
                print(f"       💬 Prompt: {ev['payload'].get('prompt', '')[:50]}...")
            elif ev['event_type'] == "TOOL_CALL":
                print(f"       🔧 工具: {ev['payload'].get('tool')}")
                print(f"       📥 参数: {ev['payload'].get('args', {})}")
            print()

        print("📊 最终状态:")
        for key, value in result["state"].items():
            print(f"   {key}: {value}")

    def verify(self, expected_events: List[str]) -> bool:
        """验证事件序列是否匹配预期"""
        actual = [e["event_type"] for e in self.evidence]
        if len(actual) != len(expected_events):
            print(f"❌ 事件数量不匹配: 预期 {len(expected_events)}, 实际 {len(actual)}")
            return False

        for i, (a, e) in enumerate(zip(actual, expected_events)):
            if a != e:
                print(f"❌ 事件序列不匹配: 位置 {i+1} 预期 {e}, 实际 {a}")
                return False

        print(f"✅ 事件序列验证通过: {actual}")
        return True