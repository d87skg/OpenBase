from openbase.core.registry import Registry


def cmd_registry(args):
    registry = Registry()

    if args.action == "list":
        data = registry.get_runtime()
        if data:
            print(f"📋 Runtime:")
            print(f"   Name: {data.get('name', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
        else:
            print("📋 尚无 Runtime")
            print("   提示: 请先运行 'openbase init' 初始化项目")
