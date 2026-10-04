---
# Core Classification
protocol: Hooks Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52475
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
source_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
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
  - Halborn
---

## Vulnerability Title

Unsafe Downcasting

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `SwapManager`contract performs unsafe downcasting from `uint256` to `uint24` in the `_swapExactInput()` and `_swapExactInput()` functions when interacting with the Uniswap V3 router. Specifically, it transforms the arguments `fee` and `pathFee` as shown below:

```
function _swapExactInput(
...
    fee: uint24(fee),
    recipient: receiver,
    deadline: block.timestamp,
    amountIn: amountIn,
    amountOutMinimum: 0,
    sqrtPriceLimitX96: 0
  });

  _amountOut = router.exactInputSingle(params);
} else {
  IRouter.ExactInputParams memory params = IRouter.ExactInputParams({
    path: abi.encodePacked(
      address(tokenOut), uint24(pathFee[1]), stablecoin, uint24(pathFee[0]), tokenIn
    ),
...
```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:L/A:L/D:N/Y:N/R:N/S:U (2.1)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:L/A:L/D:N/Y:N/R:N/S:U)

##### Recommendation

Use OpenZeppelin's `SafeCast` library to safely downcast integers. Alternatively, implement a safety mechanism to ensure that the downcasted value does not exceed the range of the target type.

##### Remediation

**SOLVED:** The **Tren finance team** fixed this finding in commit `9ecb5ed` by implementing the recommendation.

##### Remediation Hash

<https://github.com/Tren-Finance/Tren-Contracts/commit/9ecb5edfddd2f74045b18e6120148316239ca359>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Hooks Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/tren-finance/hooks-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/tren-finance/hooks-contracts

### Keywords for Search

`vulnerability`

