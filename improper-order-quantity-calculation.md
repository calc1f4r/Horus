---
# Core Classification
protocol: Mysten Deepbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47059
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/deepbookv3

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
finders_count: 3
finders:
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Improper Order Quantity Calculation

### Overview


The functions get_quantity_out and get_level2_range_and_ticks in the current implementation do not accurately calculate the remaining quantity of orders. This is due to the fact that they do not take into account partially filled or modified orders, resulting in overestimating available liquidity and incorrect calculation of quantity_out. The code also does not properly iterate over orders and aggregate quantities, leading to inaccurate results. To fix this issue, the functions need to be modified to utilize the remaining quantity of orders instead of the initial quantity. This fix has been implemented in PR #227.

### Original Finding Content

## Current Implementation Issues

The current implementations of `get_quantity_out` and `get_level2_range_and_ticks` do not account for the remaining quantity of orders. This omission may result in inaccurate calculations. 

In `get_quantity_out`, if an order has been partially filled or modified, the `order.quantity` will not reflect the remaining available quantity for matching, thus overestimating the available liquidity and resulting in incorrect `quantity_out` calculations.

```kotlin
> _book.moverust
public(package) fun get_level2_range_and_ticks(
    [...]
): (vector<u64>, vector<u64>) {
    [...]
    while (!ref.is_null() && ticks_left > 0) {
        [...]
        if (cur_price != 0) {
            cur_quantity = cur_quantity + order.quantity();
        };
        (ref, offset) = if (is_bid) book_side.prev_slice(ref, offset) else
                        book_side.next_slice(ref, offset);
    };
    [...]
}
```

Similarly, `get_level2_range_and_ticks` iterates over the orders in the book and aggregates quantities via `order.quantity`, but it does not account for the remaining quantity after partial executions or modifications, resulting in inaccurate aggregation of quantities at different price levels.

## Remediation

Modify the above functions to utilize the remaining quantity of orders instead of the initial quantity.

## Patch

Resolved in PR #227.

© 2024 Otter Audits LLC. All Rights Reserved. 03/27

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Deepbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/deepbookv3
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

