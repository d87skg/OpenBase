import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openbase_core.events import EventBus
from openbase_core.agent import BaseAgent
import json
from datetime import datetime

# 导入 Guard
from plugins.guard import install_guard

class ToolAgent(BaseAgent):
    def run(self, input_text: str):
        # 开始
        run_id = self._emit("AgentStarted", {"input": input_text})
        
        # 模拟一系列工具调用
        tools_to_try = [
            "read_file",      # ✅ 允许
            "list_directory", # ✅ 允许
            "delete_file",    # ❌ 拒绝
            "read_log",       # ✅ 允许
            "drop_table",     # ❌ 拒绝
        ]
        
        for tool in tools_to_try:
            self._emit("ToolCall", {
                "tool_name": tool,
                "input": f"{tool} /path/to/data"
            }, parent_id=run_id)
            
            # 模拟工具返回（即使被拦截，也记录结果）
            self._emit("ToolResult", {
                "tool_name": tool,
                "output": f"Result of {tool}"
            }, parent_id=run_id)
        
        # 结束
        self._emit("AgentFinished", {
            "final_output": "Tool execution completed with policy enforcement"
        }, parent_id=run_id)
        return "Done"

if __name__ == "__main__":
    bus = EventBus()
    
    # 控制台打印
    bus.subscribe(lambda ev: print(f"[EVIDENCE] {ev}"))
    
    # 证据持久化
    log_file = f"evidence_guard_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    def write_to_file(ev):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    bus.subscribe(write_to_file)
    
    # 🔐 安装 Guard（策略引擎）
    guard = install_guard(bus, config_path="guard_config.json")
    print("[GUARD] 🛡️  Guard policy engine installed!")
    
    # 运行 Agent
    agent = ToolAgent(agent_id="demo_tool_agent", event_bus=bus)
    result = agent.run("Test tool calls with Guard")
    print(f"\n[RESULT] {result}")
    print(f"[INFO] Evidence saved to {log_file}")
