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
solodit_id: 54029
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

Use conﬁdence interval from Pyth oracles to calculate a spread price 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
Pyth provides confidence intervals on the reported prices. In addition to pausing trading in high volatility scenarios where the price confidence interval is too large, it also offers an opportunity to set a dynamic spread for price calculations.

For example, when calculating loan-to-value, the value of a user's collateral, it's beneficial to use a more conservative price, indicating what the assets are worth on the sell side (because in a pinch, the protocol is a seller). On the other hand, when calculating the value of the loan, the engine would be better off using a more optimistic price, indicating the buy side worth of the assets (because in a pinch the protocol is a buyer). Buyers will naturally flock to sources where the asset is cheaper, and sellers will naturally flock to places where it is more expensive.

However, setting a reasonable dynamic spread is a challenging problem absent any additional information except the asset price. However, the confidence interval, reflecting the variety of prices at various sources, gives a natural way to calculate spreads.

## Recommendation
Use the confidence interval of Pyth prices to set a spread price and use conservative calculations where appropriate in the code.

## LayerN
Fix in progress. We are planning on implementing spread calculations, using a lower or higher price (for example, the higher price for calculating loan value and the lower price for calculating collateral value), to ensure the price used always benefits the engine, with the spread size adjusted based on the price confidence interval.

## Cantina Managed
Acknowledged. Proposed plan for implementation is sound.

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

