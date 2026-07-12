#!/usr/bin/env python3
import sys
import argparse
import json
import requests

DEFAULT_REGISTRY_URL = "http://localhost:8000"


def health_check(args):
    try:
        resp = requests.get(f"{args.registry}/health")
        print(f"✅ Registry 状态: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))
    except Exception as e:
        print(f"❌ 连接失败: {e}")


def runtime_register(args):
    data = {
        "name": args.name,
        "version": args.version,
        "vendor": args.vendor,
        "runtime_class": args.runtime_class or "STANDARD",
        "capabilities": args.capabilities.split(",") if args.capabilities else [],
        "description": args.description
    }
    try:
        resp = requests.post(f"{args.registry}/runtimes/register", json=data)
        if resp.status_code == 200:
            print(f"✅ Runtime 注册成功")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ 注册失败: {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def runtime_list(args):
    try:
        resp = requests.get(f"{args.registry}/runtimes/")
        if resp.status_code == 200:
            runtimes = resp.json()
            print(f"✅ 共 {len(runtimes)} 个 Runtime:")
            for r in runtimes:
                print(f"  - {r['name']} ({r['runtime_id']}) | {r['status']} | {r['runtime_class']}")
        else:
            print(f"❌ 请求失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def runtime_get(args):
    try:
        resp = requests.get(f"{args.registry}/runtimes/{args.runtime_id}")
        if resp.status_code == 200:
            r = resp.json()
            print(f"✅ Runtime 详情:")
            print(f"  ID: {r['runtime_id']}")
            print(f"  名称: {r['name']}")
            print(f"  版本: {r['version']}")
            print(f"  供应商: {r['vendor']}")
            print(f"  状态: {r['status']}")
            print(f"  类型: {r['runtime_class']}")
            print(f"  能力: {', '.join(r.get('capabilities', []))}")
            print(f"  描述: {r.get('description', 'N/A')}")
        else:
            print(f"❌ Runtime 不存在: {args.runtime_id}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def evidence_push(args):
    data = {
        "runtime_id": args.runtime_id,
        "execution_id": args.execution_id,
        "event_type": args.event_type,
        "payload": json.loads(args.payload) if args.payload else {}
    }
    try:
        resp = requests.post(f"{args.registry}/evidence/", json=data)
        if resp.status_code == 200:
            print(f"✅ 证据推送成功")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ 推送失败: {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def certificate_issue(args):
    data = {
        "runtime_id": args.runtime_id,
        "runtime_name": args.runtime_name or "Unknown",
        "level": args.level or "SILVER",
        "trust_score": float(args.trust_score) if args.trust_score else 0.85,
        "verification_summary": {"status": "PASS"}
    }
    try:
        resp = requests.post(f"{args.registry}/certificates/issue", json=data)
        if resp.status_code == 200:
            print(f"✅ 证书颁发成功")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ 颁发失败: {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def trust_ranking(args):
    try:
        resp = requests.get(f"{args.registry}/trust/ranking?limit={args.limit or 10}")
        if resp.status_code == 200:
            records = resp.json()
            if records:
                print(f"✅ 信任排名 (前 {len(records)}):")
                for i, r in enumerate(records, 1):
                    print(f"  {i}. {r['runtime_name']} - 信任分: {r['trust_score']:.2f}")
            else:
                print("📭 暂无信任记录")
        else:
            print(f"❌ 请求失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def reality_build(args):
    url = f"{args.registry}/reality/build/{args.runtime_id}"
    try:
        resp = requests.post(url)
        if resp.status_code == 200:
            print("✅ Reality Graph built")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ Failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def reality_query(args):
    url = f"{args.registry}/reality/query"
    data = {"claim": args.claim}
    try:
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            print("✅ Reality Query Result:")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ Failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def reality_conflicts(args):
    url = f"{args.registry}/reality/conflicts"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            print("✅ Conflicts detected:")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"❌ Failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def state_cmd(args):
    """处理 state 命令"""
    if args.action == "world":
        url = f"{args.registry}/state/world"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print("🌍 World State:")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"❌ Failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    elif args.action == "all":
        url = f"{args.registry}/state/all"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print("📊 All States:")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"❌ Failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    elif args.action == "replay":
        url = f"{args.registry}/state/replay?execution_id={args.execution_id}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f"🔄 Replay for execution {args.execution_id}:")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"❌ Failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    elif args.action == "history":
        url = f"{args.registry}/state/history?limit={args.limit or 10}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f"📜 History (last {args.limit or 10}):")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"❌ Failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    elif args.action == "trust":
        url = f"{args.registry}/state/trust/{args.runtime_id}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f"🔒 Trust for {args.runtime_id}:")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"❌ Failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Unknown state action")
        print("Available: world, all, replay, history, trust")


def main():
    parser = argparse.ArgumentParser(description="OpenBase CLI")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_URL)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # health
    subparsers.add_parser("health")

    # runtime
    runtime_parser = subparsers.add_parser("runtime")
    runtime_sub = runtime_parser.add_subparsers(dest="action", required=True)

    r_reg = runtime_sub.add_parser("register")
    r_reg.add_argument("--name", required=True)
    r_reg.add_argument("--version", required=True)
    r_reg.add_argument("--vendor", required=True)
    r_reg.add_argument("--runtime-class", choices=["CORE", "STANDARD", "ENTERPRISE", "REFERENCE"])
    r_reg.add_argument("--capabilities")
    r_reg.add_argument("--description")

    runtime_sub.add_parser("list")

    r_get = runtime_sub.add_parser("get")
    r_get.add_argument("runtime_id")

    # evidence
    evidence_parser = subparsers.add_parser("evidence")
    evidence_sub = evidence_parser.add_subparsers(dest="action", required=True)

    e_push = evidence_sub.add_parser("push")
    e_push.add_argument("--runtime-id", required=True)
    e_push.add_argument("--execution-id", required=True)
    e_push.add_argument("--event-type", required=True)
    e_push.add_argument("--payload", help="JSON string")

    # certificate
    cert_parser = subparsers.add_parser("certificate")
    cert_sub = cert_parser.add_subparsers(dest="action", required=True)

    c_issue = cert_sub.add_parser("issue")
    c_issue.add_argument("--runtime-id", required=True)
    c_issue.add_argument("--runtime-name")
    c_issue.add_argument("--level", choices=["BRONZE", "SILVER", "GOLD", "PLATINUM"])
    c_issue.add_argument("--trust-score")

    # trust
    trust_parser = subparsers.add_parser("trust")
    trust_sub = trust_parser.add_subparsers(dest="action", required=True)

    t_rank = trust_sub.add_parser("ranking")
    t_rank.add_argument("--limit", type=int, default=10)

    # reality
    reality_parser = subparsers.add_parser("reality")
    reality_sub = reality_parser.add_subparsers(dest="action", required=True)

    r_build = reality_sub.add_parser("build")
    r_build.add_argument("--runtime-id", required=True)

    r_query = reality_sub.add_parser("query")
    r_query.add_argument("--claim", required=True)

    r_conf = reality_sub.add_parser("conflicts")
    r_conf.add_argument("--threshold", type=float, default=0.2)

    # state
    state_parser = subparsers.add_parser("state")
    state_sub = state_parser.add_subparsers(dest="action", required=True)

    s_world = state_sub.add_parser("world")
    s_all = state_sub.add_parser("all")
    s_replay = state_sub.add_parser("replay")
    s_replay.add_argument("--execution-id", required=True)
    s_history = state_sub.add_parser("history")
    s_history.add_argument("--limit", type=int, default=10)
    s_trust = state_sub.add_parser("trust")
    s_trust.add_argument("--runtime-id", required=True)

    args = parser.parse_args()

    if args.command == "health":
        health_check(args)
    elif args.command == "runtime":
        if args.action == "register":
            runtime_register(args)
        elif args.action == "list":
            runtime_list(args)
        elif args.action == "get":
            runtime_get(args)
    elif args.command == "evidence":
        if args.action == "push":
            evidence_push(args)
    elif args.command == "certificate":
        if args.action == "issue":
            certificate_issue(args)
    elif args.command == "trust":
        if args.action == "ranking":
            trust_ranking(args)
    elif args.command == "reality":
        if args.action == "build":
            reality_build(args)
        elif args.action == "query":
            reality_query(args)
        elif args.action == "conflicts":
            reality_conflicts(args)
    elif args.command == "state":
        state_cmd(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
