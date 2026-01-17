---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28159
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#6-naming-variable-mistake
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Naming variable mistake

### Overview

See description below for full details.

### Original Finding Content

##### Description
Because of `_totalRewardShares` not divides for validators but divides for `effectiveStakeTotal` should to rename `perValidatorReward` to `perStakeReward` at `NodeOperatorsRegistry.sol` at line:
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L441
##### Recommendation
It is recommended to rename `perValidatorReward` to `perStakeReward`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#6-naming-variable-mistake
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

