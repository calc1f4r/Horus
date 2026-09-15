---
# Core Classification
protocol: KittenSwap_2025-05-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58159
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Inconsistent `VotingEscrow` implementation in `balanceOfNFT()` methods

### Overview


This bug report talks about an issue in a software code that has not been fixed yet. The issue is related to a function called `balanceOfNFT` which is used to protect against flash-loans. However, this protection is not consistently applied to two other functions called `balanceOfNFTAt` and `_balanceOfNFT`. The recommendation is to keep the consistency in the code and remove the check if it is no longer in use.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

This is an unfixed issue in the forked repo ([link](https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf), 5.3.9 Inconsistent between balanceOfNFT, balanceOfNFTAt and \_balanceOfNFT functions).

> The `balanceOfNFT` function implements a flash-loan protection that returns zero voting balance if
> `ownershipChange[_tokenId] == block.number`. However, this was not consistently applied to the `balanceOfNFTAt` and `_balanceOfNFT` functions.

## Recommendations

Keep the consistency. It seems like the check is no longer in use, if so, remove it from the codebase.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-05-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

