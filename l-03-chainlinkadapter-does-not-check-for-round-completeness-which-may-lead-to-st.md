---
# Core Classification
protocol: Fyde
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31712
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
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

[L-03] ChainlinkAdapter does not check for round completeness, which may lead to stale data

### Overview

See description below for full details.

### Original Finding Content

When querying the results from `latestRoundData()`, round completeness is not validated. Not checking for round completeness could lead to stale prices and wrong price return value, or outdated price.

```
    try FeedRegistryInterface(clRegistry).latestRoundData(asset, clQuoteToken) returns (
      uint80, int256 clPrice, uint256, uint256 updatedAt, uint80
    ) {
```

Validate the data feed for round completeness for all the functions that call `latestRoundData()`.

```
    try FeedRegistryInterface(clRegistry).latestRoundData(asset, clQuoteToken) returns (
+     uint80 roundID, int256 clPrice, uint256, uint256 updatedAt, uint80 answeredInRound
    ) {
+   require(answeredInRound >= roundID, "round not complete");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

