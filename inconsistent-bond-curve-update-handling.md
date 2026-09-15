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
solodit_id: 41213
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#1-inconsistent-bond-curve-update-handling
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

Inconsistent Bond Curve Update Handling

### Overview


The bug report describes an issue in the function "updateBondCurve" of the "CSAccounting" contract. This issue can cause inconsistencies in the system and potentially lead to deposits without proper bond. To fix this, it is recommended to update the bond curve in a 2-step process to ensure that all keys are updated simultaneously. The severity of this issue is classified as medium.

### Original Finding Content

##### Description
The issue is identified within the function [updateBondCurve](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSAccounting.sol#L168-L173) of contract `CSAccounting`. When updating a bond curve, there is a potential issue where the unbonded validators amount increases for a specific NO (node operator), but the corresponding depositable amount is not updated accordingly. This inconsistency can lead to unexpected behavior in the system, as the depositable amount should be forced to update, but currently, it is not possible to enforce this.

The issue is classified as **Medium** severity because it can result in inconsistencies within the contract's logic, potentially leading to deposits of NO's keys without appropriate bond.

##### Recommendation
We recommend conducting bond curve update in a 2-step way, when NO's curve Id is updated on any action of this NO which will guarantee that unbonded keys and depositable keys update simultaneously.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#1-inconsistent-bond-curve-update-handling
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

