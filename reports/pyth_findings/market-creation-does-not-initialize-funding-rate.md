---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54003
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
github_link: none

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
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Market creation does not initialize funding rate 

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Context
- `book.rs#L407-L448`
- `book.rs#L998`
- `mod.rs#L114-L118`

## Description
Markets are created by the administrator through the `CreateMarket` action. Once a market is created, trades are instantly enabled on this market. However, the newly created market has no funding rate. The funding index of a market without a funding rate will be zero, as shown in the `get_market_funding_index` function (through the use of `unwrap_or_default()`):

```rust
pub(crate) fn get_market_funding_index(&self, market_id: u32) -> FundingIndexMantissa {
    self.current_funding_info
        .get(&market_id)
        .map(|x| x.funding_index)
        .unwrap_or_default()
}
```

The funding rate for the market will be initialized during the next Pyth feed update. This gives an attacker an opportunity to exploit the zero funding rate.

## Recommendation
The market creation process should also initialize the funding rate for this market. Another way to fix this issue is to ensure that the market is not usable while there is no funding rate.

## LayerN
Fixed in PR 1113.

## Canitna Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

