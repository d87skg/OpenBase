#!/usr/bin/env python3
"""
openbase test - 运行一致性测试
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))


def run_conformance_test(evidence_dir="./evidence", verbose=False):
    evidence_path = Path(evidence_dir)
    if not evidence_path.exists():
        print(f"❌ 证据目录不存在: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

    evidence_files = list(evidence_path.glob("*.json"))
    if not evidence_files:
        print(f"❌ 证据目录为空: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

    from test import run_conformance_test as test_func
    sys.argv = ["test"]
    return test_func(evidence_dir, verbose)


def main():
    parser = argparse.ArgumentParser(description="运行一致性测试")
    parser.add_argument("--evidence-dir", default="./evidence", help="证据目录")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    sys.exit(run_conformance_test(args.evidence_dir, args.verbose))


if __name__ == "__main__":
    main()
