from openbase.core.replay import ReplayEngine


def cmd_replay(args):
    engine = ReplayEngine(args.evidence_dir or "./evidence")
    engine.load()

    if not engine.evidence:
        print("❌ 未找到证据")
        print("   提示: 请先运行 'openbase run' 生成证据")
        return

    result = engine.replay()
    print(f"🔄 重放执行过程:")
    print(f"   📄 共 {len(result['events'])} 个事件")
    print(f"   📊 最终状态: {result['state']}")

    for i, ev in enumerate(result["events"], 1):
        print(f"   [{i}] {ev['event_type']}")
