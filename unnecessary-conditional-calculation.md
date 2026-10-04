---
# Core Classification
protocol: Hubble Kamino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47881
audit_firm: OtterSec
contest_link: https://kamino.finance/
source_link: https://kamino.finance/
github_link: https://github.com/hubbleprotocol/kamino-lending

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
  - Thibault Marboud
  - OtterSec
---

## Vulnerability Title

Unnecessary Conditional Calculation

### Overview

See description below for full details.

### Original Finding Content

## Time-Weighted Average Price Calculation in Pyth and Scope

In Pyth and Scope, the time-weighted average price calculation persists even when the `token_info.is_twap_enabled()` condition evaluates to false. This behavior appears to be unnecessary and may result in computational overhead. This occurs as currently there is no mechanism implemented in `get_pyth_price_and_twap` and `get_scope_price_and_twap` to evaluate if only the price or both price and the time-weighted average price must be calculated.

## Pyth and Scope RUST Code

```rust
pub(super) fn get_pyth_price_and_twap(
    pyth_price_info: &AccountInfo,
) -> Result<TimestampedPriceWithTwap> {
    [...]
    let price = price_feed.get_price_unchecked();
    let twap = price_feed.get_ema_price_unchecked();
    [...]
    Ok(TimestampedPriceWithTwap {
        price: price.into(),
        twap: Some(twap.into()),
    })
}

pub(super) fn get_scope_price_and_twap(
    scope_price_account: &AccountInfo,
    conf: &ScopeConfiguration,
) -> Result<TimestampedPriceWithTwap> {
    let scope_prices = get_price_account(scope_price_account)?;
    let price = get_price_usd(&scope_prices, conf.price_chain)?;
    let twap = if conf.has_twap() {
        get_price_usd(&scope_prices, conf.twap_chain)
            .map_err(|e| msg!("No valid twap found for scope price, error: {:?}", e))
            .ok()
    } else {
        None
    };
    [...]
    Ok(TimestampedPriceWithTwap { price, twap })
}
```

## Remediation

Utilize the boolean value obtained from the `token_info.is_twap_enabled()` check as an argument in `get_pyth_price_and_twap` and `get_scope_price_and_twap`, within the `get_most_recent_price_and_twap` function. This approach would allow for conditional time-weighted average price calculation, thereby reducing computational overhead when it is not enabled for the token.

## Kamino Finance Audit 05 | General Findings

### Patch

Fixed in PR#112 by lazy loading the TWAP price only if it is enabled in the config.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Kamino |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Thibault Marboud, OtterSec |

### Source Links

- **Source**: https://kamino.finance/
- **GitHub**: https://github.com/hubbleprotocol/kamino-lending
- **Contest**: https://kamino.finance/

### Keywords for Search

`vulnerability`

