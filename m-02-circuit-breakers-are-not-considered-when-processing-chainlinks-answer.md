---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41675
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Cryptex-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Circuit breakers are not considered when processing Chainlink's answer

### Overview


This bug report discusses a problem with the Chainlink feed, which provides prices for different assets. The report states that due to a circuit breaker, the provided price may be incorrect if the asset's price falls outside the minimum and maximum limits set by Chainlink. This can lead to a misleading price being displayed. The report recommends implementing a check to ensure that the price is always within the limits set by Chainlink.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

Every Chainlink feed has a minimum and maximum price. However, due to the circuit breaker, if an asset's price moves outside these limits, the provided answer will still be capped.

This can lead to an incorrect price if the actual price falls below the aggregator's `minAnswer`, as Chainlink will continue providing the capped value instead of the true one.

The Chainlink documentation notes that "On most data feeds, these values are no longer used and they do not prevent your application from reading the most recent answer.". However, this is not the case on Arbitrum, as for most data feeds (including ETH and most stablecoins), these values are indeed used, for example, the ETH/USD aggregator:
[link](https://arbiscan.io/address/0x3607e46698d218B3a5Cae44bF381475C0a5e2ca7#readContract)

## Recommendations

Consider checking that the price is always between the aggregator's `minAnswer` and `maxAnswer`:

```diff
    function latestPrice(bool checkStaleness) public view virtual override returns (uint256) {
        ...
-       assert(answer > 0);
+       require(answer > MIN_ANSWER && answer < MAX_ANSWER);
        ...
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Cryptex-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

