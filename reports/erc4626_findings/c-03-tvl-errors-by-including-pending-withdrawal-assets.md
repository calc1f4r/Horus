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
solodit_id: 63543
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

[C-03] TVL errors by including pending withdrawal assets

### Overview


The bug report discusses an issue with the `getTotalAssetTVL()` function that incorrectly includes assets from pending withdrawal requests in its calculation. This leads to an inflated `elyAsset` price, which can be exploited by users to withdraw at an unfairly high rate. The root cause of this issue is that when a user initiates a withdrawal, their `elyAssets` are immediately burned, but the corresponding assets are not removed from the TVL calculation. This creates a mismatch between supply and TVL, causing the price to spike artificially. The report suggests two possible solutions: adjusting the TVL calculation to subtract assets from pending withdrawals, or delaying the burning of `elyAssets` until the withdrawal is completed. Both approaches aim to prevent price manipulation and ensure consistent accounting of assets and supply. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** High

## Description

The `getTotalAssetTVL()` function incorrectly includes assets that are backing **pending withdrawal requests** in its TVL calculation. This results in an inflated `elyAsset` price, leading to exploitable pricing errors.

**Root Issue**

When a user initiates a withdrawal via `requestWithdrawal()`, their `elyAssets` are **burned immediately**, reducing total supply. However, the corresponding assets are moved to the **unstaking vault**, and are **not removed from TVL calculations**. These assets remain counted until the user completes the withdrawal.

Since price is computed as:

```
price = totalTVL / totalSupply
```

This introduces a mismatch:

* Supply goes down (due to burned `elyAssets`).
* TVL remains the same (due to unadjusted asset accounting).

This causes the `elyAsset` price to **spike artificially**, allowing users to exploit the system by:

* Burning tokens.
* Inflating price.
* Withdrawing at an unfairly high rate.

**Technical Details**

In `ElytraDepositPoolV1`, TVL is calculated as:

```solidity
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

The problem is that `unstakingVaultBalance` is retrieved via:

```solidity
function _getUnstakingVaultBalance(address asset) internal view returns (uint256 balance) {
    address unstakingVault = elytraConfig.getContract(ElytraConstants.ELYTRA_UNSTAKING_VAULT);
    if (unstakingVault == address(0)) {
        return 0;
    }

    try IElytraUnstakingVault(unstakingVault).getClaimableAssets(asset) returns (uint256 claimableAmount) {
        return claimableAmount;
    } catch {
        return 0;
    }
}
```

This value includes assets allocated to pending withdrawal requests — even though the corresponding shares have already been burned.

**Exploitation Example**

Consider the following:

1. Initial state:

* 15e18 HYPE in pool.
* 10e18 elyHYPE total supply.
* Price = 1.5 HYPE.

2. User A requests withdrawal of 6e18 elyHYPE, backed by 9e18 HYPE.

* `elyAssets` are burned.
* 9e18 HYPE moved to unstaking vault.
* TVL remains 15e18.
* New supply = 4e18.
* New price = 3.75 HYPE (inflated).

3. User B updates price, then withdraws 4e18 elyHYPE and receives **15e18 HYPE**, extracting unearned value.

This behavior can be repeated by multiple users to drain excess value.

## Recommendations

There are two main approaches to resolving this issue:

**Option A: Adjust TVL Calculation**

Track pending withdrawals explicitly and subtract their asset backing from the result of `getTotalAssetTVL()`. This ensures the price accurately reflects only the assets backing active elyAssets.

**Option B: Delay Token Burn**

Defer burning of `elyAssets` until the withdrawal is actually completed (i.e., when the user calls `completeWithdrawal()`), so that TVL and supply remain aligned throughout the withdrawal lifecycle.

Both approaches aim to ensure consistent accounting of assets vs. supply to prevent price manipulation.





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

