---
# Core Classification
protocol: Synthetix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19668
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Improper Supply Cap Limitation Enforcement

### Overview


This bug report deals with the openLoan() function of the EtherCollateral contract. The current function does not check if the loan to be issued will result in the supply cap being exceeded. A require statement was added to the openLoan() function to prevent the total cap from being exceeded by the loan to be opened. This recommendation was implemented by the development team and has resolved the issue.

### Original Finding Content

## Description

The `openLoan()` function does not check if the loan to be issued will result in the supply cap being exceeded. Indeed, line [251] only enforces that the supply cap is not reached before the loan is opened. As a result, any account can create a loan that exceeds the maximum amount of sETH that can be issued by the EtherCollateral contract.

## Recommendations

Introduce a `require` statement in the `openLoan()` function to prevent the total cap from being exceeded by the loan to be opened.

## Resolution

The recommendation above was implemented by the development team.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Synthetix |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf

### Keywords for Search

`vulnerability`

