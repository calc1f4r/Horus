---
# Core Classification
protocol: Swaap Earn Protocol Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59532
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/swaap-earn-protocol-vaults/3fa72f3f-1132-4aa6-a88f-938b02195c1a/index.html
source_link: https://certificate.quantstamp.com/full/swaap-earn-protocol-vaults/3fa72f3f-1132-4aa6-a88f-938b02195c1a/index.html
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
  - Roman Rohleder
  - Adrian Koegl
  - Guillermo Escobero
---

## Vulnerability Title

Chainlink Decimals Assumption

### Overview

See description below for full details.

### Original Finding Content

**Update**
Fixed in: `87b3ef1c4125f0313f68ef9173573c2375a2090f`.

The client provided the following explanation:

> _A check was added._

**File(s) affected:**`PriceRouter.sol`

**Description:** Although most of the Chainlink price feeds return prices with 18 decimals for ETH pairs and 8 decimals for non-ETH pairs, a small subset of pairs do not follow this.

The protocol assumes 8 decimals for all price feeds, leading to wrong calculations if price decimals are different.

**Recommendation:** While setting a new Chainlink source in `PriceRouter._setupPriceForChainlinkDerivative()`, consider calling `decimals()` in the Chainlink contract and verifying the return value is eight.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Swaap Earn Protocol Vaults |
| Report Date | N/A |
| Finders | Roman Rohleder, Adrian Koegl, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/swaap-earn-protocol-vaults/3fa72f3f-1132-4aa6-a88f-938b02195c1a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/swaap-earn-protocol-vaults/3fa72f3f-1132-4aa6-a88f-938b02195c1a/index.html

### Keywords for Search

`vulnerability`

