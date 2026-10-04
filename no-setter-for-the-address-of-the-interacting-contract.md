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
solodit_id: 28337
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#1-no-setter-for-the-address-of-the-interacting-contract
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

No setter for the address of the interacting contract

### Overview

See description below for full details.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/1inch-rewards-manager/blob/c2cd9665666deda9452fa9e3461fbf3537413945/contracts/RewardsManager.vy#L39 the `rewards_contract` variable is described.
This is the address of the `FarmingRewards` contract. Now there is no way to change its address. If new functionality is added to this contract, it will be necessary to reinstall the `RewardsManager` contract.

##### Recommendation
It is recommended to add a method to change the value of the variable `rewards_contract`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#1-no-setter-for-the-address-of-the-interacting-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

