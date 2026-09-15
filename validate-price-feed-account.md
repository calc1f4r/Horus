---
# Core Classification
protocol: Parcl
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48420
audit_firm: OtterSec
contest_link: https://www.parcl.co/
source_link: https://www.parcl.co/
github_link: github.com/ParclFinance/parcl-v2.

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
  - Ajay Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Validate Price Feed Account

### Overview

See description below for full details.

### Original Finding Content

## Price Feed Account Validation Issue

While creating the pool, the creator passes the price feed account. While validating the price feed account, it was not verified that the price feed account was owned by Pyth.

## Code Snippet

```rust
fn validate_pyth_price_feed(price_feed_info: &AccountInfo) -> Result<()> {
    let price_account_data = price_feed_info
        .try_borrow_data()
        .map_err(|_| CoreError::AccountBorrowFailed)?;
    let price_account = load_price_account(&price_account_data)
        .map_err(|_| CoreError::InvalidPythPriceAccountData)?;
    require!(
        price_account.agg.price >= 0,
        CoreError::PythPriceFeedAggPriceCannotBeNegative
    );
    Ok(())
}
```

## Remediation

Check if the Pyth price feed account is owned by Pyth.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Parcl |
| Report Date | N/A |
| Finders | Ajay Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.parcl.co/
- **GitHub**: github.com/ParclFinance/parcl-v2.
- **Contest**: https://www.parcl.co/

### Keywords for Search

`vulnerability`

