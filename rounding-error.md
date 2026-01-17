---
# Core Classification
protocol: Jupiter Perps Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47708
audit_firm: OtterSec
contest_link: https://jup.ag/perps
source_link: https://jup.ag/perps
github_link: https://github.com/jup-ag/perpetuals

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
finders_count: 4
finders:
  - Robert Chen
  - Thibault Marboud
  - OtterSec
  - Nicola Vella
---

## Vulnerability Title

Rounding Error

### Overview


This bug report discusses a vulnerability in the get_new_price function, which calculates the average price of a trading position. The vulnerability allows an attacker to manipulate the size_usd_delta parameter, resulting in the average price not increasing proportionally to the position size. This can lead to the user realizing a substantial profit upon exiting the position. The report also includes a proof of concept and recommends a patch to fix the issue. 

### Original Finding Content

## Vulnerability Summary

The `size_usd_delta` parameter in `get_new_price` is manipulable to artificially increase the position’s average price without a corresponding increase in the average position price. The `get_new_price` function calculates the new average price of a trading position based on changes in size and the current market price. 

The vulnerability arises since the function does not enforce a minimum `size_usd_delta`, allowing an attacker to incrementally increase the position size while keeping the average price identical.

## Code Snippet

```rust
pub fn get_new_price(&self, next_price: u64, size_usd_delta: u64) -> Result<u64> {
    if self.size_usd == 0 {
        return Ok(next_price);
    }
    if size_usd_delta == 0 {
        return Ok(self.price);
    }
    let next_size = math::checked_add(self.size_usd, size_usd_delta)?;
    // get PnL delta
    let price_delta = self.price.abs_diff(next_price);
    let pnl_delta: u64 = math::checked_as_u64(math::checked_div(
        math::checked_mul(self.size_usd as u128, price_delta as u128)?,
        self.price as u128,
    )?)?;
    // when price go up, pnl is positive for long, negative for short
    // when price go down, pnl is negative for long, positive for short
    let next_size_with_pnl = if next_price > self.price {
        math::checked_add(next_size, pnl_delta)?
    } else {
        math::checked_sub(next_size, pnl_delta)?
    };
    math::checked_as_u64(math::checked_div(
        math::checked_mul(next_size as u128, next_price as u128)?,
        next_size_with_pnl as u128,
    )?)
}
```

This results in the average price for a position not rising proportionally and remaining consistent. Consequently, given that the position price is now notably higher while the average price remains unchanged, the user realizes a substantial profit upon exiting the position, as the protocol utilizes the average price to compute the profit and loss (PnL) during the exit.

## Jupiter Perp Audit 04 | Vulnerabilities

### Proof of Concept

1. Assume there is a long position with an initial `size_usd` quantity and an initial `average_price`.
2. The market price increases.
3. An attacker incrementally increases the position with a small `size_usd_delta` (e.g., one) each time.
4. Since the protocol utilizes round-down logic when calculating the average price, the small `size_usd_delta` does not trigger any change, and the average price effectively remains the same.
5. After multiple iterations of increasing the position size with small `size_usd_delta` values, the position’s `size_usd` becomes larger, but the average price remains the same.
6. Upon the attacker’s decision to close the position, the calculation of profit occurs utilizing the average price. Given that the average price has not risen in proportion to the growth in position size, the attacker realizes a profit from the position.

### Remediation

Ensure for long positions, the average price is rounded up, while for short positions, the average price is rounded down.

### Patch

Fixed in commit `80fdf99`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jupiter Perps Program |
| Report Date | N/A |
| Finders | Robert Chen, Thibault Marboud, OtterSec, Nicola Vella |

### Source Links

- **Source**: https://jup.ag/perps
- **GitHub**: https://github.com/jup-ag/perpetuals
- **Contest**: https://jup.ag/perps

### Keywords for Search

`vulnerability`

