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
solodit_id: 41230
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#8-lack-of-upper-limit-validation
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

Lack of Upper Limit Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [constructor](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondCurve.sol#L59) of the `CSBondCurve` contract. While there is a check to ensure the maximum curve length is not below a minimum threshold, there is no upper limit enforced for the maximum curve length. This lack of upper-limit validation could potentially lead to excessively long bond curves being created.

The issue is classified as **Low** severity because it primarily affects the potential efficiency and operability of the contract rather than posing a direct security risk.

##### Recommendation
We recommend introducing a reasonable upper limit for the maximum curve length during the initialization of the contract.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#8-lack-of-upper-limit-validation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

