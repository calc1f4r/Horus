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
solodit_id: 57355
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
finders_count: 2
finders:
  - x1485967
  - 3n0ch
---

## Vulnerability Title

Missing Debt Token Supply Sync Leads to Incorrect Interest Rate Calculations

### Overview


This bug report discusses an issue with the `LendingPool` contract, which is used for lending and borrowing assets. The problem is that the calculation for interest rates is incorrect, which can lead to incorrect rates being set for borrowers and depositors. This can also cause economic imbalances and potential loss of revenue for the protocol. The likelihood of this issue occurring is high and it is recommended to update the code to fix it.

### Original Finding Content

## Relevant Context

The `LendingPool` contract implements a lending protocol where users can deposit assets and borrow against them. The protocol tracks debt using a debt token, whose `totalSupply()` represents the total debt scaled by the current usage index.

The calculation flow for interest rates is:

1. `LendingPool.deposit()`
2. → `ReserveLibrary.deposit()`
3. → `ReserveLibrary.updateInterestRatesAndLiquidity()`
4. → `ReserveLibrary.calculateUtilizationRate()`

The utilization rate, calculated in the final step, is crucial for determining both borrow and lending rates.

## Finding Description

When a user calls `deposit()` in the `LendingPool`, the following sequence occurs:

1. `updateReserveState()` is called to update indices
2. The function then calls `ReserveLibrary.deposit()`, which in turn calls `updateInterestRatesAndLiquidity()`
3. Inside `updateInterestRatesAndLiquidity()`, `calculateUtilizationRate()` is called with the formula:

```solidity
utilizationRate = totalDebt / (totalLiquidity + totalDebt)
```

However, `reserve.totalUsage` (used as `totalDebt`) is not synchronized with the debt token's total supply after `updateReserveState()`. When the `usageIndex` increases over time due to interest accrual, the debt token's `totalSupply()` correctly reflects this increase as it's scaled by the usage index, but `reserve.totalUsage` remains outdated.

## Impact Explanation

High. The miscalculation of utilization rates leads to:

1. Incorrect borrow rates being set
2. Incorrect lending rates for depositors
3. Protocol-wide economic imbalances
4. Potential loss of protocol revenue

## Likelihood Explanation

High. This issue affects every operation that involves rate calculations and occurs whenever there is a time gap between operations where interest has accrued.

## Proof of Concept

Consider this scenario:

1. Initial state: `reserve.totalUsage = 100`, `usageIndex = 1.0 RAY`
2. Time passes, `usageIndex` increases to `1.2 RAY`
3. User calls `LendingPool.deposit()`:
   * `updateReserveState()` updates `usageIndex` to `1.2 RAY`
   * Debt token's `totalSupply()` correctly returns `120` (scaled by new index)
   * But `reserve.totalUsage` remains at `100`
   * Flow continues to `ReserveLibrary.deposit()` → `updateInterestRatesAndLiquidity()` → `calculateUtilizationRate()`
   * `calculateUtilizationRate()` uses `100/(totalLiquidity + 100)` instead of `120/(totalLiquidity + 120)`
4. Result: Incorrect utilization rate leads to wrong interest rate calculations

## Recommendation

Update the `totalUsage` after calling `updateReserveState()` in each of the core functions (`deposit()`, `withdraw()`):

```Solidity
function deposit(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
    // Update the reserve state
    ReserveLibrary.updateReserveState(reserve, rateData);
    
    // Update total usage to match debt token supply
    reserve.totalUsage = IERC20(reserve.reserveDebtTokenAddress).totalSupply();

    // Perform the deposit through ReserveLibrary
    uint256 mintedAmount = ReserveLibrary.deposit(reserve, rateData, amount, msg.sender);
    
    // ... rest of the function ...
}
```

Apply the same pattern to `withdraw()` function to ensure the total usage is always up to date with the actual debt token supply before any rate calculations are performed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | x1485967, 3n0ch |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

