---
# Core Classification
protocol: Elytra_2025-07-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63547
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
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

[H-04] Strategy allocation tracking errors affect TVL calculations

### Overview


The Elytra protocol has a bug that affects how it tracks the amount of assets it owns. This can lead to incorrect calculations of the total value of assets and the price of its token, called `elyAsset`. This bug can also create opportunities for malicious users to profit and potentially cause the protocol to become insolvent. The bug is caused by a tracking mechanism that does not account for changes in the value of assets due to yield growth, realized profits or losses, and slashing events. This can result in a mismatch between the reported total value of assets and the actual amount held by the protocol. To fix this bug, several recommendations have been made, including implementing a dynamic on-chain view to track asset value, accurately accounting for profits and losses during deallocation, and introducing a mechanism to manually adjust for slashing losses.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The Elytra protocol tracks strategy allocations using a static variable `assetsAllocatedToStrategies[asset]`, which is manually updated during asset allocation and deallocation. However, this tracking mechanism fails to account for:

1. **Real-time yield growth inside strategies**.
2. **Realized profits or losses during deallocation**.
3. **Slashing events incurred by restaking operations**.

As a result, the `getTotalAssetTVL()` function under- or overstates actual holdings in strategies, leading to:

* Mispriced `elyAsset` tokens.
* Front-running opportunities for malicious users.
* Inability to reflect slashing-related losses.
* Potential insolvency if users withdraw more than the protocol truly owns.

**Mechanism Breakdown**

TVL is calculated as:

```solidity
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

The issue lies in `strategyAllocated`, which is derived from:

```solidity
// Called during allocation
assetsAllocatedToStrategies[asset] += amount;

// Called during deallocation
uint256 withdrawn = IElytraStrategy(strategy).withdraw(asset, amount);
if (withdrawn <= assetsAllocatedToStrategies[asset]) {
    assetsAllocatedToStrategies[asset] -= withdrawn;
} else {
    assetsAllocatedToStrategies[asset] = 0;
}
```

This creates three critical problems:

**Yield is Ignored During Allocation Lifecycle**

When a strategy generates yield, the actual balance increases (e.g., 10 → 12 tokens), but `assetsAllocatedToStrategies` remains fixed at the original 10. This underreports TVL and keeps the `elyAsset` price **deflated**.

**Attack Scenario:**

* User observes that strategy yield has accrued unaccounted value.
* They deposit elyAssets at a low price.
* Admin deallocates funds (suddenly realizing yield), causing TVL and price to spike.
* Attacker immediately withdraws and captures profit that wasn’t rightfully theirs.

**Incorrect Profit/Loss Handling on Deallocation**

The `deallocateFromStrategy()` function assumes that the amount withdrawn is equivalent to the portion being deallocated. However, if the strategy has changed in value:

* **If there was a profit:** remaining allocation is overstated.
* **If there was a loss:** allocation is understated or even **permanently inflated**, since the shortfall cannot be recorded.

This causes the TVL to drift from actual holdings over time.

**Example:**

* Allocate 100 USDC to a strategy → TVL tracks 100
* Strategy grows to 120 USDC
* Withdraw 60 → Allocation becomes 40, but 60 remains in strategy
  → TVL = 40 + 60 unstated = 100 (incorrect; should be 60)

**Slashing Losses Are Not Reflected**

In a restaking scenario (e.g. EigenLayer), funds allocated to validators can be slashed due to misbehavior. However, the current model has no mechanism to **reduce** `assetsAllocatedToStrategies` without actually withdrawing assets — which may no longer exist post-slash.

Thus, even if a validator loses funds, the protocol keeps reporting a higher TVL and inflated `elyAsset` price.

## Recommendations

Several complementary improvements are recommended:

**Option A: Real-Time Balance Checks**

Replace or supplement `assetsAllocatedToStrategies` with a **dynamic on-chain view**, such as:

```solidity
IElytraStrategy(strategy).balanceOf(asset)
```

This ensures that `getTotalAssetTVL()` reflects the actual value of assets held, including yield and losses.

**Option B: Accurate Profit/Loss Accounting on Deallocation**

Track the originally allocated strategy shares or value, and compare it against the actual withdrawal result to update allocations correctly.

You could implement:

* `strategyReportedValue()` function for yield-aware accounting.
* `syncStrategyAllocations()` to periodically reconcile the difference.

**Option C: Manual Slashing Adjustments**

Introduce a mechanism to manually **reduce** `assetsAllocatedToStrategies[asset]` in the event of slashing. For example:

```solidity
function reportStrategyLoss(address asset, uint256 amount) external onlyAdmin {
    require(assetsAllocatedToStrategies[asset] >= amount, "Exceeds tracked allocation");
    assetsAllocatedToStrategies[asset] -= amount;
}
```






### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

