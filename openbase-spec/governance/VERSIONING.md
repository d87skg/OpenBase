# OpenBase Versioning Policy

**Version**: 1.0
**Status**: Active
**Adopted**: 2026-07-18

---

## Protocol Versioning

OpenBase follows **Semantic Versioning 2.0.0** with protocol-specific extensions.

| Version Change | Meaning | Example |
|---------------|---------|---------|
| **MAJOR** (X.0.0) | Breaking changes to Stable Core schemas | Evidence schema incompatible with previous |
| **MINOR** (X.Y.0) | New event types, optional fields, new transports | New OBS event type added |
| **PATCH** (X.Y.Z) | Bug fixes, documentation, non-normative changes | Typo fix in spec |

## Stable Core Freeze

The following layers are frozen as of v2.0.0:

| Layer | Version | Frozen Since |
|-------|---------|-------------|
| OBS (Event) | v1.0 | 2026-07-09 |
| Evidence | v2.0 | 2026-07-09 |
| Replay | v1.0 | 2026-07-09 |
| Identity | v1.0 | 2026-07-09 |
| Trust | v1.0 | 2026-07-09 |
| Certificate | v1.0 | 2026-07-09 |
| Transport | v1.0 | 2026-07-09 |

## Compatibility Promise

1. Evidence generated under v2.0 MUST be verifiable under any v2.x
2. OBS events valid under v1.0 MUST remain valid under any v1.x
3. Certificates issued under v1.0 MUST remain verifiable under any v1.x
4. Conformance tests passing under current version MUST pass under any patch version

## Deprecation Policy

1. Features deprecated in MINOR release will be removed in next MAJOR release
2. Minimum 6-month deprecation period
3. Deprecation notices in CHANGELOG.md
4. Migration guide provided for all breaking changes

## Schema Versioning

Each JSON Schema includes a ersion field. Schema versions are independent of protocol versions:
- Schema major version changes when required fields are added/removed
- Schema minor version changes when optional fields are added

## Reference Implementation Versioning

The reference implementation (openbase_core) follows the same version as the protocol it implements.
