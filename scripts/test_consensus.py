import sys, os, glob
sys.path.insert(0, os.getcwd())
from openbase_core.graph import ExecutionGraph
from openbase_core.consensus import ConsensusEngine

files = glob.glob("evidence_*.jsonl")
if len(files) >= 1:
    # 模拟两个图（实际可用两份不同文件，或同一份文件构建两次）
    g1 = ExecutionGraph.from_evidence_file(files[0])
    g2 = ExecutionGraph.from_evidence_file(files[0])  # 演示相同
    engine = ConsensusEngine([g1, g2])
    merged = engine.merge()
    print(f"✅ Merged graph nodes: {len(merged.nodes)}")
    divergences = engine.detect_divergence()
    print(f"✅ Divergences detected: {len(divergences)}")
else:
    print("❌ Need at least one evidence file")