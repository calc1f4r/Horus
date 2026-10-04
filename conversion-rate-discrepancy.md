---
# Core Classification
protocol: Plume Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53275
audit_firm: OtterSec
contest_link: https://plumenetwork.xyz/
source_link: https://plumenetwork.xyz/
github_link: https://github.com/plumenetwork/contracts

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
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Conversion Rate Discrepancy

### Overview


This bug report discusses a potential issue with the conversion rate between assets and shares in the YieldToken contract. This may cause problems with the mint and withdraw functions, resulting in rejected requests due to changes in the conversion rate. The suggested solution is to record the conversion rate at the time of the request and use that fixed rate during the execution of the functions. This issue has been resolved in the 4f16028 patch.

### Original Finding Content

## Discrepancy Between Assets and Shares

A discrepancy between assets and shares may occur due to potential changes in the conversion rate between the request time and processing time during `YieldToken::mint` or `YieldToken::withdraw`. This may result in the functions reverting if the conversion result exceeds the requested value. Thus, valid mint or withdrawal requests may be rejected simply due to conversion rate changes.

## Remediation

Record the `convertToAssets` or `convertToShares` value at request time and utilize the fixed rate during the execution of `mint` or `withdraw`.

## Patch

Resolved in 4f16028.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Plume Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://plumenetwork.xyz/
- **GitHub**: https://github.com/plumenetwork/contracts
- **Contest**: https://plumenetwork.xyz/

### Keywords for Search

`vulnerability`

