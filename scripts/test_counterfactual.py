import sys, os, glob
sys.path.insert(0, os.getcwd())
from openbase_core.graph import ExecutionGraph
from openbase_core.counterfactual import CounterfactualEngine
from openbase_core.replay_v1 import ReplayEngineV1

files = glob.glob("evidence_*.jsonl")
if files:
    latest = max(files, key=os.path.getmtime)
    g = ExecutionGraph.from_evidence_file(latest)
    engine = ReplayEngineV1(g)
    original = engine.replay()
    print(f"✅ Original state: {original}")
    
    cf = CounterfactualEngine(g)
    # 尝试修改第一个事件
    if g.roots:
        root_id = g.roots[0]
        new_state = cf.what_if(root_id, {"input": "Modified Input"})
        diff = cf.compare(original, new_state)
        print(f"✅ Counterfactual diff changed: {diff['changed']}")