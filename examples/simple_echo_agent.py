import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openbase_core.events import EventBus
from openbase_core.agent import BaseAgent
import json
from datetime import datetime

# 导入 Guard
from plugins.traccia_guard import Guard

class EchoAgent(BaseAgent):
    def run(self, input_text: str):
        run_id = self._emit("AgentStarted", {"input": input_text})
        self._emit("MemoryUpdate", {"key": "last_input", "value": input_text}, parent_id=run_id)
        
        # 模拟工具调用：调用一个安全的工具
        self._emit("ToolCall", {"tool_name": "echo", "args": {"message": input_text}}, parent_id=run_id)
        output = f"Echo: {input_text}"
        
        # 模拟一个被禁止的工具调用
        self._emit("ToolCall", {"tool_name": "delete_file", "args": {"path": "/tmp/test"}}, parent_id=run_id)
        
        self._emit("LLMResponse", {"output": output}, parent_id=run_id)
        self._emit("AgentFinished", {"final_output": output}, parent_id=run_id)
        return output

if __name__ == "__main__":
    bus = EventBus()
    
    # 注册 Guard，带上黑名单
    guard = Guard(bus, blacklist=["delete_file", "drop_database"])
    
    # 控制台打印
    bus.subscribe(lambda ev: print(f"[EVIDENCE] {ev}"))
    
    # 写入文件
    log_file = f"evidence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    def write_to_file(ev):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    bus.subscribe(write_to_file)
    
    agent = EchoAgent(agent_id="demo_001", event_bus=bus)
    result = agent.run("Hello OpenBase!")
    print(f"\n[RESULT] {result}")
    print(f"[INFO] Evidence saved to {log_file}")
