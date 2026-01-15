---
# Core Classification
protocol: SXT_2025-03-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63323
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-04] Missing check for max/min price from chainlink

### Overview

See description below for full details.

### Original Finding Content


In function `_validatePriceFeed`, we will fetch the price from the chainlink aggreagator. In chainlink, there is one min/max answer. In some edge cases, the returned value may not the actual price, e.g. return min answer if the actual price is less than min answer.


```solidity
    function _validatePriceFeed(PaymentAsset memory paymentAsset) internal view {
        if (paymentAsset.priceFeed == NATIVE_ADDRESS || !Utils.isContract(paymentAsset.priceFeed)) {
            revert InvalidPriceFeed();
        }
        (, int256 answer,, uint256 updatedAt,) = AggregatorV3Interface(paymentAsset.priceFeed).latestRoundData();

        if (answer == 0) {
            revert InvalidPriceFeed();
        }

        // slither-disable-next-line timestamp
        if (updatedAt + paymentAsset.stalePriceThresholdInSeconds < block.timestamp) {
            revert InvalidPriceFeed();
        }
    }
```

Checking https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits, we need to set one reasonable min/max value for in-scope token. If the return price reaches our set min/max value, we should revert here to avoid using the stale price.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | SXT_2025-03-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

