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
solodit_id: 19210
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

Reentrancy When Closing Perpetuals

### Overview

See description below for full details.

### Original Finding Content

## Description

The function `forceClosePerpetuals()` can be run when the quantity of funds being hedged by hedging agents has breached the `limitHAHedge`. This case occurs when enough users burn stablecoins, which may result in the hedging agents overcompensating for the remaining stablecoins.

When a perpetual is force closed, there is an external call through `_secureTransfer()` on line [315], which will call `transferFrom()` on the collateral token. The `forceClosePerpetuals()` continues to perform calculations after the external call based off a combination of variables stored in state and memory, thus opening up a potential reentrancy vector.

Exploiting this reentrancy vector allows an attacker to bypass the `estimatedCost` and `keeperFeesClosingCap` limits. These limits prevent users from earning more in fees than the cost of performing a flashloan attack.

The reentrancy attack can be performed by reentering `forceClosePerpetuals()` multiple times, which creates parallel executions of cashing out the perpetuals. These parallel executions split the amount of `cashOutFees` over each execution without changing the value for `estimatedCost`, thus avoiding the limits to the fees earned.

For this reentrancy to be viable, the collateral ERC20 token must allow the attacker to gain control of execution during `transferFrom()`. Most ERC20 tokens do not relinquish control of execution to a user; however, some do. One example is the ERC777 extension, which performs an execution call to the `to` address, alerting the user that the funds have been transferred. An attacker could use this call to gain control of the execution and reenter `forceClosePerpetuals()`.

## Recommendations

We recommend performing all external calls after all calculations have been performed in accordance with the Checks-Effects-Interactions pattern.

This can be achieved by storing the `(owner, netCashOutAmount)` variables in an array and iterating through this array, calling `_secureTransfer()` after all calculations have been performed.

## Resolution

The recommendation has been implemented in PR #123, which stores the `owner` and `netCashOutAmount` in an array. The external transfer is then executed after all calculations and state modifications are complete.

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

