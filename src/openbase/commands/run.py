from openbase.core.runtime import Runtime
from openbase.core.registry import Registry
from pathlib import Path


def cmd_run(args):
    # 确保在当前目录下使用 ./evidence
    evidence_dir = Path("./evidence")
    evidence_dir.mkdir(exist_ok=True)

    # 注册 Runtime 到当前项目的 .openbase/registry
    registry = Registry("./.openbase/registry")
    registry.register_runtime({
        "name": "OpenClaw",
        "version": "1.0.0"
    })

    runtime = Runtime("OpenClaw")
    result = runtime.execute(args.file)

    # 生成证据到 ./evidence
    from openbase.core.evidence import EvidenceEngine
    engine = EvidenceEngine("main", output_dir="./evidence")
    engine.emit("AGENT_STARTED", {"input": "Agent started"})
    engine.emit("AGENT_FINISHED", {"output": result})

    print(f"✅ 执行完成: {result}")
    print(f"   📁 证据目录: {evidence_dir.absolute()}")
    print(f"   📄 共生成 {engine.count()} 条证据")
