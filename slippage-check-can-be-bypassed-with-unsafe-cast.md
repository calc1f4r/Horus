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
solodit_id: 41567
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uniswap-v4-periphery-and-universal-router-audit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Slippage Check Can Be Bypassed With Unsafe Cast

### Overview


The Position Manager in the Uniswap v4-periphery code has a bug when removing liquidity. The `validateMinOut` function is supposed to protect against slippage and ensure that users get a minimum amount when removing liquidity. However, due to the introduction of delta-changing hooks, the returned `liquidityDelta` can sometimes be negative for one or both tokens. This can happen if a custom hook penalizes liquidity removal and requires users to pay to withdraw. 

The issue is that in the `validateMinOut` function, the returned amount is converted to `uint128` before being compared to the user-specified values. This means that a negative `int128` value can bypass the slippage check. To fix this, the code can be modified to exclude the delta caused by the hook when checking for slippage. Alternatively, the code can be changed to allow for `int128` inputs for `amount0Min` and `amount1Min`. 

This bug has been resolved in a recent pull request, so it should no longer be an issue. However, if safe cast is still being used for the returned delta, users should be given clear instructions on how to remove liquidity when their returned delta is negative.

### Original Finding Content

When removing liquidity from the Position Manager, the [`validateMinOut`](https://github.com/Uniswap/v4-periphery/blob/df47aa9ba521fc15ffd339dc773d32f5fc4c91fc/src/PositionManager.sol#L235) function enforces slippage protection and ensures that users get at least the specified minimum amounts out. Even though it is likely that `liquidityDelta` will be positive for both tokens, given the introduction of delta\-changing hooks, it is possible that the returned `liquidityDelta` is negative for one or both tokens. This scenario could happen, for example, when a custom hook penalizes liquidity removal and ends up requiring users to pay to withdraw.


In the [`validateMinOut`](https://github.com/Uniswap/v4-periphery/blob/df47aa9ba521fc15ffd339dc773d32f5fc4c91fc/src/libraries/SlippageCheck.sol#L15) function, the returned amount is cast to `uint128` before being compared to the user\-specified values. When a negative `int128` value is cast to `uint128`, the returned amount may bypass the slippage check.


Consider modifying the core contracts to return values that exclude the delta caused by the hook and checking slippage against those values. Alternatively, consider allowing `int128` inputs for `amount0Min` and `amount1Min`. If safe cast is being used for the returned delta, consider ensuring that there are clear instructions for users to remove liquidity when their returned delta is negative.


***Update:** Resolved in [pull request \#285](https://github.com/Uniswap/v4-periphery/pull/285/files).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

