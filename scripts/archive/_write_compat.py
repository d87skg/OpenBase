import os

content = '''# Compatibility Policy

## Versioning

OpenBase follows **Semantic Versioning 2.0.0** with protocol-specific extensions.

| Version Change | Meaning |
|:---|:---|
| MAJOR (2.x → 3.0) | Breaking changes to Stable Core schemas |
| MINOR (2.0 → 2.1) | New event types, optional fields, new transports |
| PATCH (2.0.0 → 2.0.1) | Bug fixes, documentation, non-normative changes |

## Backward Compatibility

- Evidence generated under v2.0 MUST be verifiable under any v2.x
- OBS events valid under v2.0 MUST remain valid under any v2.x
- Certificates issued under v2.0 MUST remain verifiable under any v2.x

## Deprecation

- Features deprecated in a MINOR release will be removed in the next MAJOR release
- Deprecation notices will be included in CHANGELOG.md
- Minimum 6-month deprecation period before removal
'''

path = r'D:\OpenBase\COMPATIBILITY.md'
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('COMPATIBILITY.md created')
