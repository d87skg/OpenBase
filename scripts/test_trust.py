import sys, os, glob
sys.path.insert(0, os.getcwd())
from openbase_core.trust import TrustGraph

files = glob.glob("evidence_*.jsonl")
if files:
    tg = TrustGraph.from_evidence_files(files)
    print(f"✅ Trust graph nodes: {tg.nodes}")
    init = {node: 0.5 for node in tg.nodes}
    propagated = tg.propagate(init)
    print(f"✅ Propagated trust scores: {propagated}")
else:
    print("❌ No evidence files")