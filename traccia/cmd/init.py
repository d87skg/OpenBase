#!/usr/bin/env python3
"""
openbase init - 初始化 OpenBase 项目
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw"))

from runtime.registry.client import RegistryClient


def run_init(args):
    project_name = args.name or "my-openbase-project"
    project_path = Path(project_name)

    if project_path.exists() and not args.force:
        print(f"❌ 目录 {project_name} 已存在，使用 --force 覆盖")
        return 1

    if not args.name:
        print("📋 未指定项目名称，使用默认: my-openbase-project")
        print("   提示: 使用 'openbase init <项目名>' 自定义名称")

    project_path.mkdir(exist_ok=True)
    (project_path / "agents").mkdir(exist_ok=True)
    (project_path / "evidence").mkdir(exist_ok=True)
    (project_path / "reports").mkdir(exist_ok=True)
    (project_path / ".openbase").mkdir(exist_ok=True)
    (project_path / ".openbase/registry").mkdir(parents=True, exist_ok=True)

    (project_path / "openbase.yaml").write_text(
        f"""# OpenBase 配置文件
project: {project_name}
version: 1.0.0

registry:
  path: ./.openbase/registry

runtime:
  name: OpenClaw
  vendor: OpenBase

evidence:
  storage: ./evidence
  format: jsonl
""",
        encoding="utf-8"
    )

    (project_path / "agents" / "main.py").write_text(
        '"""示例 Agent"""\n\ndef run():\n    print("🚀 正在运行 Agent...")\n    print("✅ Agent 执行完成")\n    return {"status": "success", "output": "Hello, OpenBase!"}\n\nif __name__ == "__main__":\n    run()\n',
        encoding="utf-8"
    )

    (project_path / "README.md").write_text(
        f"""# {project_name}

OpenBase 项目

## 快速开始

```bash
cd {project_name}
openbase run agents/main.py
""",
encoding="utf-8"
)

registry = RegistryClient(str(project_path / ".openbase/registry"))
registry.register_runtime(
name="OpenClaw",
version="1.0.0",
vendor="OpenBase",
capabilities=["execution", "evidence", "replay"]
)

print(f"✅ OpenBase 项目已初始化: {project_name}")
print(f" 📁 目录: {project_path.absolute()}")
print(f" 📄 配置文件: openbase.yaml")
print(f" 🤖 示例 Agent: agents/main.py")
print(f" 📋 Registry: .openbase/registry/")
print()
print("下一步:")
print(f" cd {project_name}")
print(" openbase run agents/main.py")
return 0

def main():
parser = argparse.ArgumentParser(description="初始化 OpenBase 项目")
parser.add_argument("name", nargs="?", default=None, help="项目名称")
parser.add_argument("--force", action="store_true", help="覆盖已存在的目录")
args = parser.parse_args()
sys.exit(run_init(args))

if name == "main":
main()
