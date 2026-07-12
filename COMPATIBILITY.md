# Compatibility Policy

## Versioning

Semantic Versioning 2.0.0 with protocol-specific extensions.

| Version | Meaning |
|:---|:---|
| MAJOR (2.x to 3.0) | Breaking changes to Stable Core |
| MINOR (2.0 to 2.1) | New event types, optional fields, new transports |
| PATCH | Bug fixes, docs |

## Backward Compatibility

- Evidence v2.0 verifiable under any v2.x
- OBS events remain valid under any v2.x
- Certificates remain verifiable under any v2.x

## Deprecation

- Minimum 6-month deprecation period
- Notices in CHANGELOG.md
