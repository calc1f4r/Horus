---
# Core Classification
protocol: Elytra_2025-07-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63578
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
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

[M-03] Elytra share price may be inflatten to block the system

### Overview


This bug report discusses an issue with the Elytra platform where the total value of assets is calculated using a formula. Users are able to withdraw their assets, but there is a problem where if they donate assets into the pool, they can still withdraw even if there is not enough balance in the pool. This can impact the share's price and may cause issues for investors. The report recommends that if the total value of assets is not enough to cover the withdrawal, it should be reverted.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description
In Elytra, total asset tvl is calculated based on the formula: `totalAssetDepositsTracked + unstakingVault + strategyBalance - reserveBalance`.

Users can choose withdrawAssets or requestWithdrawal to withdraw their assets. When we withdraw assets, we will check whether we have enough balance in ElyTra pool, and we will update the variable `totalAssetDepositsTracked`.

In a normal scenario, the pool's balanceOf should equal `totalAssetDepositsTracked` when we deposit/withdraw/transferUnstaking, we will update `totalAssetDepositsTracked` timely.

The problem here is that if users donate some assets into the pool, users can withdraw assets when there is not enough balance in the pool. This case can still work, and we will update the variable `totalAssetDepositsTracked` to `0`. However, this will impact share's price.

For example:
1. Alice, as the first depositor, deposits 1000 HYPE.
2. Admin allocates 1000 HYPE into the related strategy. Now `totalAssetDepositsTracked` is 0.
3. Alice donates 999 HYPE into the pool, and withdraws 999 shares. `totalAssetDepositsTracked` will keep `0`, and total share's amount will be decreased to 1. This will increase share's price.
4. If we set the `pricePercentageLimit`, users may fail to deposit/withdraw because of this price limit check.
Another impact here is that when we increase share's price a lot, the actual asset for each rounding down/up will become larger. This will have some bad experiences for investors.

```solidity
    function withdrawAsset(
        address asset,
        uint256 elyAssetAmount,
        address receiver,
        uint256 minUnderlyingAssetExpected
    )
    {
        uint256 poolBalance = IERC20(asset).balanceOf(address(this));
        if (poolBalance < assetAmountBeforeFee) {
            revert InsufficientPoolBalance(assetAmountBeforeFee, poolBalance);
        }
        ...
@>        if (assetAmountBeforeFee <= totalAssetDepositsTracked[asset]) {
            totalAssetDepositsTracked[asset] -= assetAmountBeforeFee;
        } else {
@>            totalAssetDepositsTracked[asset] = 0;
        }
    }
```

## Recommendations
If the `totalAssetDepositsTracked` is not enough to pay the withdrawal assets, we should revert.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

