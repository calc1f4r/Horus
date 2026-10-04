---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19218
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
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

The total supply of GhoVariableDebtToken is incorrect if there are active discounts

### Overview

See description below for full details.

### Original Finding Content

## Description

Openzeppelin’s description of the `totalSupply()` function, inherited in `GhoVariableDebtToken.sol`, reads:

> @dev Returns the amount of tokens in existence.

However, this is not quite what `GhoVariableDebtToken.totalSupply()` will do. `GhoVariableDebtToken.balanceOf()` contains logic to reduce a user’s debt token balance if that user has an interest discount from staked AAVE. However, this logic is (understandably) missing from `GhoVariableDebtToken.totalSupply()`.

As a result of this, the sum of all balances of all users will be less than the value returned by `GhoVariableDebtToken.totalSupply()`. This could potentially have security implications if any smart contract references the value of `GhoVariableDebtToken.totalSupply()` in its logic. It could also have broader financial implications if the value of `GhoVariableDebtToken.totalSupply()` is ever used in a financial estimate or report. If the difference is significant, this could potentially compromise the reputation of the protocol.

This issue is partially mitigated by the fact that `GhoVariableDebtToken` is not a tradeable token. It is also mitigated by the fact that discounts will be applied to the total supply whenever actions are taken that call `_mintScaled()` or `_burnScaled()`. There is nothing in the system, however, which prevents a holder of a large sum of `GhoVariableDebtToken` with a high discount from simply holding those tokens for a large period of time, creating a significant inaccuracy. 

Consider that the value of `GhoVariableDebtToken.totalSupply()` is not a technical detail. It does have a financial meaning: the total GHO due to be repaid, and so an error in this value could realistically be consequential.

## Recommendations

The logic changes required to make the value of `GhoVariableDebtToken.totalSupply()` precisely account for all discounts would not be trivial. The testing team suggests that a multiplier could be maintained which reflects the global discount of the entire balance of `GhoVariableDebtToken`. This would need to be updated whenever discounts or user balances of `GhoVariableDebtToken` change. Whenever the multiplier changed, it would also be necessary to apply the previous multiplier to the balance since the last change and record this new balance.

Alternatively, if the development team considers such measures unnecessary, communicate wherever possible that the value of `GhoVariableDebtToken.totalSupply()` will be an overestimate.

## Resolution

The development team has acknowledged this issue as a limitation of the current implementation. The function comment header has been changed to reflect this in commit `ae9704e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf

### Keywords for Search

`vulnerability`

