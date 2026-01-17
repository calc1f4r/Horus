---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 745
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest
source_link: https://code4rena.com/reports/2021-09-bvecvx
github_link: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/57

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - tabish
---

## Vulnerability Title

[L-06] Missing slippage/min-return check in veCVXStrategy

### Overview

See description below for full details.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details
The contracts are missing slippage checks which can lead to being vulnerable to sandwich attacks.

> A common attack in DeFi is the sandwich attack. Upon observing a trade of asset X for asset Y, an attacker frontruns the victim trade by also buying asset Y, lets the victim execute the trade, and then backruns (executes after) the victim by trading back the amount gained in the first trade. Intuitively, one uses the knowledge that someone’s going to buy an asset, and that this trade will increase its price, to make a profit. The attacker’s plan is to buy this asset cheap, let the victim buy at an increased price, and then sell the received amount again at a higher price afterwards.

See `veCVXStrategy._swapcvxCRVToWant`:
```solidity
IUniswapRouterV2(SUSHI_ROUTER).swapExactTokensForTokens(
    toSwap,
    0, // @audit min. return of zero, no slippage check
    path,
    address(this),
    now
);
```

## Impact
Trades can happen at a bad price and lead to receiving fewer tokens than at a fair market price. The attacker's profit is the protocol's loss.

## Recommended Mitigation Steps
Add minimum return amount checks.
Accept a function parameter that can be chosen by the transaction sender, then check that the actually received amount is above this parameter.

Alternatively, check if it's feasible to send these transactions directly to a miner such that they are not visible in the public mempool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | cmichel, tabish |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-bvecvx
- **GitHub**: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/57
- **Contest**: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest

### Keywords for Search

`vulnerability`

