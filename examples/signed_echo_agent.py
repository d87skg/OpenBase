import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openbase_core.events import EventBus
from openbase_core.agent import BaseAgent
import json
from datetime import datetime

# 加载密钥
with open('config/keys.json', 'r') as f:
    keys = json.load(f)
private_key = keys['private_key']

class SignedEchoAgent(BaseAgent):
    def run(self, input_text: str):
        run_id = self._emit("AgentStarted", {"input": input_text})
        self._emit("MemoryUpdate", {"key": "last_input", "value": input_text}, parent_id=run_id)
        output = f"Signed Echo: {input_text}"
        self._emit("LLMResponse", {"output": output}, parent_id=run_id)
        self._emit("AgentFinished", {"final_output": output}, parent_id=run_id)
        return output

if __name__ == "__main__":
    bus = EventBus()
    bus.subscribe(lambda ev: print(f"[EVIDENCE] {ev}"))
    
    # 证据持久化
    log_file = f"evidence_signed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    def write_to_file(ev):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    bus.subscribe(write_to_file)
    
    # 使用私钥运行
    agent = SignedEchoAgent(
        agent_id="signed_agent",
        event_bus=bus,
        private_key=private_key,
        execution_id="exec_001"  # 可自定义，或留空自动生成
    )
    result = agent.run("Hello Signed World!")
    print(f"\n[RESULT] {result}")
    print(f"[INFO] Evidence with signatures saved to {log_file}")