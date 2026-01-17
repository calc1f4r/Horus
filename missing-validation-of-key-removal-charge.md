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
solodit_id: 41228
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#6-missing-validation-of-key-removal-charge
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

Missing Validation of Key Removal Charge

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the function [\_setKeyRemovalCharge](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1674-L1677) of the contract. This function currently allows setting any amount for the key removal charge without enforcing a limit. Without an upper boundary, excessively high charges could be set, potentially creating barriers for node operators needing to remove keys or manage their nodes effectively.

The issue is classified as **Low** severity because while it could lead to operational inefficiencies or financial burdens for Node Operators, it does not directly compromise the contract’s security.

##### Recommendation
We recommend implementing a cap on the key removal charge to ensure it remains within reasonable limits.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#6-missing-validation-of-key-removal-charge
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

