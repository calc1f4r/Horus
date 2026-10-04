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
solodit_id: 41401
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

[M-05] Cross-chain deployments failure

### Overview


This bug report discusses an issue with creating cross-chain DAO deployment messages. Currently, the code divides the total ETH amount equally between cross-chain messages, but different destination chains may require different cross-chain fees. The recommendation is to allow users to specify the bridge fee amount for each cross-chain message, instead of having to pay based on the maximum bridge fee amount. This will improve the functionality and usability of the code.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When code wants to create cross-chain DAO deployment message it divides the total ETH amount equally between cross-chain messages. The issue is that different destination chains may require different cross-chain fee. Code should allow user to specify bridge fee amount for each cross-chain message. In the current design user have to pay based on maximum bridge fee amount.

## Recommendations

Allow user to specify cross-chain bridge fee amounts for each chain.

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

