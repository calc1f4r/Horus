---
# Core Classification
protocol: Parrot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48689
audit_firm: OtterSec
contest_link: https://parrot.fi/mint/
source_link: https://parrot.fi/mint/
github_link: github.com/gopartyparrot/parrot-monorepo.

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
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Stale Oracle Price

### Overview

See description below for full details.

### Original Finding Content

## Flux Aggregator and Collateral Token Price in Debt Tokens

In the program, `flux-aggregator` is used for getting the collateral token price in debt tokens. This price is then used for checking the collateral ratio during liquidation.

## Function: `read_collateral_token_price_from_account`

```rust
pub fn read_collateral_token_price_from_account(
    aggregator_info: &AccountInfo,
) -> Result<(u64, u8)> {
    let (answer, decimal) = flux_aggregator::read_price(aggregator_info)?;
    Ok((answer.median, decimal))
}
```

The `flux_aggregator::read_price` function returns an `Answer` struct and price decimals.

## Struct: `Answer`

```rust
pub struct Answer {
    pub round_id: u64,
    pub median: u64,
    pub created_at: u64,
    pub updated_at: u64,
}
```

The `read_collateral_token_price_from_account` function uses the median price, but does not validate `updated_at` to ensure the price was updated recently. This could lead to price discrepancies with the market.

## Vulnerability

An attacker can abuse the stale oracle price to bypass the collateral ratio check and get excess debt for staked collateral.

## Remediation

The program should validate `updated_at` to ensure that the oracle price was updated recently. Ideally, within the last 10 seconds.

© 2022 OtterSec LLC. All Rights Reserved. 10 / 24

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Parrot |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://parrot.fi/mint/
- **GitHub**: github.com/gopartyparrot/parrot-monorepo.
- **Contest**: https://parrot.fi/mint/

### Keywords for Search

`vulnerability`

