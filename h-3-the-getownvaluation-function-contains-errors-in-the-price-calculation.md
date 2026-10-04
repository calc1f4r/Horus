---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19132
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/222

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

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - carrotsmuggler
  - Bauer
  - J4de
  - simon135
  - warRoom
---

## Vulnerability Title

H-3: The getOwnValuation() function contains errors in the price calculation

### Overview


A bug report has been found on the getOwnValuation() function in the provided code of the UniSwap V3 pool. The bug leads to inaccurate price calculations when token0() or token1() is equal to USSD. This error can have a significant impact on the valuation of assets in the pool, leading to incorrect asset valuations and affecting trading decisions, liquidity provision, and overall financial calculations. The incorrect calculations are present in the code snippets given in the report, and manual review was used to find the bug. The recommendation is to replace the incorrect calculations with the correct ones when token0() or token1() is USSD.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/222 

## Found by 
0xPkhatri, 0xpinky, AlexCzm, Bauer, J4de, carrotsmuggler, kiki\_dev, peanuts, sam\_gmk, sashik\_eth, simon135, theOwl, twicek, warRoom
## Summary
The getOwnValuation() function in the provided code has incorrect price calculation logic when token0() or token1() is equal to USSD. The error leads to inaccurate price calculations.

## Vulnerability Detail
The `USSDRebalancer.getOwnValuation()` function calculates the price based on the sqrtPriceX96 value obtained from the uniPool.slot0() function. The calculation depends on whether token0() is equal to USSD or not.
If token0() is equal to USSD, the price calculation is performed as follows:
```solidity
  price = uint(sqrtPriceX96)*(uint(sqrtPriceX96))/(1e6) >> (96 * 2);
```
However,there is an error in the price calculation logic. The calculation should be:
```solidity
price = uint(sqrtPriceX96) * uint(sqrtPriceX96) * 1e6 >> (96 * 2);

```
If token0() is not equal to USSD, the price calculation is slightly different:
```solidity
 price = uint(sqrtPriceX96)*(uint(sqrtPriceX96))*(1e18 /* 1e12 + 1e6 decimal representation */) >> (96 * 2);
        // flip the fraction
        price = (1e24 / price) / 1e12;
```
The calculation should be:
```solidity
 price = uint(sqrtPriceX96)*(uint(sqrtPriceX96))*(1e6 /* 1e12 + 1e6 decimal representation */) >> (96 * 2);
        // flip the fraction
        price = (1e24 / price) / 1e12;
```
Reference link:
https://blog.uniswap.org/uniswap-v3-math-primer

## Impact
The incorrect price calculation in the getOwnValuation() function can lead to significant impact on the valuation of assets in the UniSwap V3 pool. The inaccurate prices can result in incorrect asset valuations, which may affect trading decisions, liquidity provision, and overall financial calculations based on the UniSwap V3 pool.

## Code Snippet
https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L74
https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L76
## Tool used

Manual Review

## Recommendation
When token0() is USSD, the correct calculation should be uint(sqrtPriceX96) * uint(sqrtPriceX96) * 1e6 >> (96 * 2).
When token1() is USSD, the correct calculation should be 
```solidity 
price = uint(sqrtPriceX96)*(uint(sqrtPriceX96))*(1e6 /* 1e12 + 1e6 decimal representation */) >> (96 * 2);
        // flip the fraction
        price = (1e24 / price) / 1e12;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | carrotsmuggler, Bauer, J4de, simon135, warRoom, sam\_gmk, 0xPkhatri, twicek, 0xpinky, kiki\_dev, peanuts, sashik\_eth, theOwl, AlexCzm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/222
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`vulnerability`

