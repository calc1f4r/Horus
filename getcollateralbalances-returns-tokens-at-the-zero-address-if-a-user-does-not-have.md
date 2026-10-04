---
# Core Classification
protocol: Term Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53738
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/term-finance/term1/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/term-finance/term1/review.pdf
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

getCollateralBalances() returns tokens at the zero address if a user does not have a balance in a collateral token

### Overview


The function `TermRepoCollateralManager.getCollateralBalances()` returns the zero address as the token address if a user does not have a balance in a given token. This causes an error when rollover bids are made. The issue occurs because the function sets the length of the returned arrays based on the number of collateral tokens, even if the user does not have a balance in some of them. To fix this, the length of the arrays should be dynamically set or all token addresses should be returned with zero balances. The issue has been resolved in the latest version of the code.

### Original Finding Content

## Description

The function `TermRepoCollateralManager.getCollateralBalances()` returns the zero address as the token address if a user does not have a balance in a given token. This causes rollover bids to fail as `TermAuctionBidLocker._isInInitialCollateralShortFall()` loops through all of the tokens returned and calls `termPriceOracle.usdValueOfTokens()` for each one. This call reverts when called with the zero address as the token’s address.

This issue occurs because the return values of `TermRepoCollateralManager.getCollateralBalances()` are set to arrays of length `collateralTokens.length` on line [543] but the token addresses are assigned to these arrays conditionally on whether the user has collateral on line [555]. Therefore, tokens with no collateral remain as the contents of memory.

## Recommendations

Either dynamically set the length of the returned arrays after determining how many token balances will be returned, or else return all token addresses, with zero balances where appropriate, and handle this returned data accordingly.

## Resolution

Based on a retest of commit `e883f0e`, the issue has been resolved - `TermAuctionBidLocker._isInInitialCollateralShortFall()` now has a check to omit zero balances of collateral tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Term Finance |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/term-finance/term1/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/term-finance/term1/review.pdf

### Keywords for Search

`vulnerability`

