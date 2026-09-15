---
# Core Classification
protocol: Compound Open Price Feed – Uniswap Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11388
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
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
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L02] Immature time-weighted average prices could be used as anchors

### Overview

See description below for full details.

### Original Finding Content

The mechanism implemented to use time-weighted average prices from Uniswap markets as anchors works as expected under the assumption that sufficient time will pass (at least [`anchorPeriod`](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L31) seconds) between the contract’s deployment and the first time a price is posted by the reporter. Yet it must be noted that this restriction is never programmatically enforced. The `UniswapAnchoredView` contract allows the reporter to post prices as soon as the contract is deployed, which could lead to using time-weighted average prices calculated over dangerously short periods of time.


Even though the described assumption is correctly stated and acknowledged by the Compound team in the external specification provided during the audit, the code base lacks documentation highlighting it. Moreover, the scenario is not being tested in the contract’s test suite.


To favor explicitness, consider adding the necessary logic to prevent prices from being posted before enough time passes since deployment. Alternatively, should this suggestion not be viable in terms of gas costs, consider at least explicitly documenting the assumption in the contract, and adding related unit tests.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Open Price Feed – Uniswap Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

