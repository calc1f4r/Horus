---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19221
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

GhoFlashMinter free borrowers could resell their privileges

### Overview

See description below for full details.

### Original Finding Content

## Description
GhoFlashMinter allows addresses to flash loan GHO with no fee if `_aclManager.isFlashBorrower()` returns true for that address. It would be possible for an address granted this status to simply resell the ability to make these loans at a discount from the main protocol’s fee and keep the fees themselves.

## Recommendations
Be aware of this issue, especially when granting borrower status via `_aclManager.isFlashBorrower()`.

## Resolution
The development team are aware of the issue and have provided the following comments. Only Aave governance can assign this privilege to addresses and likely would not assign this privilege to an address that would resell it, or would revoke this privilege if reselling was observed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf

### Keywords for Search

`vulnerability`

