---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53694
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
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

Operator Can Continue To Utilize The Protocol After Being Liquidated

### Overview


The report discusses a bug in the SDUtilityPool where certain functions do not have proper checks in place to prevent operators with low health factor or those who have already been liquidated from utilizing the pool. This could lead to protocol insolvency and funds getting stuck in the contract during the claim process. The recommended solution is to implement checks in the affected functions to ensure that the operator is not already liquidated and has a healthy health factor. The bug has been resolved in a recent commit.

### Original Finding Content

## Description

In the SDUtilityPool, the functions `utilize()` and `utilizeWhileAddingKeys()` lack necessary checks to verify the operator’s current status. As a result, operators who have already been liquidated, or those with an unhealthy health factor, are still able to call these functions to further utilize from the pool.

A significant concern arises when an operator, having already undergone liquidation, continues to operate even if their health factor deteriorates to an unhealthy level. The system’s current logic prevents an account from being liquidated more than once, preventing operators from subsequent liquidations, regardless of their health factor status. This could potentially lead to protocol insolvency.

Additionally, this issue has a cascading effect on the `OperatorRewardsCollector.withdrawableInEth()` function. An unhealthy health factor could trigger a revert due to an underflow issue on line [71] of `OperatorRewardsCollector`. This underflow results in funds getting stuck in the contract during the claim process.

## Recommendations

Implement checks within `utilize()` and `utilizeWhileAddingKeys()` functions to ensure that:
- The operator has not been already liquidated.
- The health factor is above the liquidation threshold.

## Resolution

Validation was added to `_utilize()` to check that the operator has not been already liquidated and has a good health factor.

`OperatorRewardsCollector.withdrawableInEth()` now returns 0 if there isn’t enough collateral to cover total SD interest and open liquidations.

This issue has been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf

### Keywords for Search

`vulnerability`

