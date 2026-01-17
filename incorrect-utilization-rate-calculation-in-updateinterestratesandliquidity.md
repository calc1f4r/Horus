---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57281
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 7
finders:
  - agbanusijohn
  - eta
  - pabloperezacc6
  - aravn
  - ace_30
---

## Vulnerability Title

Incorrect Utilization Rate Calculation in `updateInterestRatesAndLiquidity`

### Overview


The function `updateInterestRatesAndLiquidity` in `ReserveLibrary` is not calculating the utilization rate correctly. This means that the interest rates for borrowers and lenders may be inaccurate, potentially causing them to lose money. This happens because the function is using old values instead of updated ones. The issue can be fixed by changing a few lines of code.

### Original Finding Content

## Summary

The function `updateInterestRatesAndLiquidity` in `ReserveLibrary` is called after each transaction in `LendingPool`. However, it incorrectly calculates the utilization rate using **old values** instead of the newly calculated ones. This leads to inaccurate interest rate calculations, potentially causing fund loss for some users.

## Vulnerability Details

The function calculates `computedDebt` and `computedLiquidity` based on current indexes but when calculating the utilization rate, it still relies on the old values instead of using the newly computed ones:

```Solidity
function updateInterestRatesAndLiquidity(ReserveData storage reserve,ReserveRateData storage rateData,uint256 liquidityAdded,uint256 liquidityTaken) internal {
         -- snip --

        uint256 computedDebt = getNormalizedDebt(reserve, rateData);
        uint256 computedLiquidity = getNormalizedIncome(reserve, rateData);

        // Calculate utilization rate
        uint256 utilizationRate = calculateUtilizationRate(reserve.totalLiquidity, reserve.totalUsage);
```

## Impact

When no new liquidity or debt is added or removed, `reserve.totalLiquidity` and `reserve.totalUsage` remain unchanged, while the actual debt and liquidity amounts increase due to **interest rate** accrual.  Over time this discrepancy grows larger, causing the next user to receive a highly inaccurate utilization rate. As a result, the borrowing and liquidity rates will be significantly miscalculated.\
Borrowers and lenders will experience inaccurate interest rates.

## Tools Used

vscode

## Recommendations

```diff
        uint256 computedDebt = getNormalizedDebt(reserve, rateData);
        uint256 computedLiquidity = getNormalizedIncome(reserve, rateData);

        // Calculate utilization rate
-       uint256 utilizationRate = calculateUtilizationRate(reserve.totalLiquidity, reserve.totalUsage);
+       uint256 utilizationRate = calculateUtilizationRate(computedLiquidity, computedDebt);

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | agbanusijohn, eta, pabloperezacc6, aravn, ace_30, petersr, 0xisboss |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

