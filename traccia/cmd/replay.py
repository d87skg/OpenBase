#!/usr/bin/env python3
"""
openbase replay - 重放 Agent 执行过程
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.replay.engine import ReplayEngine


def main():
    parser = argparse.ArgumentParser(description="重放 Agent 执行过程")
    parser.add_argument("--evidence-dir", default="./evidence", help="证据目录")
    args = parser.parse_args()

    evidence_dir = Path(args.evidence_dir)
    if not evidence_dir.exists():
        print(f"❌ 证据目录不存在: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

    engine = ReplayEngine(args.evidence_dir)
    engine.load()

    if len(engine.evidence) == 0:
        print(f"❌ 证据目录为空: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

    result = engine.replay()
    engine.print_replay(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
