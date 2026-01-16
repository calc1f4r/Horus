---
# Core Classification
protocol: Yieldoor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55042
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/791
source_link: none
github_link: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/96

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x73696d616f
---

## Vulnerability Title

M-4: `Strategy::checkPoolActivity()` incorrect check leads to vulnerable price

### Overview


This bug report is about an incorrect check in the `Strategy::checkPoolActivity()` function which can lead to a vulnerable price. The issue was found by a user named `0x73696d616f` and can be seen on the source link provided. The function currently reverts if the timestamp is 0, but this never happens. Instead, the timestamp is set to 1 when the cardinality is increased for gas saving purposes. This can result in an invalid price observation and potential loss of funds for users. The root cause is an incorrect timestamp check in `Strategy:322`. There are no internal or external pre-conditions for this bug. The attack path involves an attacker or user adding cardinality to the pool, causing a rebalance with an invalid price. The impact is a loss of funds due to depositing liquidity at an unfavorable price. A proof of concept is provided in the report. To mitigate this issue, the `if` statement in line 322 should be updated to `if (timestamp == 1) { revert("timestamp 1"); }`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/96 

## Found by 
0x73696d616f

### Summary

`Strategy::checkPoolActivity()` [reverts](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Strategy.sol#L322-L324) if the timestamp is 0. However, this will never happen. What actually happens is the timestamp being 1, when the cardinality has been increased and the tick timestamp was [set](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/Oracle.sol#L118) to 1 for gas saving purposes.

When this tick is hit in the loop, it means there were not enough observations to reach the `lookAgo` timestamp and it should revert because the price could not be validated. However, if the timestamp is 1, it may not revert depending on the value of the tick delta calculated, and as the timestamp is 1, it will [return true](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Strategy.sol#L335-L337) with an invalid price observation.

### Root Cause

In `Strategy:322`, the [timestamp check](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Strategy.sol#L322-L324) is incorrect.

### Internal Pre-conditions

None.

### External Pre-conditions

None.

### Attack Path

1. Twap would not have enough credibility and rebalancing would be impossible.
2. Attacker or user adds cardinality to the uniswap pool, which sets the next ticks timestamp to 1.
3. Rebalance goes through with an invalid price with not enough validation, leading to depositing liquidity at a bad price and causing losses for users.

### Impact

Loss of funds due to depositing liquidity at an unfavourable price.

### PoC

The following function is used when cardinality is increased in the pool.
```solidity
    function grow(
        Observation[65535] storage self,
        uint16 current,
        uint16 next
    ) internal returns (uint16) {
        require(current > 0, 'I');
        // no-op if the passed next value isn't greater than the current next value
        if (next <= current) return current;
        // store in each slot to prevent fresh SSTOREs in swaps
        // this data will not be used because the initialized boolean is still false
        for (uint16 i = current; i < next; i++) self[i].blockTimestamp = 1;
        return next;
    }
```

### Mitigation

```solidity
            if (timestamp == 1) {
                revert("timestamp 1");
            }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Yieldoor |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/96
- **Contest**: https://app.sherlock.xyz/audits/contests/791

### Keywords for Search

`vulnerability`

