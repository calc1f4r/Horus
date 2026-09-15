---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35161
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Erroneous Condition in _setAssetSource

### Overview


There is a bug in the Pyth feed feature of the Radiant Capital platform. When the owner sets the parameters for a feed using Pyth, there is a check that is being done over the feedId and feedAddress. However, due to the use of an '&&' operator, if the feedAddress is set to zero, the feedId will also be set to zero and the call will not revert. This means that there are no Pyth price fees for a feedId of 0, which is incorrect. The bug needs to be fixed by correcting the check to disallow the feedId from being set to 0. This bug has been resolved in a recent pull request by the Radiant team.

### Original Finding Content

When the owner sets the parameters for a feed using Pyth, there is a [check](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L190) being done over the `feedId` and `feedAddress`. However, because they are using an `&&`, if the `feedAddress` is zero, then the `feedId` would be zero as well and the call WILL NOT revert as there are no Pyth price fees for a `feedId` of 0\.


Consider correcting this check to be meaningful and disallow the `feedId` from being 0\.


***Update:** Resolved in [pull request \#80](https://github.com/radiant-capital/riz/pull/80) at commit [cf84c06](https://github.com/radiant-capital/riz/pull/80/commits/cf84c0660912aa154af31e96c0aa07773f4c9575). The Radiant team stated:*



> *Removed the check for CL feed address when we set Pyth in the Router.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

