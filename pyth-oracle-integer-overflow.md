---
# Core Classification
protocol: Cega
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48789
audit_firm: OtterSec
contest_link: https://www.cega.fi/
source_link: https://www.cega.fi/
github_link: https://github.com/cega-fi/cega-vault.

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
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Pyth Oracle Integer Overflow

### Overview

See description below for full details.

### Original Finding Content

## Price Calculation in Oracle Program

In `get_oracle_price`, the program assumes that the price exponent will be negative [0]. Unfortunately, the Pyth oracle program allows for the price exponent of a product to be positive.

## Code Snippet

```c
pyth-client/program/src/oracle/oracle.c
static uint64_t add_price(SolParameters *prm, SolAccountInfo *ka) {
    // Validate command parameters
    cmd_add_price_t *cptr = (cmd_add_price_t*)prm->data;
    if (prm->data_len != sizeof(cmd_add_price_t) ||
        cptr->expo_ > PC_MAX_NUM_DECIMALS ||
        cptr->expo_ < -PC_MAX_NUM_DECIMALS) {
        // handle error
    }
}
```

```rust
cega-vault/src/utils.rs
let price = (current_price.price as u128)
    .checked_mul(10u128.pow(USDC_DECIMALS))
    .unwrap()
    .checked_div(10u128.pow((-current_price.expo) as u32)) // [0]
    .unwrap() as u128;
```

If `current_price.expo` is positive, the `pow` operation will lead to an integer overflow and the program will panic. Due to this, all calls to `calculation_agent` will panic. This isn't necessarily an issue because all products currently listed on Pyth have a negative price exponent. However, the program must perform the price calculation correctly to avoid any future implications.

## Remediation

Check if `current_price.expo` is positive, and use `checked_mul` in such a case. For more information, please refer to the code snippet below.

```rust
let mut price = (current_price.price as u128)
    .checked_mul(10u128.pow(USDC_DECIMALS))
    .unwrap();
if current_price.expo < 0 {
    price = price.checked_div(10u128.pow((-current_price.expo) as u32)).unwrap() as u128;
} else {
    price = price.checked_mul(10u128.pow(current_price.expo as u32)).unwrap() as u128;
}
return Some(price);
```

## Patch

The issue has been fixed and now `checked_mul` is used if `current_price.expo` is positive. Fixed in #194.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cega |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.cega.fi/
- **GitHub**: https://github.com/cega-fi/cega-vault.
- **Contest**: https://www.cega.fi/

### Keywords for Search

`vulnerability`

