#!/usr/bin/env python3
"""
openbase certificate - 证书管理
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.certificate.engine import CertificateEngine
from runtime.registry.client import RegistryClient


def issue_certificate(args):
    evidence_dir = Path(args.evidence_dir)
    if not evidence_dir.exists():
        print(f"❌ 证据目录不存在: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

    evidence_files = list(evidence_dir.glob("*.json"))
    if not evidence_files:
        print(f"❌ 证据目录为空: {evidence_dir}")
        print("   提示: 请先运行 'openbase run agents/main.py' 生成证据")
        return 1

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

    print(f"📋 Runtime: {runtime_id}")

    engine = CertificateEngine(args.evidence_dir)
    engine.load_evidence()

    certificate = engine.issue_certificate(
        runtime_id=runtime_id,
        level=args.level
    )

    if certificate and certificate.get("certificate_id"):
        # 确保输出目录是相对于当前工作目录
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / output_dir
        engine.save_certificate(certificate, str(output_dir))
        print(f"✅ 证书已保存到 {output_dir}/")
        return 0
    else:
        reason = certificate.get("reason", "未知原因") if certificate else "证书生成失败"
        print(f"❌ 证书颁发失败: {reason}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="证书管理")
    subparsers = parser.add_subparsers(dest="action", required=True)

    issue_parser = subparsers.add_parser("issue", help="颁发证书")
    issue_parser.add_argument("--runtime-id", help="Runtime ID")
    issue_parser.add_argument("--level", default="BRONZE",
                              choices=["BRONZE", "SILVER", "GOLD", "PLATINUM"],
                              help="证书等级")
    issue_parser.add_argument("--evidence-dir", default="./evidence", help="证据目录")
    issue_parser.add_argument("--output-dir", default="./reports", help="证书输出目录")

    args = parser.parse_args()

    if args.action == "issue":
        sys.exit(issue_certificate(args))


if __name__ == "__main__":
    main()
