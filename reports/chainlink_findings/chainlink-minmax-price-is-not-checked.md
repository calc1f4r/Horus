---
# Core Classification
protocol: Conic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29935
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#5-chainlink-minmax-price-is-not-checked
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
  - MixBytes
---

## Vulnerability Title

Chainlink `min&max` price is not checked

### Overview

See description below for full details.

### Original Finding Content

##### Description

- https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/oracles/ChainlinkOracle.sol#L68

Some chainlink aggregators have min and max price. The price of an asset cannot go outside the range of min and max price. 

- https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits

`When the reported answer is close to reaching reasonable minimum and maximum limits ... it can alert you to potential market events.`

##### Recommendation

According to Chainlink's recommendation:
`Configure your application to detect and respond to extreme price volatility or prices that are outside of your acceptable limits.`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Conic Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#5-chainlink-minmax-price-is-not-checked
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

