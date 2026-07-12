#!/usr/bin/env python3
"""
测试 OpenAI Adapter
"""

import sys
from pathlib import Path

# 将 openclaw 添加到路径
sys.path.insert(0, str(Path(__file__).parent / "openclaw"))

from runtime.adapters.openai import OpenAICallback, OpenAIClient
from runtime.registry.client import RegistryClient


def main():
    print("🚀 OpenAI Adapter Demo\n")

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

    callback = OpenAICallback(runtime_id=runtime_id, evidence_dir="./evidence")
    client = OpenAIClient(callback)

    print("\n📡 调用 OpenAI API...")
    response = client.chat_completion(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, OpenBase!"}
        ],
        temperature=0.7
    )

    print(f"\n📤 响应: {response['choices'][0]['message']['content']}")

    evidence_list = callback.get_evidence()
    print(f"\n📊 生成了 {len(evidence_list)} 条证据:")
    for ev in evidence_list:
        print(f"   {ev['evidence_id']}: {ev['event_type']}")


if __name__ == "__main__":
    main()