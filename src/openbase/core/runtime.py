class Runtime:
    def __init__(self, name: str):
        self.name = name

    def execute(self, agent_file: str):
        print(f"🚀 运行 Agent: {agent_file}")
        return {"status": "ok", "runtime": self.name}
