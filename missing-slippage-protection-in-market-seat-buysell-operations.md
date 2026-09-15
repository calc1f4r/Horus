---
# Core Classification
protocol: Deriverse Dex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64524
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
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
finders_count: 4
finders:
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Missing Slippage Protection in Market Seat Buy/Sell Operations

### Overview


The `buy_market_seat()` and `sell_market_seat()` functions in the Deriverse protocol calculate seat prices based on the current number of clients, but do not protect against price changes. This can result in unexpected prices for users. The price calculation functions use a model where the price increases with each additional seat, but this can be affected by other market transactions. Users also cannot specify a maximum or minimum acceptable price, making it difficult to protect against unfavorable price movements. To fix this, the protocol should allow users to set limits on acceptable prices and validate the calculated price before execution. This issue has been fixed in the Deriverse protocol.

### Original Finding Content

**Description:** The `buy_market_seat()` and `sell_market_seat()` functions calculate seat prices dynamically based on the current `perp_clients_count` at execution time, but provide no slippage protection. Users cannot specify maximum/minimum acceptable prices, exposing them to unexpected price changes.

In `buy_market_seat()`, the seat price is calculated as:

```rust
let seat_price = PerpEngine::get_place_buy_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

instrument.seats_reserve += seat_price;
let price = data.amount + seat_price;
// ... price is deducted without validation
client_state.sub_crncy_tokens(price)?;
```

Similarly, in `sell_market_seat()`, the sell price is calculated:

```rust
let seat_price = PerpEngine::get_place_sell_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

client_state.add_crncy_tokens(seat_price)?;
```

The price calculation functions (`get_place_buy_price()` and `get_place_sell_price()`) use a bonding curve model where the price increases with each additional seat. The price is calculated based on:

```rust
pub fn get_place_buy_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply + 1, df)? - get_reserve(supply, df)?)
}

pub fn get_place_sell_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply, df)? - get_reserve(supply - 1, df)?)
}
```
The problem:
1. Between transaction submission and execution, other legitimate market transactions can change `perp_clients_count`, causing the actual execution price to differ from what the user expected
2. Users have no way to specify a maximum acceptable price for buying or minimum acceptable price for selling
3. The price is calculated and immediately applied without any validation against user expectations
4. During periods of high market activity, concurrent seat purchases/sales can cause significant price drift

**Impact:**
- **Unpredictable Execution:** Users have no guarantee that their transaction will execute at an acceptable price, even in normal market conditions
- **Poor User Experience:** Users cannot protect themselves from unfavorable price movements caused by legitimate concurrent market activity

**Recommended Mitigation:** Add slippage protection by allowing users to specify maximum/minimum acceptable prices in the instruction data, and validate the calculated price against these limits before execution.

**Deriverse:** Fixed in commit [a8181f3](https://github.com/deriverse/protocol-v1/commit/a8181f37e475eb1144f39490b62e45a476b2455d).

**Cyfrin:** Verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Deriverse Dex |
| Report Date | N/A |
| Finders | RajKumar, Ctrus, Alexzoid, JesJupyter |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

