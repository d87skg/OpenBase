from openbase.core.certificate import CertificateEngine


def cmd_certificate(args):
    if args.action == "issue":
        engine = CertificateEngine()
        cert = engine.issue(level=args.level)
        print(f"✅ 证书已颁发: {cert['certificate_id']} ({cert['level']})")
