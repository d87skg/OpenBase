#!/usr/bin/env python3
"""
测试 Anthropic Adapter
"""

import sys
from pathlib import Path

# 将 openclaw 添加到路径
sys.path.insert(0, str(Path(__file__).parent / "openclaw"))

from runtime.adapters.anthropic import AnthropicCallback, AnthropicClient
from runtime.registry.client import RegistryClient


def main():
    print("🚀 Anthropic Adapter Demo\n")

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

    callback = AnthropicCallback(runtime_id=runtime_id, evidence_dir="./evidence")
    client = AnthropicClient(callback)

    print("\n📡 调用 Anthropic API...")
    response = client.messages_create(
        model="claude-3-haiku-20240307",
        messages=[
            {"role": "user", "content": "Hello, OpenBase with Anthropic!"}
        ],
        max_tokens=1024,
        temperature=0.7
    )

    # 提取响应文本
    content = response.get("content", [])
    if content and len(content) > 0:
        text = content[0].get("text", "No text")
    else:
        text = str(response)

    print(f"\n📤 响应: {text}")

    evidence_list = callback.get_evidence()
    print(f"\n📊 生成了 {len(evidence_list)} 条证据:")
    for ev in evidence_list:
        print(f"   {ev['evidence_id']}: {ev['event_type']}")


if __name__ == "__main__":
    main()