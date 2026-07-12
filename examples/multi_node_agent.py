import sys, os, time, threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openbase_core.events import EventBus
from openbase_core.agent import BaseAgent
import json
from datetime import datetime

class SimpleAgent(BaseAgent):
    def run(self, input_text: str):
        run_id = self._emit("AgentStarted", {"input": input_text})
        self._emit("MemoryUpdate", {"key": "msg", "value": input_text}, parent_id=run_id)
        self._emit("AgentFinished", {"final_output": f"Processed: {input_text}"}, parent_id=run_id)
        return "Done"

def run_agent(node_id, agent_name, input_text, events):
    # 每个节点创建独立的 EventBus
    bus = EventBus(node_id=node_id)
    # 收集事件，存储 (node_id, vector_clock, event_type)
    def collector(ev):
        # ev 是 to_dict() 输出，包含 vector_clock
        events.append((node_id, ev.get("vector_clock", {}), ev.get("event_type"), ev.get("run_id")))
    bus.subscribe(collector)
    agent = SimpleAgent(agent_id=agent_name, event_bus=bus)
    agent.run(input_text)

if __name__ == "__main__":
    print("🚀 Running multi-node demonstration with Vector Clocks...")
    events = []
    t1 = threading.Thread(target=run_agent, args=("node-A", "agent1", "Hello from A", events))
    t2 = threading.Thread(target=run_agent, args=("node-B", "agent2", "Hello from B", events))
    t1.start(); t2.start()
    t1.join(); t2.join()

    # 按向量时钟的字典比较（简化：按节点 A 的时间为主）
    # 实际应使用偏序比较，但为了演示，我们按字典中第一个节点的值排序
    def sort_key(x):
        # 取 vector_clock 中第一个节点的值，若无则 0
        vc = x[1]
        return vc.get("node-A", vc.get("node-B", 0)) if vc else 0

    events.sort(key=sort_key)
    print("\n📊 Events with Vector Clocks (sorted by first node's time):")
    for node, vc, evtype, eid in events:
        print(f"  {node}: {vc} → {evtype} ({eid[:8]})")