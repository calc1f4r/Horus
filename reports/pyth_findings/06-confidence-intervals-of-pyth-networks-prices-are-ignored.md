---
# Core Classification
protocol: Flex Perpetuals
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49637
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-flex-perpetuals
source_link: https://code4rena.com/reports/2024-12-flex-perpetuals
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
finders_count: 0
finders:
---

## Vulnerability Title

[06] Confidence intervals of pyth network’s prices are ignored

### Overview

See description below for full details.

### Original Finding Content


The prices fetched by the Pyth network come with a degree of uncertainty, which is expressed as a confidence interval around the given price values. Considering a provided price `p`, its confidence interval `σ` is roughly the standard deviation of the price’s probability distribution. The [official documentation of the Pyth Price Feeds](https://docs.pyth.network/documentation/pythnet-price-feeds/best-practices# confidence-intervals) recommends some ways in which this confidence interval can be utilized for enhanced security. For example, the protocol can compute the value `σ/p` to decide the level of the price’s uncertainty and disallow user interaction with the system in case this value exceeds some threshold.

Currently, the protocol [completely ignores](https://github.com/code-423n4/2024-12-flex-perpetuals/blob/b84a0812c3368866964b8a16e7c36f6e7a50b655/src/handlers/IntentHandler.sol# L72-L73) the confidence interval provided by the price feed. Consider utilizing the confidence interval provided by the Pyth price feed as recommended in the official documentation. This would help mitigate the possibility of users taking advantage of invalid prices.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Flex Perpetuals |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-flex-perpetuals
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-12-flex-perpetuals

### Keywords for Search

`vulnerability`

