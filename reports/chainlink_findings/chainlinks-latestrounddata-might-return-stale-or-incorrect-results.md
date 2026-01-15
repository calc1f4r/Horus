---
# Core Classification
protocol: Aarna
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37172
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
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
  - Zokyo
---

## Vulnerability Title

Chainlink’s latestRoundData might return stale or incorrect results

### Overview


The report discusses an issue in the AFiStorage contract where the checkIfUSDC function retrieves price data from a Chainlink oracle, but there is a risk that the data may be incorrect or outdated. This could lead to inaccurate prices. The recommendation is to add checks to compare the returned data to a staleness threshold and to track heartbeat intervals for each token. The issue has been resolved by adding these checks in the getPriceAndDecimals function.

### Original Finding Content

**Severity**: Medium

**Status**:  Resolved

 **Description**
 
The checkIfUSDC function in the AFiStorage contract retrieves price data from a Chainlink oracle by calling latestRoundData. However, there's a risk that this data may be stale or incorrect due to various reasons related to Chainlink oracles. There is no check if the return value indicates stale data. This could lead to stale prices according to the Chainlink documentation:
https://docs.chain.link/docs/historical-price-data/#historical-rounds


**Recommendation**: 

Check the updatedAt parameter returned from latestRoundData() and compare it to a staleness threshold. Consider introducing a mapping for tracking heartbeat intervals for each allowlisted token. 

**Fix**: Recommended checks have been added in the getPriceAndDecimals function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Aarna |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

