from openbase.core.trust import SimpleTrustProvider
from openbase.core.registry import Registry


def cmd_trust(args):
    registry = Registry()
    runtime = registry.get_runtime()

    if not runtime:
        print("❌ 未找到 Runtime")
        print("   提示: 请先运行 'openbase init' 初始化项目")
        return

    # 简单模拟：从 evidence 目录加载证据
    # 实际应通过 registry 获取
    from openbase.core.evidence import EvidenceEngine
    engine = EvidenceEngine("temp", "./evidence")
    evidence = engine.get_all()

    provider = SimpleTrustProvider()
    score = provider.calculate(evidence)
    explanation = provider.explain(evidence)

    print(f"📋 Runtime: {runtime.get('name', 'unknown')}")
    print(f"📄 证据数: {len(evidence)}")
    print(f"🔢 信任分数: {score:.2f}")
    print(f"📝 说明: {explanation}")
