import os

content = '''# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in OpenBase, please **do not** open a public issue.

Email: security@openbase.dev (placeholder)

Response time: 48 hours

## Supported Versions

| Version | Supported |
|:---|:---|
| 2.0.x | Yes |

## Cryptographic Dependencies

- **Signatures**: Ed25519 (via Python cryptography library)
- **Hashing**: SHA-256 (via Python hashlib)
- **Canonical JSON**: RFC 8785

## Security Considerations

- Private keys should never be committed to version control
- Production deployments should use hardware security modules (HSM) for key storage
- Evidence chains are append-only; tampering is detectable but not preventable
'''

path = r'D:\OpenBase\SECURITY.md'
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('SECURITY.md created')
