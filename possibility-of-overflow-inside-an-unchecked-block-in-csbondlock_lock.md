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
solodit_id: 41238
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#16-possibility-of-overflow-inside-an-unchecked-block-in-csbondlock_lock
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

Possibility of overflow inside an unchecked block in `CSBondLock._lock()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
If [`CSModule.reportELRewardsStealingPenalty()`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1014) is called by mistake with `amount` parameter close to `type(uint256).max` and the node operator already has locked bond, an overflow inside an unchecked block in `CSBondLock._lock()` may happen. So stored node operator's lock becomes less than it should be.

##### Recommendation
We recommend moving 
```
if ($.bondLock[nodeOperatorId].retentionUntil > block.timestamp) {
    amount += $.bondLock[nodeOperatorId].amount;
}
```
outside of the unchecked block.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#16-possibility-of-overflow-inside-an-unchecked-block-in-csbondlock_lock
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

