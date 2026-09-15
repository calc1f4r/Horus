---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49445
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#5-wrong-ltv-calculation-for-duplicate-assets
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
  - MixBytes
---

## Vulnerability Title

Wrong LTV calculation for duplicate assets

### Overview


The bug report is about a problem with the `Repository.newLendingPool()` function, where if a manager passes two of the same assets, it will create a pool with the wrong number of assets and the Loan-to-Value (LTV) calculation will be incorrect. This can result in users losing their funds. The recommendation is to check for unique asset addresses when creating a pool to avoid this issue.

### Original Finding Content

##### Description
If a manager passes two identical assets when calling `Repository.newLendingPool()`, the pool will be created with an incorrect asset count, and the Loan-to-Value (LTV) calculation will be incorrect, potentially leading to user funds loss.
##### Recommendation
We recommend checking for unique asset addresses when creating the pool.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#5-wrong-ltv-calculation-for-duplicate-assets
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

