---
# Core Classification
protocol: Euler Price Oracle Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32435
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/price-oracle-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Chainlink Adapter Can Return Incorrect Price During Flash Crashes

### Overview

See description below for full details.

### Original Finding Content

Some Chainlink price feeds might have a built-in minimum and maximum price that they can return. In the event the price falls below the minimum price or crosses the maximum price, the Chainlink oracle will return an incorrect price. This can lead to catastrophic consequences.


Consider allowing the deployer to define a percentage margin and if the price returned by Chainlink is within that narrow percentage of the minimum price or the maximum price, the adapter should revert. The minimum price and maximum price can be retrieved from the [`OffchainAggregator`](https://docs.chain.link/data-feeds/api-reference/#variables-and-functions-in-accesscontrolledoffchainaggregator) contract of the price feed at the `minAnswer` and `maxAnswer` variables.


***Update:** Acknowledged, not resolved. The Euler team stated:*



> *Acknowledged. We chose not to use `minAnswer` and `maxAnswer` as indicators for the Chainlink oracle malfunctioning. It is unclear whether these values are expected to change, while reading them on every call would add a gas overhead to what would be a very hot path in production.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Euler Price Oracle Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/price-oracle-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

