---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27197
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
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
  - Guardian Audits
---

## Vulnerability Title

OCL-2 | Chainlink Feed Validation

### Overview


This bug report is about ensuring that the data from the Chainlink price feed is up to date and correct. This is important because the price from the data feed influences the execution of orders and liquidations. The recommendation is to add two require statements to validate the price feed. These statements are “require(answeredInRound >= roundID, “Chainlink:: Stale price”)” and “require(timestamp > 0, “Chainlink:: Round not complete”)”. The GMX team acknowledged the recommendation.

### Original Finding Content

**Description**

Extra validation checks should be added on the result from the Chainlink price feed to ensure non-stale data. The price from the data feed influences the execution of orders and liquidations so it is imperative the data is up to date and correct. 

**Recommendation**

Add the following require statements to validate the price feed:
- `require(answeredInRound >= roundID, "Chainlink:: Stale price")`
- `require(timestamp > 0, "Chainlink:: Round not complete")`

**Resolution**

GMX Team: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

