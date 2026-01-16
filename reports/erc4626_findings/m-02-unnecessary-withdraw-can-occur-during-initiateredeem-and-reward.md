---
# Core Classification
protocol: Level_2025-04-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63739
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Unnecessary withdraw can occur during `initiateRedeem` and `reward`

### Overview


The bug report states that when users use `initiateRedeem`, the operation always tries to withdraw collateral from the default strategies without first checking if there is enough collateral in the boring vault. This can result in unnecessary withdrawals from strategies, leading to suboptimal yield and asset management. The same issue occurs when `RewardsManager.reward` is called. The recommendation is to only trigger `vaultManager.withdrawDefault` when there is not enough collateral in the vault to cover the redemption and reward request.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When users trigger `initiateRedeem`, the operation always attempts to withdraw collateral from the default strategies without first checking whether the current collateral balance in the boring vault is sufficient to cover the redemption request.

```solidity
    function initiateRedeem(address asset, uint256 lvlUsdAmount, uint256 expectedAmount)
        external
        requiresAuth
        notPaused
        returns (uint256, uint256)
    {
        if (!redeemableAssets[asset]) revert UnsupportedAsset();
        if (!isBaseCollateral[asset]) revert RedemptionAssetMustBeBaseCollateral();
        if (lvlUsdAmount == 0) revert InvalidAmount();

        uint256 collateralAmount = computeRedeem(asset, lvlUsdAmount);
        if (collateralAmount < expectedAmount) revert MinimumCollateralAmountNotMet();

        pendingRedemption[msg.sender][asset] += collateralAmount;
        userCooldown[msg.sender][asset] = block.timestamp;

        // note preventing amounts that would fail by definition at complete redeem due to max per block
        if (pendingRedemption[msg.sender][asset] > maxRedeemPerBlock) revert ExceedsMaxBlockLimit();

        lvlusd.burnFrom(msg.sender, lvlUsdAmount);

        // Don't block redemptions if withdraw default fails
>>>     try vaultManager.withdrawDefault(asset, collateralAmount) {
            emit WithdrawDefaultSucceeded(msg.sender, asset, collateralAmount);
        } catch {
            emit WithdrawDefaultFailed(msg.sender, asset, collateralAmount);
        }

        vaultManager.vault().exit(
            address(silo), ERC20(asset), collateralAmount, address(vaultManager.vault()), lvlUsdAmount
        );

        emit RedeemInitiated(msg.sender, asset, collateralAmount, lvlUsdAmount);

        return (lvlUsdAmount, collateralAmount);
    }
```

This could lead to unnecessary withdrawals from strategies, even when there is enough collateral in the vault to cover the redemption request. This results in suboptimal yield and asset management.

The same case also applies when `RewardsManager.reward` is called.

## Recommendations

Only trigger `vaultManager.withdrawDefault` when the collateral balance in the vault is insufficient to cover the redemption and `reward` request.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Level_2025-04-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

