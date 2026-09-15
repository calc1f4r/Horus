---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53631
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
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

Variable stakedButUnverifiedNativeETH Is Never Decremented

### Overview


The bug report states that there is an issue with the variable `stakedButUnverifiedNativeETH` in the `NodeDelegator` function. This variable is supposed to track the amount of native ETH staked through EigenLayer, but it is not being accurately accounted for. This can cause the price of `rsETH` to be incorrect, leading to significant losses for the protocol. The recommendation is to fix the accounting of `stakedButUnverifiedNativeETH` by decrementing its value when ETH is unstaked. The issue has been resolved by the development team in commit `7db0e43`.

### Original Finding Content

## Description

The incorrect accounting of variable `stakedButUnverifiedNativeETH` may cause inaccurate `rsETH` price.

Variable `stakedButUnverifiedNativeETH` in `NodeDelegator` is meant to track the amount of native ETH staked through EigenLayer. As a result, it is incremented when the function `stake32Eth()` is called. However, when a `NodeDelegator` withdraws ETH using functions `initiateNativeEthWithdrawBeforeRestaking()` and `claimNativeEthWithdraw()`, it is not decremented.

When the unstaked Ether is then sent to a user who wishes to withdraw, the Ether will still be counted towards the total assets of the protocol even though it is no longer a part of the protocol. This results in the price of `rsETH` being higher than it should be. When users withdraw assets at this inflated `rsETH` price, the protocol will suffer significant losses.

## Recommendations

Decrement the value of `stakedButUnverifiedNativeETH` when the Ether is unstaked to ensure the accounting of assets is accurate at all times.

## Resolution

The development team has mitigated this issue by fixing the accounting of `stakedButUnverifiedNativeETH`, as per commit `7db0e43`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf

### Keywords for Search

`vulnerability`

