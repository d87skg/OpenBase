#!/usr/bin/env python3
"""
openbase trust - 信任管理
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.trust.interface import SimpleTrustProvider, WeightedTrustProvider
from runtime.registry.client import RegistryClient


def trust_calculate(args):
    registry = RegistryClient("./.openbase/registry")

    runtime_id = args.runtime_id
    if not runtime_id:
        runtime_info = registry.get_runtime_by_name("OpenClaw")
        if runtime_info:
            runtime_id = runtime_info["runtime_id"]

    if not runtime_id:
        print("❌ 未找到 Runtime")
        print("   提示: 请先运行 'openbase run agents/main.py' 注册 Runtime")
        return 1

    evidence_list = registry.list_evidence(runtime_id)
    if not evidence_list:
        print(f"📋 Runtime: {runtime_id}")
        print("⚠️ 尚无证据")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 0

    provider_map = {
        "simple": SimpleTrustProvider(),
        "weighted": WeightedTrustProvider()
    }
    provider = provider_map.get(args.provider, SimpleTrustProvider())

    score = provider.calculate(evidence_list)
    verified = provider.verify(score, args.threshold)
    explanation = provider.explain(evidence_list)

    print(f"📋 Runtime: {runtime_id}")
    print(f"📄 证据数: {len(evidence_list)}")
    print(f"🔢 信任分数: {score:.2f}")
    print(f"✅ 验证结果: {'通过' if verified else '未通过'} (阈值: {args.threshold})")
    print(f"📝 说明: {explanation.get('explanation', '')}")
    print(f"📊 详情: {explanation.get('detail', '')}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="信任管理")
    subparsers = parser.add_subparsers(dest="action", required=True)

    calc_parser = subparsers.add_parser("calculate", help="计算信任分数")
    calc_parser.add_argument("--runtime-id", help="Runtime ID")
    calc_parser.add_argument("--provider", default="simple",
                             choices=["simple", "weighted"],
                             help="信任提供者")
    calc_parser.add_argument("--threshold", type=float, default=0.6,
                             help="验证阈值 (0.0-1.0)")

    args = parser.parse_args()

    if args.action == "calculate":
        sys.exit(trust_calculate(args))


if __name__ == "__main__":
    main()
