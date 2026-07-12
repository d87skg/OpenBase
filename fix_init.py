import os

os.makedirs("traccia/cmd", exist_ok=True)

content = '''#!/usr/bin/env python3
"""
openbase init - 初始化 OpenBase 项目
"""

import sys
import argparse
from pathlib import Path


def run_init(args):
    project_name = args.name or "my-openbase-project"
    project_path = Path(project_name)

    if project_path.exists() and not args.force:
        print(f"❌ 目录 {project_name} 已存在，使用 --force 覆盖")
        return 1

    project_path.mkdir(exist_ok=True)
    (project_path / "agents").mkdir(exist_ok=True)
    (project_path / "evidence").mkdir(exist_ok=True)
    (project_path / "reports").mkdir(exist_ok=True)

    (project_path / "openbase.yaml").write_text(
        f"""# OpenBase 配置文件
project: {project_name}
version: 1.0.0

registry:
  url: http://localhost:8000

runtime:
  name: OpenClaw
  vendor: OpenBase

evidence:
  storage: ./evidence
  format: jsonl
""",
        encoding="utf-8",
    )

    (project_path / "agents" / "main.py").write_text(
        '"""示例 Agent"""\\n\\ndef run():\\n    print("🚀 正在运行 Agent...")\\n    print("✅ Agent 执行完成")\\n    return {"status": "success", "output": "Hello, OpenBase!"}\\n\\nif __name__ == "__main__":\\n    run()\\n',
        encoding="utf-8",
    )

    (project_path / "README.md").write_text(
        f"""# {project_name}

OpenBase 项目

## 快速开始

```bash
cd {project_name}
openbase run agents/main.py
```
""",
        encoding="utf-8",
    )

    print(f"✅ OpenBase 项目已初始化: {project_name}")
    print(f"   📁 目录: {project_path.absolute()}")
    print(f"   📄 配置文件: openbase.yaml")
    print(f"   🤖 示例 Agent: agents/main.py")
    print()
    print("下一步:")
    print(f"   cd {project_name}")
    print("   openbase run agents/main.py")
    return 0


def main():
    parser = argparse.ArgumentParser(description="初始化 OpenBase 项目")
    parser.add_argument("name", nargs="?", default="my-openbase-project", help="项目名称")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的目录")
    args = parser.parse_args()
    sys.exit(run_init(args))


if __name__ == "__main__":
    main()
'''

with open("traccia/cmd/init.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ traccia/cmd/init.py 已重新生成（缩进正确）")