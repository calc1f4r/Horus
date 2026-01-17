---
# Core Classification
protocol: Compound Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11836
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Truncation-Related Issues

### Overview

See description below for full details.

### Original Finding Content

Throughout the compound contracts, truncation issues inherent to EVM operation result in some relatively unavoidable errors. These errors exist when minting cTokens, when redeeming cTokens for their underlying assets, and when liquidating another user’s loan.


In the case of minting, the `CToken.mintFresh` function [calls `divScalarByExpTruncate`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L724) to determine the number of cTokens the user will receive given their input of a certain number of underlying tokens. The result will be truncated if it is calculated to be some non-integer number of cToken units.


In the case of redeeming, the `CToken.redeemFresh` function also [calls `divScalarByExpTruncate`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L855). The number of tokens to redeem will similarly be truncated to the next lowest integer value of underlying token units.


Finally, the `Comptroller.liquidateCalculateSeizeTokens` function [calls `mulScalarTruncate`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/Comptroller.sol#L767). If the amount repaid is sufficiently small, the result will be rounded down to the next nearest integer value of indivisible token units.


In all cases, the user receives less than they theoretically should (either in terms of cTokens, or in terms of underlying tokens). However, the loss should never be more than 1 indivisible unit of whatever token the user is receiving. Even in the case of wBTC, where 1 indivisible unit is worth the most out of any other token involved, the loss is only roughly 1% of a USD cent (at time of writing). This issue, unlike the issue of interest-free loans, does not hurt the protocol. Instead, the users take the brunt of the (very small) loss.


It should be pointed out that extremely small loans that are able to be liquidated may not actually be liquidated, since truncation could cause the liquidator to receive nothing, or far less than they’d theoretically receive. However, loans that are not liquidated because of this will eventually accrue enough interest that they can be profitably liquidated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

