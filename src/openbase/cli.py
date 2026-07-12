import argparse
from openbase.commands.init import cmd_init
from openbase.commands.run import cmd_run
from openbase.commands.certificate import cmd_certificate
from openbase.commands.registry import cmd_registry
from openbase.commands.replay import cmd_replay
from openbase.commands.trust import cmd_trust
from openbase.commands.test import cmd_test
from openbase.commands.doctor import cmd_doctor
from openbase.commands.mesh import cmd_mesh
from openbase.commands.node import cmd_node


def main():
    parser = argparse.ArgumentParser(prog="openbase", description="OpenBase CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="初始化项目")
    p_init.add_argument("name", nargs="?", default=None, help="项目名称")
    p_init.add_argument("--force", action="store_true", help="覆盖已存在目录")
    p_init.set_defaults(func=cmd_init)

    # run
    p_run = sub.add_parser("run", help="运行 Agent")
    p_run.add_argument("file", help="Agent 文件路径")
    p_run.set_defaults(func=cmd_run)

    # certificate
    p_cert = sub.add_parser("certificate", help="证书管理")
    p_cert.add_argument("action", choices=["issue"])
    p_cert.add_argument("--level", default="BRONZE", choices=["BRONZE", "SILVER", "GOLD", "PLATINUM"])
    p_cert.set_defaults(func=cmd_certificate)

    # registry
    p_reg = sub.add_parser("registry", help="Registry 管理")
    p_reg.add_argument("action", choices=["list"])
    p_reg.set_defaults(func=cmd_registry)

    # replay
    p_replay = sub.add_parser("replay", help="重放执行过程")
    p_replay.add_argument("--evidence-dir", default="./evidence", help="证据目录")
    p_replay.set_defaults(func=cmd_replay)

    # trust
    p_trust = sub.add_parser("trust", help="信任管理")
    p_trust.add_argument("--level", default="simple", choices=["simple"], help="信任提供者")
    p_trust.set_defaults(func=cmd_trust)

    # test
    p_test = sub.add_parser("test", help="运行一致性测试")
    p_test.add_argument("--evidence-dir", default="./evidence", help="证据目录")
    p_test.set_defaults(func=cmd_test)

    # doctor
    p_doctor = sub.add_parser("doctor", help="系统诊断")
    p_doctor.set_defaults(func=cmd_doctor)

    # mesh
    p_mesh = sub.add_parser("mesh", help="Execution Mesh 管理")
    p_mesh.add_argument("action", choices=["status", "list", "sync"])
    p_mesh.set_defaults(func=cmd_mesh)

    # node
    p_node = sub.add_parser("node", help="Runtime Node 管理")
    p_node.add_argument("action", choices=["start", "stop", "list", "status", "join"])
    p_node.add_argument("--id", help="节点 ID")
    p_node.add_argument("--port", type=int, default=8001, help="节点端口")
    p_node.add_argument("--peer", help="加入的目标节点 ID")
    p_node.set_defaults(func=cmd_node)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
