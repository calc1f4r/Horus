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
solodit_id: 41229
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#7-redundant-function-definition
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

Redundant Function Definition

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [\_getClaimableBondShares](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondCore.sol#L275-L279) function of the `CSBondCore` contract. This function is redundant as it is overridden in the `CSAccounting` contract, suggesting that its definition in the current context might be unnecessary. This redundancy could lead to confusion and potential maintenance issues, as developers might overlook which version of the function is being called in different contexts.

The issue is classified as **Low** severity because it primarily affects the clarity and maintainability of the code rather than its functionality or security.

##### Recommendation
We recommend removing the `_getClaimableBondShares` function from the current contract to streamline the codebase and avoid confusion.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#7-redundant-function-definition
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

