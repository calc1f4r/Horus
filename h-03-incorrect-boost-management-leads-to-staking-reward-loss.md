---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55113
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Incorrect boost management leads to staking reward loss

### Overview


This report describes a bug in the `rewardCache::dropBoost` function (BGT 0x656b95E550C07a9ffe548bd4085c72418Ceb1dba). This function is supposed to drop boosted rewards for a validator, but it is not working correctly. The problem is that the function checks a storage called `dropBoostQueue` to make sure enough time has passed since the last boost. However, other functions like `Staker::_redeemRewards` and `Staker::setValidator` do not call the `rewardCache::queueDropBoost` function before using `dropBoost`. This means that the `dropBoostQueue` is always empty and the `dropBoost` function always returns `false`, preventing reward adjustments. To fix this bug, the logic in `Staker::_redeemRewards` and `Staker::setValidator` needs to be updated to make sure `rewardCache::queueDropBoost` is called before using `dropBoost`.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `rewardCache::dropBoost` function (BGT 0x656b95E550C07a9ffe548bd4085c72418Ceb1dba) is designed to drop boosted rewards for a given validator. However, it checks the `dropBoostQueue` storage to confirm whether sufficient time has passed since the last boost. The problem arises because `rewardCache::queueDropBoost` is never called prior to `dropBoost` in functions like `Staker::_redeemRewards` and `Staker::setValidator`. Consequently, the `dropBoostQueue` remains empty, and `dropBoost` always returns `false`, preventing reward adjustments.

1. The `queueDropBoost` function is used to queue a future drop of boosted tokens:

```solidity
    function queueDropBoost(bytes calldata pubkey, uint128 amount) external {
@>      QueuedDropBoost storage qdb = dropBoostQueue[msg.sender][pubkey];
        uint128 dropBalance = qdb.balance + amount;
        // check if the user has enough boosted balance to drop
        if (boosted[msg.sender][pubkey] < dropBalance) NotEnoughBoostedBalance.selector.revertWith();
@>      (qdb.balance, qdb.blockNumberLast) = (dropBalance, uint32(block.number));
        emit QueueDropBoost(msg.sender, pubkey, amount);
    }
```

2. The `dropBoost` function attempts to drop boosts but requires a valid `dropBoostQueue` entry:

```solidity
    function dropBoost(address user, bytes calldata pubkey) external returns (bool) {
@>      QueuedDropBoost storage qdb = dropBoostQueue[user][pubkey];
@>      (uint32 blockNumberLast, uint128 amount) = (qdb.blockNumberLast, qdb.balance);
        // `amount` must be greater than zero to avoid reverting as
        // `withdraw` will fail with zero amount.
@>      if (amount == 0 || !_checkEnoughTimePassed(blockNumberLast, dropBoostDelay)) return false;
..
```

3. `_redeemRewards` directly calls `dropBoost` without `queueDropBoost`:

```solidity
File: Staker.sol
305:             if (toFulfill > 0) {
306:                 rewardCache.dropBoost(validator, uint128(toFulfill));
307:             }
```

4. Similarly, `setValidator` calls `dropBoost` without using `queueDropBoost`:

```solidity
File: Staker.sol
80:         uint256 boosted = rewardCache.boosts(address(this));
81:         if (boosted > 0) {
82:             rewardCache.dropBoost(oldValidator, uint128(boosted));
83:         }
```

## Recommendations

Update the logic in `Staker::_redeemRewards` and `Staker::setValidator` to ensure that `rewardCache::queueDropBoost` is properly called before invoking `dropBoost`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

