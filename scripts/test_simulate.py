import sys, os, glob
sys.path.insert(0, os.getcwd())
from openbase_core.graph import ExecutionGraph
from openbase_core.simulator import ProbabilisticReplayer

files = glob.glob("evidence_*.jsonl")
if files:
    latest = max(files, key=os.path.getmtime)
    g = ExecutionGraph.from_evidence_file(latest)
    replayer = ProbabilisticReplayer(g, samples=3)
    distribution = replayer.run_distribution()
    print(f"✅ Simulated {len(distribution)} possible worlds")
    for i, state in enumerate(distribution):
        print(f"  World {i+1}: {len(state['outputs'])} outputs")