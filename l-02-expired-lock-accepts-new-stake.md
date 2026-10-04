---
# Core Classification
protocol: BOB-Staking_2025-10-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63725
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-02] Expired lock accepts new stake

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

`BobStaking::stake` lets anyone add stake to a position whose `unlockTimestamp` has already passed because the function only blocks deposits when `unbondEndTimes[receiver] != 0`. This means matured positions can be topped up and then unbonded immediately, bypassing the intended lock period for the fresh deposit. I recommend reinitialising the lock when a user adds stake to an expired position (e.g., `set unlockTimestamp = max(currentUnlock, block.timestamp + lockPeriod)`) or disallowing top-ups altogether until the user restakes from scratch.

```solidity
// From BobStaking::stake
        if (stakers[receiver].amountStaked > 0) {
            _updateUnclaimedRewardsForStaker(receiver);
        } else {
            stakers[receiver].timeOfLastUpdate = uint80(block.timestamp);
            stakers[receiver].conditionIdOflastUpdate = nextConditionId - 1;
            stakers[receiver].lockPeriod = lockPeriod;
            stakers[receiver].unlockTimestamp = uint80(block.timestamp) + lockPeriod;
        }
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BOB-Staking_2025-10-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

