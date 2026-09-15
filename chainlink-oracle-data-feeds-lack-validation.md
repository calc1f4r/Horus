---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19394
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Chainlink Oracle Data Feeds Lack Validation

### Overview


This bug report concerns Chainlink oracle data feeds, which lack validation to ensure that the data is fresh and from a complete round. Without this validation, the protocol may be put at risk of liquidation events or insolvency. To mitigate this issue, the development team implemented a series of checks to validate the output of Chainlink's latestRoundData() function. This commit is 59d9e0c and the checks are implemented within _checkAnswer(). These checks must be added to all cases where latestRoundData() is used. This issue is now resolved.

### Original Finding Content

## Description

Chainink oracle data feeds lack validation to ensure that the data is fresh and from a complete round. Oracle malfunctions may lead to large scale liquidation events or alternatively it may put the protocol at risk of insolvency.

## Recommendations
Validate the output of Chainlink’s `latestRoundData()` function to match the following code snippet:

```solidity
(
    uint80 roundID,
    int256 price,
    ,
    uint256 updateTime,
    uint80 answeredInRound
) = AggregatorV3Interface(priceFeeds[token]).latestRoundData();

require(
    answeredInRound >= roundID,
    "Chainlink Price Stale"
);
require(price > 0, "Chainlink Malfunction");
require(updateTime != 0, "Incomplete round");
```

It is important that these checks are added to all cases where `latestRoundData()` is used.

## Resolution

The development team mitigated the issue in commit `59d9e0c` implementing the recommendations above. Several checks are implemented within `_checkAnswer()`, which is called on the outputs of `AggregatorV3Interface.latestRoundData()` wherever it is called.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

