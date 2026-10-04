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
solodit_id: 59537
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

Incorrect Chainlink Interface

### Overview

See description below for full details.

### Original Finding Content

**Update**
Fixed in: `341c883754b3e8127b2648b58865633cec1b31ec`.

The client provided the following explanation:

> _Used correct interfaces_

**Description:** The `IChainlinkAggregator` interface is not entirely correct in its implementation. The `minAnswer()` and `maxAnswer()` function never exist in the same contract as the `aggregator()` function. More specifically, the `aggregator()` function is implemented in Chainlink's price feed contract and the `minAnswer()` and `maxAnswer()` functions are implemented in the aggregator contract returned by the `aggregator()` function.

However, it doesn't cause any issues in this codebase because the different functions are only called on the respective contracts.

**Recommendation:** To prevent confusion when reusing this interface, we recommend splitting it into two interfaces, representing the respective contracts: the aggregator and the price feed contract.

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

