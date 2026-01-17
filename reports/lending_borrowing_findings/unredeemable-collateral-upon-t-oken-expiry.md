---
# Core Classification
protocol: DXdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53752
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/dxdao/carrot-kpi/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/dxdao/carrot-kpi/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Unredeemable Collateral Upon T oken Expiry

### Overview

The report describes a bug in the function `redeemCollateral()` which is used by KPI Token holders to redeem their collateral tokens. The bug prevents users from redeeming their tokens if they have registered their redemption intent but do not call `redeemCollateral()` before the token expires. This is due to a check on line [665] which is incorrect and does not allow the contract to be finalized. The testing team recommends removing this check to resolve the issue. The bug has been fixed in commit `82b98e2` by removing the code on line [665]. This will allow users to redeem their collateral tokens even after the contract has expired.

### Original Finding Content

## Description

Function `redeemCollateral()` is callable by a KPI Token holder that has registered their redemption intent and burned their KPI Tokens through the function `registerRedemption()`. The function conducts several checks, including preventing the call when `_isExpired()` is true. This check is potentially incorrect. If the user has called `registerRedemption()` but does not call `redeemCollateral()` before the token expires, they will never be able to redeem their collateral tokens. Another indication that the check on line [665] is incorrect is that the function has a condition where it checks whether the token is expired or not on line [675]. Based on the current implementation, once the contract expires (i.e., when `expired() == Trueholds`), there is no way to finalize the contract.

## Recommendations

The testing team recommends removing the instructions on line [665] to allow the burned token (through function `registerRedemption()`) to be redeemed.

## Resolution

The issue has been fixed on commit `82b98e2`. The code on line [665] was removed such that users can redeem their collateral tokens after the contract expires.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | DXdao |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/dxdao/carrot-kpi/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/dxdao/carrot-kpi/review.pdf

### Keywords for Search

`vulnerability`

