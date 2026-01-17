---
# Core Classification
protocol: Growth Defi V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13575
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/12/growth-defi-v1/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - John Mardlin
  - Alexander Wade
---

## Vulnerability Title

Potentially dangerous use of a cached exchange rate from Compound

### Overview


This bug report is about an issue with the `GPortfolioReserveManager.adjustReserve` function, which is used to perform reserve adjustment calculations based on Compound's cached exchange rate values. The problem is that there can be a significant difference between the cached values and the up-to-date values, which can make it difficult to predict the outcome of reserve adjustments.

The recommendation is to use `getExchangeRate()` consistently, or to ensure that `fetchExchangeRate()` is used first and `getExchangeRate()` afterward. This should help to ensure that the reserve adjustment calculations are based on the most up-to-date values, reducing the risk of unexpected outcomes.

### Original Finding Content

#### Description


`GPortfolioReserveManager.adjustReserve` performs reserve adjustment calculations based on Compound’s cached exchange rate values (using `CompoundLendingMarketAbstraction.getExchangeRate()`) then triggers operations on managed tokens based on up-to-date values (using `CompoundLendingMarketAbstraction.fetchExchangeRate()`) . Significant deviation between the cached and up-to-date values may make it difficult to predict the outcome of reserve adjustments.


#### Recommendation


Use `getExchangeRate()` consistently, or ensure `fetchExchangeRate()` is used first, and `getExchangeRate()` afterward.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Growth Defi V1 |
| Report Date | N/A |
| Finders | John Mardlin, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/12/growth-defi-v1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

