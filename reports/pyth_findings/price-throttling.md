---
# Core Classification
protocol: GooseFX v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47696
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Price Throttling

### Overview


The update_price function in the oracle_price_history/mod.rs file does not properly limit the frequency of price updates, which can potentially allow for price manipulation. The minimum_elapsed_slots field is meant to prevent this by limiting the frequency of updates. However, the function currently does not take this into account, allowing for a user to manipulate the price by causing it to drop briefly and then quickly executing the minimum_elapsed_slots operation. This can significantly decrease the token price. To fix this, the function should check the elapsed slots since the last update and only allow updates if a sufficient number of slots have passed. This issue has been fixed in the b87a933 patch.

### Original Finding Content

## Update Price Function Vulnerability

The `update_price` function lacks a proper implementation of throttling price updates, potentially allowing price manipulation by exploiting `CrankPriceHistories`. The `minimum_elapsed_slots` field is intended to serve as a throttling mechanism, preventing frequent updates to the price history by limiting the frequency of price updates to avoid abuse or manipulation.

## Code Snippet

```rust
oracle_price_history/mod.rs

/// Push an update onto the historical prices array, using the appropriate
/// deserialization routine for the oracle type given by `self.oracle_type`.
pub fn update_price(
    &mut self,
    oracle_data: &[u8],
) -> Result<()> {
    let historical_price = match OracleType::from(self.oracle_type) {
        OracleType::Pyth => {
            HistoricalPrice::from_pyth_data(oracle_data)
        },
        OracleType::Switchboardv2 => {
            HistoricalPrice::from_switchboard_data(oracle_data)
        },
        _ => {
            return err!(SSLV2Error::InvalidOracleType);
        }
    }?;
    [...]
}
```

However, the function `update_price` currently doesn’t take into account the variable `minimum_elapsed_slots`. As a consequence, a user has the potential to manipulate the asset price by causing it to drop for a brief duration. Subsequently, they can exploit this situation by quickly executing the permissionless operation known as `minimum_elapsed_slots`. This operation involves processing a set of oracle and historical price accounts, updating the historical prices for each single-sided liquidity pool based on new oracle data. In this scenario, this unintended update can significantly decrease the token price in comparison to its initial value.

## Remediation

Ensure `update_price` checks the elapsed slots since the last update and only allows updates if a sufficient number of slots have passed, as specified by `minimum_elapsed_slots`.

## Patch

Fixed in commit `b87a933`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX v2 |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Thibault Marboud |

### Source Links

- **Source**: https://www.goosefx.io/
- **GitHub**: https://github.com/GooseFX1/gfx-ssl-v2
- **Contest**: https://www.goosefx.io/

### Keywords for Search

`vulnerability`

