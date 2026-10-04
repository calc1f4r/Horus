---
# Core Classification
protocol: Uniswap v4 Periphery and Universal Router Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41565
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uniswap-v4-periphery-and-universal-router-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Slippage Checks Are Not Enforced When Fees Accrued Exceed Tokens Required for a Liquidity Deposit

### Overview


The bug report states that when increasing the liquidity of a position, the function `validateMaxInNegative` in the `SlippageCheck.sol` file does not properly check for slippage when the `balanceDelta` is positive. This is a problem because even if the fees accrued exceed the tokens required for the liquidity deposit, slippage checks should still be enforced. This is important because any increase in liquidity loses value if the current tick of the pool deviates from the correct price tick. This bug can potentially be exploited by attackers, and it is recommended to check for slippage on the amount of tokens required to modify a liquidity position without including the accrued fees. The bug has been resolved in a recent update.

### Original Finding Content

When increasing the liquidity of a position, the [`validateMaxInNegative`](https://github.com/Uniswap/v4-periphery/blob/df47aa9ba521fc15ffd339dc773d32f5fc4c91fc/src/libraries/SlippageCheck.sol#L31) function in [`SlippageCheck.sol`](https://github.com/Uniswap/v4-periphery/blob/df47aa9ba521fc15ffd339dc773d32f5fc4c91fc/src/libraries/SlippageCheck.sol) does not check slippage when `balanceDelta` is positive. `balanceDelta` is a combination of the tokens required to modify a liquidity position and the fees accrued to a liquidity position. When the fees accrued exceed the tokens required to increase the liquidity of a position, `balanceDelta` can be positive.


However, slippage checks should still be enforced on positive balance deltas. Any liquidity increase loses value as long as the current tick of the pool deviates from the correct price tick. Normally, slippage checks would prevent the tick from being manipulated by a frontrunner as manipulating the pool tick always increases the `amountIn` of one of the tokens. Yet, when the fees accrued exceed the tokens required for the liquidity deposit, it is impossible to set a slippage parameter when the price tick is manipulated adversely.


From an attacker’s perspective, the fact that the liquidity deposit comes from fees makes no difference in a liquidity deposit sandwich attack. The liquidity depositor still loses value as their fees are converted to a liquidity position which is worth less than the pre\-deposit value.


Consider checking the slippage on the amount of tokens required to modify a liquidity position without including the accrued fees.


***Update:** Resolved in [pull request \#285](https://github.com/Uniswap/v4-periphery/pull/285).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Uniswap v4 Periphery and Universal Router Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uniswap-v4-periphery-and-universal-router-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

