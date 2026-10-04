---
# Core Classification
protocol: Hubble Scope
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47612
audit_firm: OtterSec
contest_link: https://hubbleprotocol.io/
source_link: https://hubbleprotocol.io/
github_link: https://github.com/hubbleprotocol/scope

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Tamta Topuria
  - OtterSec
---

## Vulnerability Title

Negative Exponent

### Overview

See description below for full details.

### Original Finding Content

## Handling Negative Exponents in Pyth and Pyth EMA

In `pyth` and `pyth_ema`, while calculating the price from `pyth_price`, the case where the exponent (expo) of the price is negative is not handled.

## Code Example

### File: `oracles/pyth_ema.rs`

```rust
pub fn get_price(price_info: &AccountInfo) -> Result<DatedPrice> {
    [...]
    Ok(DatedPrice {
        price: Price {
            value: price,
            exp: pyth_price.expo.abs().try_into().unwrap(),
        },
        last_updated_slot: price_account.valid_slot,
        unix_timestamp: u64::try_from(price_account.timestamp).unwrap(),
        ..Default::default()
    })
}
```

The code only considers the absolute value of the exponent when calculating the price from Pyth data. The exponent represents the scale factor for the price, determining the number of decimal places to move the implied decimal point. Thus, ignoring the sign of the exponent may result in incorrect unit conversions. 

In cases where the exponent is negative, neglecting the sign could result in miscalculations of the price units.

## Remediation

Handle negative exponents properly in `pyth` and `pyth_ema` to ensure accurate unit conversions.

## Patch

Fixed in PR#221.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Scope |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Tamta Topuria, OtterSec |

### Source Links

- **Source**: https://hubbleprotocol.io/
- **GitHub**: https://github.com/hubbleprotocol/scope
- **Contest**: https://hubbleprotocol.io/

### Keywords for Search

`vulnerability`

