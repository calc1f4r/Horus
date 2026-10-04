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
solodit_id: 31814
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

[M-01] Collateral token interest is accrued after relative price calculation in liquidations

### Overview


The `batchLiquidateBorrow()` function in the code calculates the amount of collateral tokens to seize by finding the relative exchange rate between the two assets. However, the code does not take into account the interest that has not been accrued yet. This can result in the liquidator being able to seize more collateral than they should be able to. To fix this issue, the code should include a call to `cTokenCollateral.accrueInterest()` before performing the calculations. This issue has been fixed in the code.

### Original Finding Content

When `batchLiquidateBorrow()` is called, we calculate the amount of collateral tokens to seize by taking the amount of liquidatable assets paid back and finding the relative exchange rate between the two. This logic is performed in `liquidateCalculateSeizeTokensNormed()`:
```solidity
function liquidateCalculateSeizeTokensNormed(address cTokenCollateral, uint normedRepayAmount) public view returns (uint) {
    uint priceCollateralMantissa = oracle.getUnderlyingPrice(CToken(cTokenCollateral));
    if (priceCollateralMantissa == 0) {
        revert PriceError();
    }

    uint exchangeRateMantissa = CToken(cTokenCollateral).exchangeRateStored(); // Note: reverts on error
    uint numerator = liquidationIncentiveMantissa * normedRepayAmount * expScale;
    uint denominator = priceCollateralMantissa * exchangeRateMantissa;

    uint seizeTokens = numerator / denominator;

    return seizeTokens;
}
```
This function sets the denominator to `priceCollateralMantissa * exchangeRateMantissa`, which is equivalent to the USD value of the underlying asset multiplied by the exchange rate from underlying asset to CToken. In other words, it represents the USD value of the CToken. This is used for the conversion.

However, the CToken has not had interest accrued at this point. That happens later, when `_seize()` is called.
```solidity
uint seizeTokens = liquidateCalculateSeizeTokensNormed(address(cTokenCollaterals[i]), liquidatedValueRemaining);
uint actualSeizeTokens;

uint borrowerBalance = cTokenCollaterals[i].balanceOf(borrower);
if (borrowerBalance < seizeTokens) {
    // can't seize more collateral than owned by the borrower
    actualSeizeTokens = borrowerBalance;
} else {
    actualSeizeTokens = seizeTokens;
}

actualSeizeTokens = cTokenCollaterals[i]._seize(msg.sender, borrower, actualSeizeTokens);
```
The result is that, if interest has not been accrued in a while, the exchange rate will be artificially low, and the liquidator will be able to seize more collateral than they should be able to.

This is limited by ensuring that the borrower's debt ratio has approved throughout the liquidation, so there is a limit to how much funds can be taken. However, for a market that has had a substantial time pass without accruing interest, the liquidator could get up to `1 / (1 - collateralFactor)` as a reward, instead of the 8% that is intended.

**Recommendation**

`liquidateCalculateSeizeTokensNormed()` should include a call to `cTokenCollateral.accrueInterest()` before calculations are performed to ensure they are accurate.

**Review**

Fixed via the fix to M-08 (which accrues interest before the debt ratio is calculated) in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

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

