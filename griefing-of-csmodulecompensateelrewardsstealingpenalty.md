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
solodit_id: 41220
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#8-griefing-of-csmodulecompensateelrewardsstealingpenalty
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

Griefing of `CSModule.compensateELRewardsStealingPenalty()`

### Overview


The bug report describes a problem with a function called `CSModule.compensateELRewardsStealingPenalty()`. This function is currently allowed to be used by anyone, but it is required to only compensate a certain amount. This means that someone could take advantage of this by causing the function to fail and potentially causing issues for the Node Operator manager. The recommendation is to make this function only accessible to the Node Operator manager to prevent potential issues.

### Original Finding Content

##### Description

`CSModule.compensateELRewardsStealingPenalty()` [function is permissionless](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1096-L1108). At the same time [it's required](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondLock.sol#L126-L128) to compensate no more than what was locked. A griefer may frontrun a `CSModule.compensateELRewardsStealingPenalty()` call and compensate 1 locked share, causing the initial call to revert. The griefer can do this multiple times, putting the Node Operator manager at risk of having to settle their lock with a reset of the bond curve.

##### Recommendation
We recommend making the `CSModule.compensateELRewardsStealingPenalty()` function permissioned so that only the Node Operator manager can call it.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#8-griefing-of-csmodulecompensateelrewardsstealingpenalty
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

