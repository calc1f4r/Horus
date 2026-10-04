---
# Core Classification
protocol: Angle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19205
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
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

Purchase of Zero Tokens from BondingCurve

### Overview

See description below for full details.

### Original Finding Content

## Description

Tokens can be bought from the BondingCurve contract through the function `buySoldTokens()`, which exchanges a stablecoin token for another ERC20 token. The contract allows users to pass zero (0) as the `targetSoldTokenQuantity` to the function. This will likely later fail the condition `require(amountToPayInAgToken > 0)` since the cost of zero tokens should also be zero.

## Recommendations

Consider adding an additional check to prevent users from attempting to buy zero tokens.

## Resolution

This issue has been resolved in commit `2848add` by adding a check to ensure `targetSoldTokenQuantity` is greater than zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Angle |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf

### Keywords for Search

`vulnerability`

