---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34275
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#6-missing-validations-for-non-zero-mintamount-borrowamount-and-repayamount
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

Missing validations for non-zero `mintAmount`, `borrowAmount` and `repayAmount`

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the current codebase, validations ensuring that `mintAmount`, `borrowAmount` and `repayAmount` are greater than zero are absent in the `iToken.mint`,`iToken.borrow`, `iToken.repayBorrow` functions respectively.

These missing checks can lead to unintended consequences, such as misleading event emissions or and registering empty collateral or borrow assets to users.

Related code:
- `mintInternal` https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/TokenBase/Base.sol#L179
- `borrowInternal` https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/TokenBase/Base.sol#L261
- `repayInternal` https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/TokenBase/Base.sol#L299
##### Recommendation
We recommend inserting validation checks ensuring that the amounts are greater than zero to the following functions: `Base.borrowInternal`, `Base.repayInternal`, `Base.mintInternal`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#6-missing-validations-for-non-zero-mintamount-borrowamount-and-repayamount
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

