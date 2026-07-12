#!/usr/bin/env python3
"""
OpenBase 全面测试执行器
运行所有单元测试、集成测试和性能测试
"""

import sys
import os
import subprocess
import json
import time
from datetime import datetime

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n{'='*60}")
    print(f"▶️ {description}")
    print(f"{'='*60}")
    
    start = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode == 0:
        print(f"✅ 完成 ({elapsed:.2f}s)")
    else:
        print(f"❌ 失败 ({elapsed:.2f}s)")
        if result.stdout:
            print("输出:")
            print(result.stdout[-1000:])  # 显示最后1000字符
        if result.stderr:
            print("错误:")
            print(result.stderr[-1000:])
    
    return {
        "description": description,
        "success": result.returncode == 0,
        "elapsed": elapsed,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

def main():
    print("\n" + "="*60)
    print("🚀 OpenBase 全面测试套件")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    
    # 1. 单元测试
    results.append(run_command(
        "python tests/unit/test_all_modules.py",
        "单元测试 (Unit Tests)"
    ))
    
    # 2. 数据完整性测试
    results.append(run_command(
        "python tests/integration/test_integrity.py",
        "数据完整性测试 (Integrity Tests)"
    ))
    
    # 3. 性能压测
    results.append(run_command(
        "python tests/performance/performance_test.py",
        "性能压测 (Performance Tests)"
    ))
    
    # 4. 快速功能验证（CLI）
    results.append(run_command(
        "openbase verify",
        "CLI 验证 (openbase verify)"
    ))
    
    # 5. 证明测试
    results.append(run_command(
        "openbase prove && openbase proof-verify --full",
        "证明生成与验证 (Proof Generation & Verification)"
    ))
    
    # 6. 多节点测试
    results.append(run_command(
        "python examples/multi_node_agent.py",
        "多节点模拟 (Multi-node Simulation)"
    ))
    
    # 汇总
    print("\n" + "="*60)
    print("📊 测试汇总")
    print("="*60)
    
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    total_time = sum(r["elapsed"] for r in results)
    
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"{status} {r['description']} ({r['elapsed']:.2f}s)")
    
    print(f"\n总计: ✅ {passed} 通过, ❌ {failed} 失败")
    print(f"⏱️ 总耗时: {total_time:.2f}s")
    
    if failed > 0:
        print("\n⚠️ 有测试失败，请检查上述输出")
        sys.exit(1)
    else:
        print("\n🎉 所有测试通过！")
        sys.exit(0)

if __name__ == "__main__":
    main()