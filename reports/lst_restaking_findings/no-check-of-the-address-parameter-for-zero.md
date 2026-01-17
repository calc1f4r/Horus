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
solodit_id: 28335
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#1-no-check-of-the-address-parameter-for-zero
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
  - MixBytes
---

## Vulnerability Title

No check of the address parameter for zero

### Overview


This bug report is about a problem with the `RewardsManager.vy` contract in the `1inch-rewards-manager` repository on GitHub. At line 66 of the contract, the `owner` variable is assigned the value of the `_to` parameter. However, if the value of the parameter is zero, then the `set_rewards_period_duration()` and `recover_erc20()` functions will be blocked. To fix this issue, it is recommended to add a check for the variable `_to` for zero before line 66.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/1inch-rewards-manager/blob/c2cd9665666deda9452fa9e3461fbf3537413945/contracts/RewardsManager.vy#L66, the `owner` variable is assigned the value of the `_to` parameter. 
But, if by chance the value of the parameter turns out to be equal to zero, then the work of the following functions will be blocked:
`set_rewards_period_duration()`, `recover_erc20()`.

##### Recommendation
It is recommended to add a check for the variable `_to` for zero before line 66.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#1-no-check-of-the-address-parameter-for-zero
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

