import sys
from pathlib import Path


def cmd_doctor(args):
    print("🏥 OpenBase 系统诊断")
    print("=" * 40)

    # Python 版本
    print(f"🐍 Python: {sys.version.split()[0]}")

    # 当前目录
    print(f"📁 当前目录: {Path.cwd()}")

    # 检查 openbase 包
    try:
        import openbase
        print(f"📦 OpenBase: {openbase.__version__}")
    except:
        print("❌ OpenBase 未安装")

    # 检查项目文件
    if Path("openbase.yaml").exists():
        print("✅ openbase.yaml 存在")
    else:
        print("⚠️ openbase.yaml 不存在 (请运行 'openbase init')")

    # 检查证据
    ev_dir = Path("evidence")
    if ev_dir.exists():
        files = list(ev_dir.glob("*.json"))
        print(f"📄 证据文件: {len(files)} 条")
    else:
        print("⚠️ evidence/ 目录不存在 (请运行 'openbase run')")

    print("=" * 40)
    print("✅ 诊断完成")
