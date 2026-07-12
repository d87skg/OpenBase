"""
OpenClaw ↔ Engine Bridge Integration Test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from reference.openclaw.adapter import OpenClawExecutionAdapter


def test_bridge():
    print("=" * 60)
    print("🔗 OpenClaw ↔ Engine Bridge Integration Test")
    print("=" * 60)

    # 创建 Adapter
    adapter = OpenClawExecutionAdapter()
    print("\n✅ Adapter created and engines initialized")

    # 1. 开始执行（模拟 OpenClaw 启动）
    print("\n⚙️  1. Starting Execution (simulating OpenClaw)...")
    result = adapter.start_execution("openclaw-agent", session_id="session-001")
    print(f"   - Execution started: {result.get('execution_id')}")

    # 2. 模拟 OpenClaw 执行步骤（发出 Evidence）
    print("\n📝 2. Simulating OpenClaw execution steps...")

    steps = [
        ("AGENT_STARTED", {"input": "What is the weather in San Francisco?"}),
        ("LLM_CALL", {"model": "gpt-4", "prompt": "What is the weather in San Francisco?"}),
        ("LLM_RESPONSE", {"output": "I need to check the weather API."}),
        ("TOOL_CALL", {"tool": "get_weather", "args": {"city": "San Francisco"}}),
        ("TOOL_RESULT", {"result": {"temperature": "18°C", "condition": "Sunny"}}),
        ("LLM_CALL", {"model": "gpt-4", "prompt": "Summarize the weather for the user."}),
        ("LLM_RESPONSE", {"output": "San Francisco is currently 18°C and sunny."}),
    ]

    for event_type, payload in steps:
        result = adapter.emit_evidence(event_type, payload)
        print(f"   - {event_type}: {result.get('evidence_id', 'OK')}")

    # 3. 完成执行
    print("\n🏁 3. Completing Execution...")
    result = adapter.complete_execution("San Francisco is currently 18°C and sunny.")
    print(f"   - Execution completed: {result.get('evidence_id')}")

    # 4. 验证
    print("\n🔍 4. Running Verification...")
    result = adapter.verify()
    print(f"   - Verification passed: {result.get('passed')}")
    print(f"   - Checks: {len(result.get('checks', []))}")

    # 5. 重放
    print("\n🔄 5. Running Replay...")
    result = adapter.replay()
    print(f"   - Replayed: {result.get('event_count')} events")

    # 6. 分析确定性
    print("\n🎯 6. Analyzing Determinism...")
    result = adapter.analyze_determinism()
    print(f"   - Profile: {result.get('profile')}")
    print(f"   - Sources: {result.get('sources')}")

    # 7. 生成证书
    print("\n🏛️  7. Generating Certificate...")
    result = adapter.certify(trust_score=0.95)
    if "error" not in result:
        cert = result.get("certificate", {})
        print(f"   - Certificate ID: {cert.get('certificate_id')}")
        print(f"   - Status: {cert.get('status')}")
        print(f"   - Level: {cert.get('level')}")
    else:
        print(f"   - Error: {result.get('error')}")

    # 8. 完整报告
    print("\n📊 8. Full Report:")
    report = adapter.get_full_report()
    print(f"   - Execution ID: {report.get('execution_id')}")
    print(f"   - Evidence Count: {report.get('evidence_count')}")
    print(f"   - Certification Status: {report.get('certification', {}).get('status', 'N/A')}")

    print("\n" + "=" * 60)
    print("✅ Bridge integration test completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_bridge()
