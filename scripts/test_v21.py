import sys, os, glob, json
sys.path.insert(0, os.getcwd())

from openbase_core.fault_injector import FaultInjector
from openbase_core.byzantine_detector import ByzantineDetector
from openbase_core.adversarial_replay import AdversarialReplayEngine
from openbase_core.inconsistency_proof import InconsistencyProver
from openbase_core.replay_v1 import ReplayEngineV1
from openbase_core.graph import ExecutionGraph

def load_events(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

# 1. 加载原始证据
files = glob.glob("evidence_*.jsonl")
if not files:
    print("❌ No evidence files found.")
    sys.exit(1)
latest = max(files, key=os.path.getmtime)
print(f"📂 Loading: {latest}")
original_events = load_events(latest)
print(f"✅ Loaded {len(original_events)} events")

# 2. 注入故障
injector = FaultInjector(seed=42)
corrupted_events = injector.apply_all(original_events)
print(f"✅ Injected faults: {len(injector.get_fault_report())} faults")
for fault in injector.get_fault_report()[:5]:
    print(f"  - {fault}")

# 3. 拜占庭检测
detector = ByzantineDetector()
check_result = detector.full_check(corrupted_events)
print(f"\n🔍 Byzantine Check Result:")
print(f"  Anomalies: {check_result['anomaly_count']}")
print(f"  Malicious suspicion: {check_result['malicious_suspicion']}")
for a in check_result['anomalies'][:3]:
    print(f"  - {a}")

# 4. 对抗重放
print("\n🔄 Adversarial Replay:")
replayer = AdversarialReplayEngine(corrupted_events)
reconstructed = replayer.reconstruct()
print(f"  Reconstructed state: {reconstructed}")
# 比较与原始状态（用原始事件的确定性重放作为基准）
graph = ExecutionGraph()
for ev in original_events:
    graph.add_event(ev)
original_replayer = ReplayEngineV1(graph)
original_state = original_replayer.replay()
diff = replayer.compare_with_original(original_state)
print(f"  Diff match: {diff['match']}")
if not diff['match']:
    print(f"  Differences: {diff['differences']}")

# 5. 不一致证明
print("\n📜 Inconsistency Proof:")
prover = InconsistencyProver(original_events, corrupted_events)
proof = prover.prove()
print(f"  Inconsistency found: {proof['inconsistency_found']}")
print(f"  Missing events: {len(proof['missing_events'])}")
print(f"  Extra events: {len(proof['extra_events'])}")
print(f"  Malicious suspicion: {proof['malicious_suspicion']}")

print("\n✅ v2.1 测试完成！")