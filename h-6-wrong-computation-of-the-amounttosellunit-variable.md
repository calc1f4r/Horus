---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19135
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/535

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
  - wrong_math

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - qpzm
  - innertia
  - toshii
  - Nyx
  - WATCHPUG
---

## Vulnerability Title

H-6: Wrong computation of the amountToSellUnit variable

### Overview


This bug report is about the incorrect computation of the `amountToSellUnits` variable in the `BuyUSSDSellCollateral()` function in the `USSDRebalancer.sol` contract. The `amountToSellUnits` variable is used to sell an amount of collateral during a peg-down recovery event which should be equivalent (in USD) to the ratio of `amountToBuyLeftUSD / collateralval`. However, the code is written incorrectly which will lead to an incorrect amount of collateral to be sold. The incorrect code is found at line 121 of the `USSDRebalancer.sol` contract. The bug was found by 0xRobocop, 0xlmanini, Aymen0909, Bahurum, Bauer, Juntao, Nyx, Proxy, VAD37, Vagner, WATCHPUG, \_\_141345\_\_, auditsea, carrotsmuggler, immeas, innertia, kiki\_dev, pengun, qpzm, saidam017, sakshamguruji, toshii, and tvdung94. The recommendation is to delete the last 1e18 factor.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/535 

## Found by 
0xRobocop, 0xlmanini, Aymen0909, Bahurum, Bauer, Juntao, Nyx, Proxy, VAD37, Vagner, WATCHPUG, \_\_141345\_\_, auditsea, carrotsmuggler, immeas, innertia, kiki\_dev, pengun, qpzm, saidam017, sakshamguruji, toshii, tvdung94
## Summary

The variable `amountToSellUnits` is computed wrongly in the code which will lead to an incorrect amount of collateral to be sold.

## Vulnerability Detail

The `BuyUSSDSellCollateral()` function is used to sell collateral during a peg-down recovery event. The computation of the amount to sell is computed using the following formula:

```solidity
// @audit-issue Wrong computation
uint256 amountToSellUnits = IERC20Upgradeable(collateral[i].token).balanceOf(USSD) * ((amountToBuyLeftUSD * 1e18 / collateralval) / 1e18) / 1e18;
```

The idea is to sell an amount which is equivalent (in USD) to the ratio of `amountToBuyLeftUSD / collateralval`. Flattening the equation it ends up as:

```solidity
uint256 amountToSellUnits = (collateralBalance * amountToBuyLeftUSD * 1e18) / (collateralval * 1e18 * 1e18);

// Reducing the equation
uint256 amountToSellUnits = (collateralBalance * amountToBuyLeftUSD) / (collateralval * 1e18);
```

`amountToBuyLeftUSD` and `collateralval` already have 18 decimals so their decimals get cancelled together which will lead the last 1e18 factor as not necessary.

## Impact

The contract will sell an incorrect amount of collateral during a peg-down recovery event.

## Code Snippet

https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/contracts/USSDRebalancer.sol#L121

## Tool used

Manual Review

## Recommendation

Delete the last 1e18 factor

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | qpzm, innertia, toshii, Nyx, WATCHPUG, kiki\_dev, carrotsmuggler, Juntao, saidam017, Vagner, auditsea, VAD37, Bauer, Bahurum, immeas, Aymen0909, 0xRobocop, tvdung94, sakshamguruji, Proxy, 0xlmanini, pengun, \_\_141345\_\_ |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/535
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`Wrong Math`

