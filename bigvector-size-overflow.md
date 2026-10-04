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
solodit_id: 47060
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

BigVector Size Overflow

### Overview


The bug report discusses an issue with the initialization of two BigVector instances for storing bid and ask orders. The problem arises from setting the max_slice_size parameter to 10000, which affects the size of leaf nodes in the underlying data structure. This can result in excessively large leaf objects, which can cause errors in the Mover runtime and prevent the order book from functioning correctly. The report suggests setting the max_slice_size to a more appropriate value (less than 2000) to reduce the size of leaf objects and avoid object size limitations. The issue has been resolved in PR #176.

### Original Finding Content

## Book Initialization Issue

The `empty` function initializes two `BigVector` instances for storing bid and ask orders, respectively. The issue arises from setting the `max_slice_size` parameter to `10000` when creating these `BigVector` instances. This parameter influences the size of leaf nodes in the underlying data structure. A large `max_slice_size` results in excessively large leaf objects.

> _book.moverust_

```rust
public(package) fun empty(
    tick_size: u64,
    lot_size: u64,
    min_size: u64,
    ctx: &mut TxContext,
): Book {
    Book {
        tick_size,
        lot_size,
        min_size,
        bids: big_vector::empty(64, 64, ctx),
        asks: big_vector::empty(64, 64, ctx),
        next_bid_order_id: START_BID_ORDER_ID,
        next_ask_order_id: START_ASK_ORDER_ID,
    }
}
```

This is especially relevant due to the Sui Move runtime’s limitation on maximum object size, which is `256000 bytes`. If the leaf objects in the `BigVector` exceed this limit, the Move runtime will throw an error, preventing the order book from functioning correctly.

## Remediation

Set the `max_slice_size` value to a more appropriate value (less than `2000`) to reduce the size of leaf objects and prevent object size limitations.

## Patch

Resolved in PR #176.

© 2024 Otter Audits LLC. All Rights Reserved. 14/27

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

