---
# Core Classification
protocol: Aftermath Orderbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47456
audit_firm: OtterSec
contest_link: https://aftermath.finance/
source_link: https://aftermath.finance/
github_link: https://github.com/AftermathFinance

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Risk Of Arithmetic Overflow

### Overview


This bug report discusses a situation where a user submits a bid with a very high price, which can prevent other users from placing additional bids. This is due to a potential overflow in the code that calculates the tick size and base and quote asset deltas within the orderbook. The report recommends using a function called "checked_mul" to prevent overflows from occurring. The bug has been fixed in a recent patch.

### Original Finding Content

## Overflow Risks in Bid Submission

In situations where a user submits a bid at an exceedingly high price, such as `TICK_SIZE * ((0x8000_0000_0000_0000 - TICK_SIZE) / TICK_SIZE)`, where `0x8000_0000_0000_0000` signifies the maximum value of a variable type `u64`, it may prevent other users from placing additional bids. This is due to the potential overflow in `ticks_per_lot_to_quote_per_base` and `get_base_and_quote_asset_deltas` within the orderbook.

> _sources/orderbook.move

```rust
fun ticks_per_lot_to_quote_per_base(
    ticks_per_lot: u64, 
    lot_size: u64, 
    tick_size: u64,
) -> u256 {
    ifixed::from_fraction(ticks_per_lot * tick_size, lot_size)
}

fun get_base_and_quote_asset_deltas(
    price: u64,
    size: u64,
    lot_size: u64,
    tick_size: u64,
) -> (u256, u256) {
    let base_asset_balance9 = size * lot_size;
    let quote_asset_balance9 = size * price * tick_size;
    let base_asset_delta = ifixed::convert_balance9_to_fixed(base_asset_balance9);
    let quote_asset_delta = ifixed::convert_balance9_to_fixed(quote_asset_balance9);
    (base_asset_delta, quote_asset_delta)
}
```

In `ticks_per_lot_to_quote_per_base`, there is a multiplication operation: `ticks_per_lot * tick_size`. Thus, if the outcome of this multiplication surpasses the maximum representable value of a `u64`, it may result in an integer overflow. Similarly, in the calculation of `quote_asset_balance9` within `get_base_and_quote_asset_deltas`, the multiplication of `size`, `price`, and `tick_size` (all of type `u64`) may also result in an overflow.

## Remediation
Utilize `checked_mul`, which returns `None` if an overflow occurs.

---

© 2024 Otter Audits LLC. All Rights Reserved. 6/21  
Aftermath Audit 04 — Vulnerabilities  
Patch Fixed in 7bd64b0.  
© 2024 Otter Audits LLC. All Rights Reserved. 7/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aftermath Orderbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://aftermath.finance/
- **GitHub**: https://github.com/AftermathFinance
- **Contest**: https://aftermath.finance/

### Keywords for Search

`vulnerability`

