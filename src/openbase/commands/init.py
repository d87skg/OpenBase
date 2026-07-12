from openbase.core.registry import Registry
from pathlib import Path


def cmd_init(args):
    name = args.name or "my-openbase-project"
    force = args.force

    if Path(name).exists() and not force:
        print(f"❌ 目录 {name} 已存在，使用 --force 覆盖")
        return

    Path(name).mkdir(exist_ok=True)
    Path(f"{name}/agents").mkdir(exist_ok=True)
    Path(f"{name}/evidence").mkdir(exist_ok=True)
    Path(f"{name}/reports").mkdir(exist_ok=True)

    Registry().register_runtime({
        "name": "OpenClaw",
        "version": "1.0.0"
    })

    print(f"✅ 项目已初始化: {name}")
