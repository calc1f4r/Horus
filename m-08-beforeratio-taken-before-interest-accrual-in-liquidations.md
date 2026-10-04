---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31821
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[M-08] `beforeRatio` taken before interest accrual in liquidations

### Overview


The `batchLiquidateBorrow()` function has a bug that can cause it to allow too much collateral to be seized, harming the borrower's debt position. This happens because interest is accrued after the first check is done, but before the second check. This can also lead to additional rewards for the liquidator. To fix this, the recommendation is to explicitly call `accrueInterest()` on all relevant tokens when `batchLiquidateBorrow()` is called. This has been fixed in a recent commit.

### Original Finding Content

In `batchLiquidateBorrow()`, the fundamental check on the liquidation is that the account debt ratio after is less than or equal to what it was before.

```solidity
if ((err != uint(Error.NO_ERROR) && err != uint(Error.TOO_LITTLE_INTEREST_RESERVE)) || afterRatio > beforeRatio) {
    revert LiquidateSeizeTooMuch();
}
```
Along the pathway to liquidation, all relevant markets have their interest accrued (either in the `_liquidateBorrow()` function or the `_seize()` function), which increases the value of both the debt and collateral tokens.

These accruals happen after the `beforeRatio` is taken, but before the `afterRatio` is taken. Therefore, the values of the tokens will be shifted between these two checks.

This can lead to a situation where the liquidation takes too much collateral that it actually harms the debt position of the borrower, but is allowed to proceed.

For example, imagine a situation where a borrower has 5 cTokens of collateral worth $1 each (not accrued) and 1 cTokens of debt worth $4.50 (fully accrued). This leads to a `beforeRatio` of `4.5 / (5 * 0.85) = 1.058e18`. If there are interest accruals due that will move the value of the collateral tokens up 25%, and the borrower seizes 1 cToken (unpaid), the resulting `afterRatio = 4.5 / ((5 - 1) * 1.25 * 0.85) = 1.058e18`.

Clearly taking a collateral token without paying any debt off is not good for the borrower, but it will be allowed to pass by this check before the interest accrual mismatch.

Note that in some edge cases, this could also cause the problem of allowing a non-liquidatable position to be liquidated, but this is less likely because it presumes that the position was previously in a liquidatable state but wasn't liquidated.

**Note on Exploitability**

Because of the logic used to calculate the amount of tokens seized, there is no way for a liquidator to directly choose to seize tokens without paying any debt off. However, this can be combined with issues like [M-01] and [M-04] to lead to additional rewards beyond the `1 / (1 - collateralFactor)` that the liquidator can earn.

**Recommendation**

Explicitly call `accrueInterest()` on all liquidatable and collateral tokens when `batchLiquidateBorrow()` is called.

If this is done, it negates the need for the fix suggested for [M-01].

**Review**

Fixed as recommended in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

