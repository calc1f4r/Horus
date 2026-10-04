---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36213
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#2-change-the-access-role-name-for-the-secondopinionoracle-function
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
  - MixBytes
---

## Vulnerability Title

Change the access role name for the `secondOpinionOracle` function

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is a `setOracleReportLimits` function at the [following line](https://github.com/lidofinance/core/blob/efeff81c18f85451ebf98e8fd8bb78b8eb0095f6/contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol#L269). It has a restricted access only for the `ALL_LIMITS_MANAGER_ROLE` role. This function also allows setting the `secondOpinionOracle` address.

##### Recommendation
We recommend changing the role name for the `setOracleReportLimits` function to reflect all allowed actions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#2-change-the-access-role-name-for-the-secondopinionoracle-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

