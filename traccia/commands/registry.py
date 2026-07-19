#!/usr/bin/env python3
"""
openbase registry - Registry 管理
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.registry.client import RegistryClient


def list_runtimes(args):
    registry_dir = Path(".openbase/registry")
    if not registry_dir.exists():
        print("📋 尚无 Registry 数据")
        print("   提示: 请先运行 'openbase run agents/main.py' 注册 Runtime")
        return 0

    registry = RegistryClient("./.openbase/registry")

    if args.runtime_id:
        runtime = registry.get_runtime(args.runtime_id)
        if runtime:
            print(json.dumps(runtime, indent=2))
        else:
            print(f"❌ Runtime {args.runtime_id} 未找到")
        return 0

    if args.name:
        runtime = registry.get_runtime_by_name(args.name)
        if runtime:
            print(json.dumps(runtime, indent=2))
        else:
            print(f"❌ Runtime {args.name} 未找到")
        return 0

    runtimes = registry.list_runtimes()
    if not runtimes:
        print("📋 尚无 Runtime")
        print("   提示: 请先运行 'openbase run agents/main.py' 注册 Runtime")
        return 0

    print(f"📋 共 {len(runtimes)} 个 Runtime:")
    for r in runtimes:
        print(f"   {r['name']} ({r['runtime_id']}) | {r['status']} | {r['version']}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Registry 管理")
    subparsers = parser.add_subparsers(dest="action", required=True)

    list_parser = subparsers.add_parser("list", help="列出 Runtime")
    list_parser.add_argument("--runtime-id", help="按 ID 查询")
    list_parser.add_argument("--name", help="按名称查询")

    args = parser.parse_args()

    if args.action == "list":
        sys.exit(list_runtimes(args))


if __name__ == "__main__":
    main()
