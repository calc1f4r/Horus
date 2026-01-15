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
solodit_id: 54027
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

Governance needs to ensure weight is proportional to market volume 

### Overview

See description below for full details.

### Original Finding Content

## Context: MARKETS.md#L500

## Description
A common attack in DeFi lending protocols is inflating collateral through price manipulation. Suppose a token is eligible for collateral but not very liquid. In that case, it is possible to inflate the price temporarily (as in Mango Markets) or permanently (as in CREAM finance) with the result that a large batch of the token inside the protocol is apparently worth far more than it could be sold for in the market. Price manipulation is "real" because the actual spot price changes for a brief period. If the manipulation cost is lower than the available funds to borrow in the protocol, then the attack is worth it. Even if there is no typical lending, only margin, the attack may still be worthwhile if the attacker can take a large leveraged position on what is essentially a binary bet and have something like a 50/50 chance of making a large amount from their leveraged position.

## Recommendation
Ensure that weight is proportional to the market volume included in the Pyth price updates and the total value locked in the L2. Monitor for changes.

## LayerN
Acknowledged.

## Cantina Managed
Acknowledged. Will be handled by setting appropriate asset weights and monitoring them.

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

