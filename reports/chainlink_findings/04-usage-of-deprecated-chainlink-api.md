---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43169
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-tigris
source_link: https://code4rena.com/reports/2022-12-tigris
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] Usage of deprecated chainlink API

### Overview

See description below for full details.

### Original Finding Content


`latestAnswer()` from chainlink is deprecated and can return stale data.

### Recommendation

Use `latestRoundData()` instead of `latestAnswer()`. Also, adding checks for [additional fields](https://docs.chain.link/data-feeds/price-feeds/api-reference/#latestrounddata) returned from `latestRoundData()` is recommended. E.g.

```
(uint80 roundID, int256 price,,uint256 timestamp, uint80 answeredInRound) = chainlink.latestRoundData();
require(timestamp != 0, "round not complete");
require(answeredInRound >= roundID, "stale data");
require(price != 0, "chainlink error");
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-12-tigris

### Keywords for Search

`vulnerability`

