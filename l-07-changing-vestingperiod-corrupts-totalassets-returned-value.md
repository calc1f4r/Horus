---
# Core Classification
protocol: Falcon_2025-02-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49903
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Falcon-security-review_2025-02-17.md
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

[L-07] Changing `vestingPeriod` corrupts `totalAssets` returned value

### Overview

See description below for full details.

### Original Finding Content

The `StakedUSDf.sol` contract is a ERC4626 vault for staking USDf to accrue yield, with linear vesting for reward deposits.
the `StakingRewardsDistributor.sol` will trigger `transferInRewards()` function in `StakedUSDf.sol` to transfer the reward and update the vesting amount.

In case the admin calls `setVestingPeriod()` function to update the duration of the vesting period and the `getUnvestedAmount()` still returns a non-zero value. it will corrupt the current reward vesting or it can lead to loss/profit to the current stackers because the `totalAssets()` function uses the returned value from `getUnvestedAmount()` which will be directly affected by any update to `vestingPeriod`.

It also could lead to blocking multiple functions in `StakedUSDf.sol` contract e.g. deposit, mint, withdraw, redeem... these functions will revert with panic **arithmetic underflow or overflow**.

Recommendations:

You can revert in case `getUnvestedAmount() > 0`

```diff
    function _setVestingPeriod(uint32 newPeriod) internal {
        uint32 oldVestingPeriod = vestingPeriod;
        require(newPeriod <= MAX_VESTING_PERIOD, DurationExceedsMax());
        require(oldVestingPeriod != newPeriod, DurationNotChanged());
        require(newPeriod > 0 || cooldownDuration > 0, ExpectedCooldownOn());
+       require(getUnvestedAmount() == 0, ExpectedCooldownOn());
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Falcon_2025-02-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Falcon-security-review_2025-02-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

