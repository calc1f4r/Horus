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
solodit_id: 57344
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
  - kobbyeugene
  - zgczgc
---

## Vulnerability Title

Late Reserve Index Update Causes Stale Interest Accrual

### Overview


The report discusses a bug in the updateReserveInterests function that causes the reserve indices to be updated too late, resulting in inaccurate interest calculations. This can lead to economic discrepancies and impact the stability of the protocol. The bug can be fixed by calling the function before any state changes occur.

### Original Finding Content

## Summary

The reserve indices are updated too late (after liquidity or debt changes occur) resulting in stale interest accrual. This mis-sequencing leads to inaccurate interest rate computations and may distort economic incentives.

## Vulnerability Details

The `updateReserveInterests` function is intended to be called *before* any state-changing operations to capture the current interest accrual accurately. However, in the `updateInterestRatesAndLiquidity` function, it is invoked at the end—after liquidity or debt updates have already occurred.

* **Step 1:** During a deposit, `updateReserveInterests` is called at the beginning, updating indices (liquidityIndex and usageIndex) using the reserve's current state.

- **Step 2:** The deposit is processed, increasing the reserve’s liquidity.
- **Step 3:** Later, `updateInterestRatesAndLiquidity` is called, which in turn calls `updateReserveInterests` at its end, updating the indices again based on the new state.

This delayed update causes the indices to reflect a timestamp later than when the deposit was actually made. As a result, the accrued interest calculations for subsequent operations use stale indices, misrepresenting the actual interest earned or owed.

Demonstration:

* Reserve liquidity: 1,000 tokens

- Liquidity index: 1.0 RAY
- Last update timestamp: t = 0

**Ideal Update:**

* At t = 86,400 seconds (1 day), with a 1% daily interest, the liquidity index should update to approximately 1.01 RAY based solely on the original 1,000 tokens.

**Issue:**

* User A deposits 100 tokens at t = 86,000 seconds.
* Instead of updating the indices before processing the deposit, the protocol calls `updateReserveInterests` at the end of `updateInterestRatesAndLiquidity`.
* Consequently, the liquidity index is recalculated using the new total liquidity (1,100 tokens) and a time delta that includes the deposit. This late update causes the new index to be higher than it should be for the period before the deposit.

**Result:**

* Interest for early depositors is accrued using an outdated index (around 1.01 RAY), while User A’s deposit benefits from the inflated index calculated after the deposit.
* This misalignment leads to inaccurate interest computations and potential unfair distribution of rewards.

## Impact

* **Interest Miscalculation:**\
  Because indices are updated after liquidity changes, the calculated borrow and liquidity rates may not accurately reflect the interest that should have accrued during the deposit or withdrawal process. This mispricing can lead to either overcharging or underpaying interest.
* **Economic Discrepancy:**\
  Stakeholders—both borrowers and depositors—may receive rewards or incur costs that differ from what is expected. This misalignment can erode user trust, distort market incentives, and ultimately impact the protocol’s stability.

## Tools Used

manual review

## Recommendations

Call `updateReserveInterests` immediately before any state changes (liquidity or debt adjustments) occur.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | kobbyeugene, zgczgc |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

