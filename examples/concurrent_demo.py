import sys, os, threading, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openbase_core.events import EventBus
from openbase_core.agent import BaseAgent
from openbase_core.vector_clock import VectorClock
import json

class ConcurrentAgent(BaseAgent):
    def run(self, input_text: str):
        run_id = self._emit("AgentStarted", {"input": input_text})
        # 模拟业务处理
        time.sleep(0.01)
        self._emit("ResourceWrite", {"resource": "counter", "value": input_text}, parent_id=run_id)
        self._emit("AgentFinished", {"final_output": f"Written: {input_text}"}, parent_id=run_id)
        return "Done"

def run_node(node_id, value, events):
    bus = EventBus(node_id=node_id)
    def collector(ev):
        events.append((node_id, ev["vector_clock"], ev["event_type"], ev["payload"].get("value", "")))
    bus.subscribe(collector)
    agent = ConcurrentAgent(agent_id=f"agent_{node_id}", event_bus=bus)
    agent.run(value)

if __name__ == "__main__":
    print("🚀 Running concurrent write demonstration...")
    events = []
    
    # 两个节点几乎同时修改同一资源
    t1 = threading.Thread(target=run_node, args=("node-X", "100", events))
    t2 = threading.Thread(target=run_node, args=("node-Y", "200", events))
    t1.start(); t2.start()
    t1.join(); t2.join()

    print("\n📊 Events with Vector Clocks:")
    for node, vc, evtype, val in events:
        print(f"  {node}: {vc} → {evtype} (value={val})")
    
    # 检查第一个和最后一个事件的关系
    # 这里我们检查两个 ResourceWrite 事件是否并发
    writes = [e for e in events if e[2] == "ResourceWrite"]
    if len(writes) == 2:
        vc_a = writes[0][1]
        vc_b = writes[1][1]
        rel = VectorClock.compare(vc_a, vc_b)
        print(f"\n🔍 Relationship between writes: {rel}")