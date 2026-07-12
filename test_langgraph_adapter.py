#!/usr/bin/env python3
"""
测试 LangGraph Adapter
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "openclaw"))

from runtime.adapters.langgraph import LangGraphAdapter
from runtime.registry.client import RegistryClient


def main():
    print("🚀 LangGraph Adapter Demo\n")

    registry = RegistryClient(".openbase/registry")

    runtime_info = registry.get_runtime_by_name("OpenClaw")
    if not runtime_info:
        runtime_info = registry.register_runtime(
            name="OpenClaw",
            version="1.0.0",
            vendor="OpenBase",
            capabilities=["execution", "evidence", "replay"]
        )

    runtime_id = runtime_info["runtime_id"]
    print(f"📋 Runtime: {runtime_id}")

    adapter = LangGraphAdapter(runtime_id=runtime_id, evidence_dir="./evidence")

    print("\n📡 模拟 LangGraph 执行...")
    result = adapter.simulate_graph_execution(
        graph_name="SimpleWorkflow",
        inputs={"task": "Build a graph"}
    )

    print(f"\n📤 结果: {result}")

    evidence_list = adapter.get_evidence()
    print(f"\n📊 生成了 {len(evidence_list)} 条证据:")
    for ev in evidence_list:
        print(f"   {ev['evidence_id']}: {ev['event_type']}")


if __name__ == "__main__":
    main()