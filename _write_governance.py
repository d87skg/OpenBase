import os

content = '''# OpenBase Governance

## Decision-Making Process

OpenBase follows a merit-based governance model.

### Roles

- **Maintainers**: Core protocol stewards with merge permissions
- **Contributors**: Anyone who submits accepted PRs
- **Community**: Users, adopters, and ecosystem partners

### OBEP Process

The **OpenBase Enhancement Proposal** (OBEP) is the formal mechanism for proposing changes to the Stable Core.

1. **Proposal**: Submit an OBEP as a GitHub Issue using the OBEP template
2. **Discussion**: Community discussion period (minimum 2 weeks)
3. **Vote**: Maintainers vote (majority required)
4. **RFC**: Accepted proposals become RFC documents
5. **Implementation**: RFC is implemented in openbase_core
6. **Release**: Included in next minor or major release

### What Requires an OBEP

- Breaking changes to any Stable Core schema
- New required fields in existing schemas
- Removal of event types from OBS
- Changes to hash or signature algorithms

### What Does NOT Require an OBEP

- New event types added to OBS registry
- New optional fields
- New transport protocol support
- Documentation improvements
- Bug fixes

### Extensions

Extensions (Policy, Compliance, Risk, Approval, Audit) are maintained in separate repositories with independent governance.
'''

path = r'D:\OpenBase\GOVERNANCE.md'
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('GOVERNANCE.md created')
