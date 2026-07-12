"""
openbase node - Runtime Node 管理
"""

from datetime import datetime
from ..state import add_node, get_node, remove_node, get_nodes, update_node


def cmd_node(args):
    if args.action == "start":
        if get_node(args.id):
            print(f"⚠️ 节点 {args.id} 已存在")
            return

        node_data = {
            "node_id": args.id,
            "port": args.port or 8001,
            "status": "RUNNING",
            "trust_score": 0.5,
            "evidence_count": 0,
            "peers": [],
            "started_at": datetime.now().isoformat()
        }
        add_node(node_data)
        print(f"✅ 节点已启动: {args.id} (port: {args.port or 8001})")
        print(f"   📋 Node: {args.id}")
        print(f"   🔌 Port: {args.port or 8001}")
        print(f"   📊 Status: RUNNING")

    elif args.action == "stop":
        if not get_node(args.id):
            print(f"❌ 节点 {args.id} 不存在")
            return
        remove_node(args.id)
        print(f"🛑 节点已停止: {args.id}")

    elif args.action == "list":
        nodes = get_nodes()
        if not nodes:
            print("📋 暂无运行中的节点")
            return
        print(f"📋 共 {len(nodes)} 个节点:")
        for nid, node in nodes.items():
            print(f"   {nid} | {node.get('status')} | port: {node.get('port')} | trust: {node.get('trust_score')}")

    elif args.action == "status":
        node = get_node(args.id)
        if not node:
            print(f"❌ 节点 {args.id} 不存在")
            return
        print(f"📋 节点状态: {args.id}")
        print(f"   Status: {node.get('status')}")
        print(f"   Port: {node.get('port')}")
        print(f"   Trust Score: {node.get('trust_score')}")
        print(f"   Evidence: {node.get('evidence_count')}")
        print(f"   Peers: {', '.join(node.get('peers', [])) or 'None'}")
        print(f"   Started: {node.get('started_at')}")

    elif args.action == "join":
        node = get_node(args.id)
        if not node:
            print(f"❌ 节点 {args.id} 不存在")
            return
        if not get_node(args.peer):
            print(f"❌ 目标节点 {args.peer} 不存在")
            return
        peers = node.get("peers", [])
        if args.peer not in peers:
            peers.append(args.peer)
            update_node(args.id, {"peers": peers})
            print(f"🔗 {args.id} 已连接到 {args.peer}")

    else:
        print("❌ 未知命令: openbase node", args.action)
