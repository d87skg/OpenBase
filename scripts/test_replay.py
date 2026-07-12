import sys, os, glob
sys.path.insert(0, os.getcwd())
from openbase_core.graph import ExecutionGraph
from openbase_core.replay_v1 import ReplayEngineV1
import json

files = glob.glob("evidence_*.jsonl")
if files:
    latest = max(files, key=os.path.getmtime)
    print(f"📂 Replaying: {latest}")
    g = ExecutionGraph.from_evidence_file(latest)
    engine = ReplayEngineV1(g)
    # 模拟"原始状态"（假设我们知道原始结束状态，这里用重放结果自身做对比演示）
    replayed = engine.replay()
    print(f"✅ Replay completed. Final state: {json.dumps(replayed, indent=2)}")
    # 实际对比需要存储原始state，这里用重放自身diff演示
    diff = engine.diff(replayed, replayed)
    print(f"✅ Diff match: {diff['match']}")