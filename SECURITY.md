# Security Policy

## Reporting

Email: security@openbase.dev
Response: 48 hours

## Supported Versions

| Version | Supported |
|:---|:---|
| 2.0.x | Yes |

## Cryptographic Dependencies

- Signatures: Ed25519 (cryptography library)
- Hashing: SHA-256 (hashlib)
- Canonical JSON: RFC 8785

## Security Considerations

- Private keys should never be committed to VCS
- Use HSM for production key storage
- Evidence chains are append-only and tamper-detectable
