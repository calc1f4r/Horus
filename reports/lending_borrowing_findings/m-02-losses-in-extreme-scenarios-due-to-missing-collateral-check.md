---
# Core Classification
protocol: Tangent_2025-10-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63867
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
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

[M-02] Losses in extreme scenarios due to missing collateral check

### Overview


The bug report is about a function called `_liquidate()` that is used to calculate `collatValue` using an oracle price. The report states that the function does not have a check in place to ensure that the collateral value is enough to cover the debt repayment. This could result in losses for liquidators in extreme price movements or when the oracle is not up to date. The report recommends adding a check to protect liquidators or requiring the collateral value to always be greater than the debt repayment amount.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `_liquidate()` function calculates `collatValue` using oracle price and requires liquidators to burn `USGToRepay + fee`, but it doesn't verify that the collateral value is sufficient to cover the debt repayment. 

While `minUSGOut` provides slippage protection for the swap and liquidation fee, it doesn't protect against scenarios where the oracle-based `collatValue` is less than `USGToRepay`. 

In extreme price movements or oracle staleness, liquidators may be forced to burn more USG than they receive from selling the collateral, resulting in losses. The protocol should add a `minCollatValue` check to ensure liquidators are protected, or reject liquidations when `collatValue < USGToRepay` and route them to `seizeCollateral()` instead.

```solidity
if (collatValue > USGToRepay) {
    // Fee is taken on the liquidation profits
    uint256 delta = collatValue - USGToRepay;
    fee = (liquidationFee * delta) / DENOMINATOR;
}
```
We can observe that there is no Protection When `collatValue < USGToRepay`. This could cause the liquidator to bear the risk of price discrepancy in extreme price movement scenarios.


## Recommendations

Add a minimum collateral value check to protect liquidators or require the `collatValue` to always be greater than the `USGToRepay`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-10-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

