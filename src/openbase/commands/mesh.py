"""
openbase mesh - Execution Mesh 管理
"""

from ..state import get_nodes, update_node


def cmd_mesh(args):
    nodes = get_nodes()

    if args.action == "status":
        node_count = len(nodes)
        print("🌐 OpenBase Execution Mesh")
        print(f"   Status: {'MULTI_NODE' if node_count > 1 else 'SINGLE_NODE'}")
        print(f"   Nodes: {node_count}")

        if node_count > 0:
            print("   Node Summary:")
            for nid, node in nodes.items():
                peer_count = len(node.get("peers", []))
                print(f"      {nid} | {node.get('status')} | trust: {node.get('trust_score')} | peers: {peer_count}")

    elif args.action == "list":
        if not nodes:
            print("📋 暂无节点")
            return
        print("📋 Registered Nodes:")
        for nid, node in nodes.items():
            peer_label = f"peers: {len(node.get('peers', []))}" if node.get('peers') else "no peers"
            print(f"   {nid} ({node.get('status')}) | trust: {node.get('trust_score')} | {peer_label}")

    elif args.action == "sync":
        print("🔄 同步 Mesh 状态...")
        for nid, node in nodes.items():
            if node.get("peers"):
                update_node(nid, {"trust_score": min(1.0, node.get("trust_score", 0.5) + 0.05)})
        print("✅ 同步完成")

    else:
        print("❌ 未知命令: openbase mesh", args.action)
