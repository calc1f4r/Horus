---
# Core Classification
protocol: Treehouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38564
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
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

Future Liquid Staking Token Additions

### Overview

See description below for full details.

### Original Finding Content

## Description

The Treehouse team has outlined that future updates will likely include support for different Liquid Staking Tokens (LSTs). Each LST is designed by a different team and thus takes different approaches to accounting and profit distribution. These different approaches can make integrating multiple LSTs a challenging process. For example, Origin's OETH only receives staking rewards if the smart contract holding it opts in.

## Recommendations

Careful research must be undertaken when expanding the current system to include other LSTs. It is recommended to check new integrations thoroughly with the token's developers to ensure all existing systems remain suitable.

## Resolution

The issue was acknowledged by the project team.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Treehouse |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf

### Keywords for Search

`vulnerability`

