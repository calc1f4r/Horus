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
solodit_id: 48788
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

Missing Pyth Oracle Confidence Interval Check

### Overview

See description below for full details.

### Original Finding Content

## Asset Price Update Issue with Pyth's Oracle

The program is missing confidence interval checks while fetching asset price updates for options from Pyth’s oracle. A high confidence interval denotes that Pyth’s price is inaccurate and must not be used by the program. Alternatively, the program can fall back to another oracle. 

## Code Snippet

It can be seen in the following snippet that the program uses Pyth’s price without checking:

```rust
let current_price: Price = price_feed.get_current_price().unwrap();
let price = (current_price.price as u128)
    .checked_mul(10u128.pow(USDC_DECIMALS))
    .unwrap()
    .checked_div(10u128.pow((-current_price.expo) as u32))
    .unwrap() as u128;
return Some(price);
```

## Remediation

It is recommended to add a confidence interval check while using the Pyth oracle. For more information, please refer to the code linked in the footnote below.

```rust
if conf > PYTH_CONF_FILTER {
    msg!(
        "Pyth conf interval too high; oracle index: {} value: {} conf: {}",
        [...]
    );
    return Err(throw_err!(MangoErrorCode::InvalidOraclePrice));
}
```

[1]: https://github.com/blockworks-foundation/mango-v3/blob/6b01e3f63d2a0f97eb08b734317ef47e3f667c4f/program/src/processor.rs#L6860

## Patch

The confidence interval is now checked. Fixed in #198.

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

