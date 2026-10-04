---
# Core Classification
protocol: Hedge Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48837
audit_firm: OtterSec
contest_link: https://www.hedge.so/
source_link: https://www.hedge.so/
github_link: https://github.com/Hedge-Finance/hedge-vault/.

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - Mohan Pedhapati
  - OtterSec
---

## Vulnerability Title

Missing Pyth Oracle Confidence Interval Check

### Overview

See description below for full details.

### Original Finding Content

## Price Updates with the Pyth Oracle

## Missing Confidence Interval Checks

Price updates with the Pyth oracle are missing confidence interval checks. A high confidence interval means that Pyth’s price is not accurate and the program must fall back to another oracle. It can be seen in the following snippets that the Pyth price update only checks the slot but not the confidence interval.

### Code Snippet 1: Refresh Oracle Price

```rust
let pyth_price_account: Price =
load_price(&oracle_pyth.try_borrow_data()?).unwrap().clone();
let result = get_verified_price(
    &pyth_price_account,
    oracle_chainlink,
    Clock::get().unwrap().slot,
)
.unwrap();
vault_type_account.recent_price = result.to_account(); // [0]
vault_type_account.price_last_updated_timestamp =
    Clock::get().unwrap().unix_timestamp.to_u64().unwrap();
Ok(())
```

### Code Snippet 2: Get Verified Price

```rust
fn get_verified_price(
    pyth_price_account: &Price,
    oracle_chainlink: &AccountInfo,
    current_slot: u64,
) -> Option<Decimal> {
    let max_slot_age = 60u64;
    let current_pyth_price: Option<PriceConf> =
        pyth_price_account.get_current_price();
    // Check if Pyth has current price
    if current_pyth_price.is_some() {
        msg!("HEDGE: Checking Pyth Price age");
        let price_conf = current_pyth_price.unwrap();
        let result = Decimal::from_i64(price_conf.price)
            .unwrap();
```

### References
- [0] Reference to the price update code snippet.
- [1] Reference to where confidence intervals should be checked.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hedge Vault |
| Report Date | N/A |
| Finders | Robert Chen, Mohan Pedhapati, OtterSec |

### Source Links

- **Source**: https://www.hedge.so/
- **GitHub**: https://github.com/Hedge-Finance/hedge-vault/.
- **Contest**: https://www.hedge.so/

### Keywords for Search

`vulnerability`

