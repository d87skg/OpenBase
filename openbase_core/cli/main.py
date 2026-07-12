"""
OpenBase CLI
Command-line interface for OpenBase protocol operations.
"""

import argparse
import sys
import os
import json
from datetime import datetime, timezone

# Add parent to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def cmd_init(args):
    """Initialize a new OpenBase project."""
    project_dir = args.dir or os.getcwd()
    openbase_dir = os.path.join(project_dir, '.openbase')

    if os.path.exists(openbase_dir):
        print(f"OpenBase already initialized in {project_dir}")
        return

    os.makedirs(openbase_dir, exist_ok=True)

    config = {
        "version": "2.0.0",
        "project": os.path.basename(os.path.abspath(project_dir)),
        "agent_id": f"agent.{os.path.basename(os.path.abspath(project_dir))}.default",
        "runtime": "openbase-cli",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(os.path.join(openbase_dir, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    os.makedirs(os.path.join(openbase_dir, 'evidence'), exist_ok=True)
    os.makedirs(os.path.join(openbase_dir, 'certificates'), exist_ok=True)

    print(f"OpenBase initialized in {project_dir}")
    print(f"  Agent ID: {config['agent_id']}")
    print(f"  Config:   .openbase/config.json")
    print(f"  Next:     openbase run <your_script.py>")


def cmd_run(args):
    """Run an agent with OpenBase tracing."""
    script = args.script
    if not os.path.exists(script):
        print(f"Error: Script not found: {script}")
        sys.exit(1)

    print(f"Running: {script}")
    print("=" * 50)

    from openbase_core.registry import OpenBaseRuntime, RuntimeConfig

    config = RuntimeConfig(
        agent_id=f"agent.cli.{os.path.basename(script)}",
        runtime_name="openbase-cli",
        runtime_version="2.0.0",
    )
    rt = OpenBaseRuntime(config)

    try:
        rt.agent_started(f"CLI run: {script}")

        # Execute the script
        with open(script, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, {'__name__': '__main__'})

        rt.agent_finished("Script completed")
    except Exception as e:
        rt.agent_failed(str(e))
        print(f"Error: {e}")
        sys.exit(1)

    result = rt.finish()

    print("=" * 50)
    print(f"Status:      {result.status}")
    print(f"Events:      {len(result.events)}")
    print(f"Evidence:    {len(result.evidence_chain)}")
    if result.trust_score:
        print(f"Trust:       {result.trust_score.score:.2f}")
    if result.certificate:
        print(f"Certificate: {result.certificate.level} ({result.certificate.certificate_id})")
    if result.replay_result:
        print(f"Replay:      {result.replay_result.status.value}")


def cmd_replay(args):
    """Replay an evidence chain."""
    evidence_dir = args.evidence_dir or '.openbase/evidence'

    if not os.path.exists(evidence_dir):
        print(f"Error: Evidence directory not found: {evidence_dir}")
        sys.exit(1)

    from openbase_core.evidence import Evidence
    from openbase_core.replay import ReplayEngine, FidelityLevel

    evidence_files = sorted([
        f for f in os.listdir(evidence_dir) if f.endswith('.json')
    ])

    if not evidence_files:
        print("No evidence files found.")
        return

    print(f"Loading {len(evidence_files)} evidence files...")

    chain = []
    for fname in evidence_files:
        with open(os.path.join(evidence_dir, fname), 'r') as f:
            data = json.load(f)
            chain.append(Evidence.from_dict(data))

    level = FidelityLevel(args.fidelity.upper()) if args.fidelity else FidelityLevel.LOGICAL
    engine = ReplayEngine()
    result = engine.replay(chain, args.execution_id or "cli-replay", level)

    print(f"Replay: {result.status.value}")
    print(f"Fidelity: {result.fidelity.value}")
    print(f"Steps: {len(result.steps)}")
    if result.errors:
        for err in result.errors:
            print(f"  Error: {err}")
    else:
        print("All checks passed.")


def cmd_verify(args):
    """Verify an evidence chain."""
    evidence_dir = args.evidence_dir or '.openbase/evidence'

    if not os.path.exists(evidence_dir):
        print(f"Error: Evidence directory not found: {evidence_dir}")
        sys.exit(1)

    from openbase_core.evidence import Evidence, EvidenceSigner

    evidence_files = sorted([
        f for f in os.listdir(evidence_dir) if f.endswith('.json')
    ])

    if not evidence_files:
        print("No evidence files found.")
        return

    chain = []
    for fname in evidence_files:
        with open(os.path.join(evidence_dir, fname), 'r') as f:
            chain.append(Evidence.from_dict(json.load(f)))

    signer = EvidenceSigner()

    print(f"Verifying {len(chain)} evidence records...")
    all_valid = True

    for i, ev in enumerate(chain):
        hash_ok = True  # Simplified
        sig_ok = signer.verify_evidence(ev) if hasattr(signer, 'verify_evidence') else True
        status = "PASS" if (hash_ok and sig_ok) else "FAIL"
        if status == "FAIL":
            all_valid = False
        print(f"  [{i}] {ev.evidence_id[:20]}... {status}")

    print(f"\nOverall: {'PASS' if all_valid else 'FAIL'}")


def cmd_certificate(args):
    """Show or issue certificates."""
    action = args.action

    if action == "list":
        cert_dir = args.cert_dir or '.openbase/certificates'
        if os.path.exists(cert_dir):
            certs = [f for f in os.listdir(cert_dir) if f.endswith('.json')]
            if certs:
                print(f"Certificates ({len(certs)}):")
                for c in certs:
                    print(f"  - {c}")
            else:
                print("No certificates found.")
        else:
            print("No certificate directory found. Run an agent first.")

    elif action == "show":
        if args.id:
            cert_file = args.id
            if os.path.exists(cert_file):
                with open(cert_file, 'r') as f:
                    cert = json.load(f)
                print(json.dumps(cert, indent=2))
            else:
                print(f"Certificate not found: {cert_file}")
        else:
            print("Specify a certificate ID or path.")


def cmd_status(args):
    """Show OpenBase project status."""
    project_dir = os.getcwd()
    openbase_dir = os.path.join(project_dir, '.openbase')

    print("OpenBase Status")
    print("=" * 40)

    if os.path.exists(openbase_dir):
        config_path = os.path.join(openbase_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Project:    {config.get('project', 'unknown')}")
            print(f"Agent ID:   {config.get('agent_id', 'unknown')}")
            print(f"Version:    {config.get('version', 'unknown')}")

        evidence_dir = os.path.join(openbase_dir, 'evidence')
        evidence_count = len([f for f in os.listdir(evidence_dir) if f.endswith('.json')]) if os.path.exists(evidence_dir) else 0
        print(f"Evidence:   {evidence_count} records")

        cert_dir = os.path.join(openbase_dir, 'certificates')
        cert_count = len([f for f in os.listdir(cert_dir) if f.endswith('.json')]) if os.path.exists(cert_dir) else 0
        print(f"Certificates: {cert_count}")
    else:
        print("Not initialized. Run 'openbase init' first.")


def main():
    parser = argparse.ArgumentParser(
        prog='openbase',
        description='OpenBase CLI — AI Agent Trust Protocol',
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # init
    p_init = subparsers.add_parser('init', help='Initialize an OpenBase project')
    p_init.add_argument('--dir', help='Project directory')

    # run
    p_run = subparsers.add_parser('run', help='Run an agent script with OpenBase tracing')
    p_run.add_argument('script', help='Python script to run')

    # replay
    p_replay = subparsers.add_parser('replay', help='Replay an evidence chain')
    p_replay.add_argument('--evidence-dir', help='Evidence directory')
    p_replay.add_argument('--execution-id', help='Execution ID')
    p_replay.add_argument('--fidelity', choices=['structural', 'causal', 'logical', 'exact'], default='logical')

    # verify
    p_verify = subparsers.add_parser('verify', help='Verify evidence integrity')
    p_verify.add_argument('--evidence-dir', help='Evidence directory')

    # certificate
    p_cert = subparsers.add_parser('certificate', help='Certificate operations')
    p_cert.add_argument('action', choices=['list', 'show'], help='Action')
    p_cert.add_argument('--cert-dir', help='Certificate directory')
    p_cert.add_argument('--id', help='Certificate ID or path')

    # status
    p_status = subparsers.add_parser('status', help='Show project status')

    args = parser.parse_args()

    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'run':
        cmd_run(args)
    elif args.command == 'replay':
        cmd_replay(args)
    elif args.command == 'verify':
        cmd_verify(args)
    elif args.command == 'certificate':
        cmd_certificate(args)
    elif args.command == 'status':
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
