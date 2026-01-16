---
# Core Classification
protocol: Propchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35330
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Propchain.md
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
  - Zokyo
---

## Vulnerability Title

Incorrect Loop Condition.

### Overview


This report describes a critical bug in the PROPCStakingV2.sol contract that has now been resolved. The bug affects the redeem() function, which is used for claiming rewards. The bug prevents users from claiming rewards for their first staking position (stake ID 0). This is because the loop in the function does not account for stake ID 0 due to a condition that prevents the loop from reaching it. The same issue also affects the _userPoolMetrics() function, which can result in underflow and prevent users from leaving the pool or making emergency withdrawals. The recommendation is to adjust the loop to include stake ID 0 by changing the loop condition. This has now been done in the updated contract. 

### Original Finding Content

**Severity**: Critical

**Status**: Resolved

**description**

1. PROPCStakingV2.sol: redeem().

The function contains a critical flaw in its loop construct that results in the function not accounting for the very first staking position (stake ID 0) when calculating the rewards for redemption. As a result, users cannot claim rewards for their initial stake. The issue arises from the loop's condition that prevents the iteration from reaching the index 0:
```solidity
for(uint256 stakeId = _stakes.length; stakeId > 0; stakeId--) {
Stake storage_stake = _stakes[stakeId];
}
```
Since the condition checks 'stakeId > 0, and stake IDs are zero-indexed, the first element (stakeId = 0) is never processed, resulting in rewards associated with the first stake never being claimed.

2. PROPCStakingV2.sol: _userPoolMetrics()
   
The function contains a critical flaw in its for-loop condition. In case when `stakeld` becomes zero, the index in `array_stakes` will be less than zero, so there will be underflow in the loop. As a result, users cannot leave the pool or make emergency withdrawals.

**Recommendation:**

Adjust the loop to iterate over all stakes by changing the loop condition to allow stakeId to reach 0.

**Post audit.**

Loop iterates over the stake with index 0 now.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Propchain |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Propchain.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

