#!/usr/bin/env python3
"""
openbase run - 使用 OpenBase Reference Runtime 运行 Agent
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.lifecycle.runtime import Runtime
from runtime.registry.client import RegistryClient


def run_agent(file_path: str, args: list):
    if not Path(file_path).exists():
        print(f"❌ Agent 文件不存在: {file_path}")
        return 1

    agent_name = Path(file_path).stem

    print(f"🚀 正在运行 Agent: {agent_name}")

    registry = RegistryClient("./.openbase/registry")

    runtime_info = registry.get_runtime_by_name("OpenClaw")
    if not runtime_info:
        runtime_info = registry.register_runtime(
            name="OpenClaw",
            version="1.0.0",
            vendor="OpenBase",
            capabilities=["execution", "evidence", "replay"]
        )

    runtime = Runtime(agent_id=agent_name, output_dir="./evidence")
    runtime.initialize()
    runtime.execute({"prompt": "Hello, OpenBase!", "file": file_path})
    runtime.finish()

    for ev in runtime.get_evidence():
        registry.index_evidence(
            evidence_id=ev["evidence_id"],
            runtime_id=runtime_info["runtime_id"],
            event_type=ev["event_type"],
            timestamp=ev["timestamp"]
        )

    print(f"\n📊 证据摘要:")
    for ev in runtime.get_evidence():
        print(f"   {ev['evidence_id']}: {ev['event_type']}")

    print(f"\n📋 Registry 摘要:")
    summary = registry.get_summary()
    print(f"   Runtime: {summary['total_runtimes']}")
    print(f"   Evidence: {summary['total_evidence']}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="使用 Reference Runtime 运行 Agent")
    parser.add_argument("file", help="Agent 文件路径")
    parser.add_argument("--args", nargs="*", help="传递给 Agent 的参数")
    args = parser.parse_args()

    sys.exit(run_agent(args.file, args.args))


if __name__ == "__main__":
    main()