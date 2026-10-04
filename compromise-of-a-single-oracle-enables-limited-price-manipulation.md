---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17709
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jim Miller
  - Sam Moelius
  - Natalie Chin
---

## Vulnerability Title

Compromise of a single oracle enables limited price manipulation

### Overview


This bug report is about a data validation issue with the Apollo Oracle which is used to compute the median of a set of values provided by price oracles. An attacker could potentially gain control of the median price by compromising only one oracle, setting it to a value within a certain range. To exploit this, there must be an odd number of prices, and the attacker could turn a profit by adjusting the rate when buying and selling assets.

Short term, it is recommended to implement on-chain monitoring of the exchange and oracle contracts to detect any suspicious activity. Long term, the price computations should be made more robust to mitigate a partial compromise.

### Original Finding Content

## Data Validation

**Target:** frame/oracle/src/lib.rs

**Difficulty:** Medium

## Description
By compromising only one oracle, an attacker could gain control of the median price and set it to a value within a certain range. The Apollo Oracle computes the median of the first set of values provided by the price oracles. If the number of prices is odd (i.e., the median is the value in the center of the ordered list of prices), an attacker could skew the median price, setting it to a value between the lowest and highest prices submitted by the oracles.

## Exploit Scenario
There are three available oracles: O₀, with a price of 603; O₁, with a price of 598; and O₂, which has been compromised by Eve. Eve is able to set the median price to any value in the range [598, 603]. Eve can then turn a profit by adjusting the rate when buying and selling assets.

## Recommendations
**Short term:** Be mindful of the fact that there is no simple fix for this issue; regardless, we recommend implementing on-chain monitoring of the exchange and oracle contracts to detect any suspicious activity.

**Long term:** Assume that an attacker may be able to compromise some of the oracles. To mitigate a partial compromise, ensure that the price computations are robust.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Jim Miller, Sam Moelius, Natalie Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf

### Keywords for Search

`vulnerability`

