#!/usr/bin/env python3
"""
OpenAI Adapter 演示
"""

import sys
from pathlib import Path

# 添加 openclaw 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.registry.client import RegistryClient
from adapters.openai.adapter import OpenAICallback, OpenAIClient


def main():
    print("🚀 OpenAI Adapter Demo\n")

    # 初始化 Registry
    registry = RegistryClient("./.openbase/registry")

    # 获取 Runtime
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

    # 创建 OpenAI 适配器
    callback = OpenAICallback(runtime_id=runtime_id, evidence_dir="./evidence")
    client = OpenAIClient(callback)

    # 调用 OpenAI（自动记录证据）
    print("\n📡 调用 OpenAI API...")
    response = client.chat_completion(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, OpenBase!"}
        ],
        temperature=0.7
    )

    print(f"\n📤 响应: {response['choices'][0]['message']['content']}")

    # 显示生成的证据
    evidence_list = callback.get_evidence()
    print(f"\n📊 生成了 {len(evidence_list)} 条证据:")
    for ev in evidence_list:
        print(f"   {ev['evidence_id']}: {ev['event_type']}")


if __name__ == "__main__":
    main()