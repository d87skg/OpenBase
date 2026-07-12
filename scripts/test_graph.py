import sys, os
sys.path.insert(0, os.getcwd())
from openbase_core.graph import ExecutionGraph
import glob

# 找最新的 evidence 文件
files = glob.glob("evidence_*.jsonl")
if files:
    latest = max(files, key=os.path.getmtime)
    print(f"📂 Building graph from: {latest}")
    g = ExecutionGraph.from_evidence_file(latest)
    print(f"✅ Nodes: {len(g.nodes)}, Roots: {len(g.roots)}")
    sorted_ids = g.topological_sort()
    print(f"✅ Topological order: {len(sorted_ids)} events")
    for eid in sorted_ids[:5]:
        print(f"  - {eid}")
else:
    print("❌ No evidence files found. Run an agent first.")