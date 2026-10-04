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
solodit_id: 41399
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

[M-03] `mintGTToAddress()` in ERC20DAO doesn't check `distributionAmount` limit

### Overview


The bug report discusses an issue with the `mintGTToAddress()` function in the ERC721 and Factory contract. This function does not have a limit on the amount of tokens that can be created, which could allow administrators to create an unlimited number of tokens. The severity of this bug is considered medium, and it is recommended that the `distributionAmount` limit is checked in the `mintGTToAddress()` function in the ERC20DAO.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

While `mintGTToAddress()` in ERC721 and Factory contract check for `distributionAmount` limit the ERC20DAO doesn't check for `distributionAmount` limit and it would be possible for admins to mint unlimited amount of tokens.

## Recommendations

Check for `distributionAmount` in `mintGTToAddress()` in ERC20DAO.

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

