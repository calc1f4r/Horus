---
# Core Classification
protocol: Eigen Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36030
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
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

Incorrect Use Of EIP-712

### Overview

See description below for full details.

### Original Finding Content

## Description

In `DelegationManagerStorage`, the `DelegationApproval` and `OperatorAVSRegistration` EIP-712 types are missing the `delegationApprover` and `salt` members respectively, causing the `DELEGATION_APPROVAL_TYPEHASH` and `OPERATOR_AVS_REGISTRATION_TYPEHASH` to be incorrectly defined. This results in integration failures with wallets and other software that support EIP-712.

## Recommendations

Add the required members to their respective data types.

## Resolution

`OPERATOR_AVS_REGISTRATION_TYPEHASH` has been moved to the `AVSDirectoryStorage` contract. This issue has been addressed in PR #435.

---

## EigenLayer Detailed Findings

## EGN3-04 Missing Call To _disableInitializers() In Proxy Contract Implementation

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Eigen Layer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-3/review.pdf

### Keywords for Search

`vulnerability`

