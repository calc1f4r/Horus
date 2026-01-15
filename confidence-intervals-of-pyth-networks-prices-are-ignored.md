---
# Core Classification
protocol: Anvil Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41258
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/anvil-audit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Confidence Intervals of Pyth Network's Prices Are Ignored

### Overview


The Pyth network provides prices with a confidence interval, which is a measure of uncertainty around the given price values. However, the current protocol ignores this confidence interval, which can potentially allow users to exploit invalid prices. The official documentation recommends using the confidence interval to enhance security, and a pull request has been made to resolve this issue. The Ampera team plans to use a "sanity check" to ensure that the confidence interval is smaller than the price, and will upgrade the price oracle if there are any issues.

### Original Finding Content

The prices fetched by the Pyth network come with a degree of uncertainty which is expressed as a confidence interval around the given price values. Considering a provided price `p`, its confidence interval `σ` is roughly the standard deviation of the price's probability distribution. The [official documentation of the Pyth Price Feeds](https://docs.pyth.network/documentation/pythnet-price-feeds/best-practices#confidence-intervals) recommends some ways in which this confidence interval can be utilized for enhanced security. For example, the protocol can compute the value `σ / p` to decide the level of the price's uncertainty and disallow user interaction with the system in case this value exceeds some threshold.


Currently, the protocol [completely ignores](https://github.com/AmperaFoundation/sol-contracts/blob/4c4423791b3427153937881fc5287a81283ee141/contracts/Pricing.sol#L7-L15) the confidence interval provided by the price feed. Consider utilizing the confidence interval provided by the Pyth price feed as recommended in the official documentation. This would help mitigate the possibility of users taking advantage of invalid prices.


***Update:** Resolved in [pull request \#148](https://github.com/AmperaFoundation/sol-contracts/pull/148). The Ampera team stated:*



> *The approach taken is to "sanity check" the price making sure that the Confidence Interval is smaller than the price, as we are largely relying on the oracle to have a good price. If somehow there is an issue with the oracle, related to Confidence Intervals or not, we will use the implemented logic to upgrade the `IPriceOracle` within `LetterOfCredit`.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Anvil Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/anvil-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

