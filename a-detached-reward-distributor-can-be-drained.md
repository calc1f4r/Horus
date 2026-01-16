---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34257
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#2-a-detached-reward-distributor-can-be-drained
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

A detached reward distributor can be drained

### Overview


This bug report discusses an issue with the reward distribution logic in the dForce LendingContracts. If an admin changes the reward distribution logic using the `_setRewardDistributor()` function, the previous version is supposed to distribute rewards for the previous period. However, after detaching the reward distribution contract from the controller, transfers are no longer tracked by the controller. This allows an attacker to drain rewards from the old distributor by using cycles charge balance and then claiming from different accounts or through a flashloan attack. The report recommends two solutions: either allow tracking transfers by multiple distributors at the same time or do not change the distributor address and use migration.

### Original Finding Content

##### Description
If admin decided to change the current reward distribution logic and set new one by using the [`_setRewardDistributor()`](https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/Controller.sol#L548) function,
 the prev version is supposed to distribute rewards for the prev period. 
After detaching the reward distribution contract from the controller, transfers don't track by the controller any more and by abusing this issue an attacker can drain rewards from the old distributor by using cycles charge balance then claim from different accounts or a flashloan attack.

##### Recommendation
We recommend following one of the two ways:
- allow tracking transfers by a few distributors at the same time,
- don't change the distributor address and use migration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#2-a-detached-reward-distributor-can-be-drained
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

