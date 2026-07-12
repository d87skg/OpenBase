# OpenBase Certificate Specification v1.0

## Version
**1.0**

## Status
**Draft**

---

## 1. Abstract

The Certificate Layer defines formal trust credentials issued to Runtimes and Agents. A Certificate is a signed, verifiable attestation that a subject meets specific trust criteria at a point in time.

## 2. Certificate Model

### 2.1 Core Principle

A Certificate is:
- Issued based on verifiable Trust Score
- Signed by the OpenBase Registry
- Time-bounded with explicit expiry
- Revocable if trust conditions degrade

### 2.2 Certificate Levels

| Level | Min Score | Min Evidence | Description |
|:---|:---|:---|:---|
| BRONZE | 0.30 | 10 | Basic participation |
| SILVER | 0.50 | 50 | Consistent good behavior |
| GOLD | 0.70 | 100 | High trust, peer verified |
| PLATINUM | 0.90 | 500 | Exceptional trust record |

### 2.3 Certificate Lifecycle

`
Issued → Active → Expiring → Expired
                 ↓
              Revoked
`

- Issued: Created after trust threshold met
- Active: Valid and usable
- Expiring: Within renewal window
- Expired: Past validity period
- Revoked: Explicitly invalidated before expiry

## 3. Certificate Structure

A Certificate contains:
- Subject identity
- Issuer identity
- Trust level achieved
- Evidence snapshot (scores at issuance time)
- Validity period (issued_at, expires_at)
- Digital signature from Registry

## 4. Verification

Anyone can verify a Certificate by:
1. Check signature against Registry public key
2. Verify subject identity exists in Registry
3. Confirm certificate not expired or revoked
4. Optionally: re-verify current Trust Score meets level

## 5. Renewal

Certificates auto-renew if:
- Current Trust Score still meets level threshold
- Subject is active (evidence in last 30 days)
- Certificate not revoked

## 6. Revocation

Grounds for revocation:
- Trust Score drops below level threshold
- Evidence of malicious behavior
- Subject voluntarily requests revocation
- Subject identity deprecated or retired

## 7. References

- Trust v1.0 (trust score computation)
- Identity v1.0 (subject identification)
- Evidence v2.0 (evidence verification)
- Registry v1.0 (issuer authority)
