---
# Core Classification
protocol: Celo Contracts Audit – Release 4
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10862
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/celo-audit-release-4/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Incorrect use of require in revokeVotes

### Overview


The `revokeVotes` function of the `Governance` contract is intended to revoke votes on proposals in the Referendum stage. However, it currently requires all dequeued proposals to be in the Referendum stage, which is not necessary during normal operations. If any element of dequeued is not within the Referendum stage, the `revokeVotes` function will revert. This makes the function unusable.

To fix this issue, the following operations should be performed if the proposal is within the Referendum stage. Otherwise, the iteration of the loop should be treated as a no-op. This issue has now been fixed in commits a10bdf3 and 750341b.

### Original Finding Content

The [`revokeVotes` function](https://github.com/celo-org/celo-monorepo/blob/f64b4c5b5228ecbf41e3e7cfdbb8c0e9a983eea2/packages/protocol/contracts/governance/Governance.sol#L672) of the `Governance` contract is intended to revoke votes on proposals in the Referendum stage. However, it actually [`requires` all `dequeued` proposals to be in that stage](https://github.com/celo-org/celo-monorepo/blob/f64b4c5b5228ecbf41e3e7cfdbb8c0e9a983eea2/packages/protocol/contracts/governance/Governance.sol#L683), which is not necessary during normal operations. Whenever any element of `dequeued` is not within the `Referendum` stage, the `revokeVotes` function will revert. This effectively makes the `revokeVotes` function unusable.


Instead of reverting, consider performing [the following operations](https://github.com/celo-org/celo-monorepo/blob/f64b4c5b5228ecbf41e3e7cfdbb8c0e9a983eea2/packages/protocol/contracts/governance/Governance.sol#L684-L688) if the proposal is within the `Referendum` stage. Otherwise, that iteration of the loop should be treated as a no-op.


**Update:** *Fixed in commits [a10bdf3](https://github.com/celo-org/celo-monorepo/commit/a10bdf3e42ecb0667cbe98d287bac02c1da85e93) and [750341b](https://github.com/celo-org/celo-monorepo/commit/750341b6c62a0d8f2641fcbe841d03ed3c7d7ff2).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Celo Contracts Audit – Release 4 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/celo-audit-release-4/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

