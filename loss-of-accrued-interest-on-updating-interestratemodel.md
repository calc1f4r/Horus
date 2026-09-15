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
solodit_id: 49446
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#6-loss-of-accrued-interest-on-updating-interestratemodel
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

Loss of accrued interest on updating InterestRateModel

### Overview


The report is about a bug that occurs when the "InterestRateModel" is changed for the "LendingPool" in the "Repository". This results in the function "LendingPool._accrueInterest()" not being called automatically, which can cause a loss of accrued interest for both borrowers and suppliers. The recommendation is to accrue interest for the old "InterestRateModel" before updating it.

### Original Finding Content

##### Description
When the `InterestRateModel` is changed for the `LendingPool` in the `Repository`, `LendingPool._accrueInterest()` is not automatically called, which could lead to a loss of accrued interest for both borrowers and suppliers.
##### Recommendation
We recommend accruing interest for the old `InterestRateModel` before updating it.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#6-loss-of-accrued-interest-on-updating-interestratemodel
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

