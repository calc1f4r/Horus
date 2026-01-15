---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41410
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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

[M-14] ERC721 max token per user limit can always be bypassed by one

### Overview


The report describes a bug in the `ERC721DAO` smart contract that affects the `transferFrom()` and `safeTransferFrom()` functions. These functions have an error that allows users to have more tokens than they should. This is inconsistent with the limit validation in the `mintToken()` function. The bug can be fixed by making a small change to the code in both `transferFrom()` and `safeTransferFrom()` functions. This change will ensure that users cannot have more tokens than the limit set by the DAO. The bug is low in severity but has a high likelihood of occurring.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

Both `transferFrom()` and `safeTransferFrom()` functions in `ERC721DAO` have an off-by-one error when calculating the max amount of tokens a user can have:

```solidity
require(balanceOf(to) <= erc721DaoDetails.maxTokensPerUser);
```

This is also inconsistent with the limit validation performed in `mintToken()`, where it is applied correctly.

This leads to users being able to have more tokens than they should. For example, a DAO that would like to limit their tokens to one per user would allow them to have two instead.

## Recommendations

Consider making this change to both `transferFrom()` and `safeTransferFrom()`:

```diff
-   require(balanceOf(to) <= erc721DaoDetails.maxTokensPerUser);
+   require(balanceOf(to) < erc721DaoDetails.maxTokensPerUser);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

