---
# Core Classification
protocol: Rubicon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48946
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1003

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0xDING99YA
  - Toshii
  - immeas
---

## Vulnerability Title

[H-07] Wrong calculation of repayment amount in Position contract

### Overview


This bug report discusses an issue with the `closePosition(..)` function in the `Position` contract. When a user calls this function, the amount they need to repay is calculated using the `borrowBalanceOfPos(..)` function, which takes into account the amount borrowed and the interest accrued. However, the calculation of interest may be incorrect due to the `borrowRate` being defined as a function of total borrows and supply, which can change over time. This can result in an incorrect amount being repaid, potentially leading to excess assets being swapped. The report recommends keeping track of changes in supply and borrow state to mitigate this issue. The severity of this bug has been marked as high as it affects the repayment amount. 

### Original Finding Content


<https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L282> <br><https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L82> <br><https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L329-L331> <br><https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L87>

When a user calls `closePosition(..)` -> `_repay(..)` on the `Position` contract, the function `borrowBalanceOfPos(..)` is used to calculate the amount that the user needs to repay. This repayment amount is equivalent to the amount the user borrowed (`_borrowedAmount`) plus their interest (`_interest`). To calculate this interest portion, the function multiplies the current `borrowRate` by the difference in number of blocks between when the user created the position and the current block timestamp. The issue arises because the `borrowRate` over the entire duration of the borrow is defined as: `rate = CTokenInterface(bathToken).borrowRatePerBlock();`. However, `borrowRatePerBlock()` is a function of total borrows and total supply for the `cToken`; thus, is not required to be the same over the entire duration of when the user takes it out of their position. This means the calculated repayment amount can potentially overshoot/undershoot the actual amount.

### Proof of Concept

Steps:
1. Bob uses the `Position` contract to open a leveraged position using the `buyAllAmountWithLeverage(..)` function. This results in an increased borrow interest rate.
2. Later, Alice also uses the `Position` contract to open a leveraged position using the `buyAllAmountWithLeverage(..)` function. This again results in an increased borrow interest rate.
3. Bob calls `closePosition(..)`, where the call to `_repay(..)` references the current `borrowRatePerBlock()`, which prices Bob's interest at the rate which includes Bob and Alice's borrows.

This results in excess `asset` being swapped to `quote`, rather than what is needed for repayment.

### Recommended Mitigation Steps

Potentially keep track of changes in the supply/borrow state. However, this might not be worth the tradeoff in increased gas.

**[daoio (Rubicon) confirmed](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1003#issuecomment-1534074919)**

**[HickupHH3 (judge) increased severity to High and commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1003#issuecomment-1560368752):**
 > Incorrect interest calculation, consider this to be high severity because it affects repay amount.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | 0xDING99YA, Toshii, immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1003
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

