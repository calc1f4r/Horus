---
# Core Classification
protocol: Aries Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47308
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: https://github.com/aries-markets/aries-markets

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
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Incorrect Liquidity Calculation

### Overview


The function get_borrow_rate is currently calculating the utilization ratio and interest rates incorrectly, resulting in lower interest rates for borrowers. This is due to an incorrect calculation of total_liquidity, which includes the reserve_amount instead of subtracting it. This leads to an overestimation of total_liquidity and a lower utilization ratio. As a result, borrowers are being charged a lower interest rate than intended. To fix this issue, the decimal::add function should be changed to decimal::sub in the calculation of total_liquidity. This will ensure an accurate utilization ratio and appropriate interest rate calculations. The bug has been fixed in the latest patch. 

### Original Finding Content

## Issue with `get_borrow_rate`

The issue in `get_borrow_rate` may result in miscalculated utilization ratios and lower interest rates for borrowers than intended. The function currently calculates `total_liquidity` by adding the `reserve_amount` (unborrowed reserve funds) to the sum of `total_borrowed` and `decimal::from_u128(total_cash)`, which is incorrect. The utilization ratio is calculated by dividing `total_borrowed` by `total_liquidity`. With the incorrect calculation, the `total_liquidity` is overestimated because the `reserve_amount` is added instead of subtracted, lowering the utilization ratio.

```rust
> _interest_rate_config.move
public fun get_borrow_rate(
    config: &InterestRateConfig,
    total_borrowed: Decimal,
    total_cash: u128,
    reserve_amount: Decimal,
): Decimal {
    if (decimal::eq(total_borrowed, decimal::zero())) {
        return decimal::zero()
    };
    let total_liquidity = decimal::add(
        total_borrowed,
        decimal::add(reserve_amount, decimal::from_u128(total_cash))
    );
    [...]
}
```

The utilization ratio determines the borrow rate. A lower utilization ratio calculated due to the flawed formula would incorrectly imply that the reserve is less utilized than it actually is. This will result in a lower borrow rate being charged to borrowers compared to what it should be based on the true utilization level.

## Remediation

Change the `decimal::add` to `decimal::sub` in the calculation of `total_liquidity`. This will ensure the `reserve_amount` is subtracted, resulting in an accurate utilization ratio and appropriate borrow rate calculations.

## Patch

Fixed in `7564ea2`.

© 2024 Otter Audits LLC. All Rights Reserved. 12/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: https://github.com/aries-markets/aries-markets
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`

