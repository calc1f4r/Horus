---
# Core Classification
protocol: Ipnft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20602
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-IPNFT.md
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
  - Pashov
---

## Vulnerability Title

[M-02] Insufficient input validation in `CrowdSale` configuration

### Overview


This bug report describes two flaws in the configuration validation of a new CrowdSale. It is possible to create a never ending Sale if the closingTime field does not have a max value check, and a never ending lock or a 0 duration lock can be used in VestedCrowdSale if the cliff argument of startSale is not validated. This could result in almost permanently locked tokens, which would be a value loss for users. The likelihood of this happening is low, as it requires a fat-finger or a big configuration error. However, the impact is high, making it a serious issue.

The recommended solution is to add proper min & max value bounds for both the closingTime and cliff parameters. This will help to prevent the issue from occurring in the future.

### Original Finding Content

**Impact:**
High, as it can lock up valuable tokens almost permanently

**Likelihood:**
Low, as it requires a fat-finger or a big configuration error

**Description**

There are two flaws in the configuration validation of a new `CrowdSale`. It is currently possible to create a never ending `Sale` as the `closingTime` field does not have a max value check. It is also possible that a never ending lock or a 0 duration lock is used in `VestedCrowdSale` as the `cliff` argument of `startSale` is not validated as in `StakedVestedCrowdSale::startSale`. Both can result in almost permanently locked tokens which is a value loss for users.

**Recommendations**

Add proper min & max value bounds for both `closingTime` and `cliff` parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ipnft |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-IPNFT.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

