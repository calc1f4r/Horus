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
solodit_id: 52470
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
source_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
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
  - Halborn
---

## Vulnerability Title

SwapManager Swaps Without Slippage Protection

### Overview


This bug report discusses an issue with the `SwapManager` contract, which performs swaps on the Uniswap V3 platform. The contract does not currently enforce slippage protection, which means that swap transactions can succeed even when the output is significantly lower than expected. This can result in unfavorable trades and potential loss of funds for users. To address this issue, the report recommends replacing the hardcoded `amountOutMinimum` parameter with a dynamic value that is specified by the user. This will ensure that the swap only proceeds if the output meets or exceeds the user's specified minimum amount, providing protection against slippage. The team behind the contract has accepted the risk of this finding, but may explore adding optional user-defined slippage protection in the future.

### Original Finding Content

##### Description

The `SwapManager` contract performs Uniswap V3 swaps without enforcing slippage protection. In both direct and indirect swaps, the `amountOutMinimum` parameter is hardcoded to `0`, as shown below:

```
...
if (directSwap) {
    IRouter.ExactInputSingleParams memory params = IRouter.ExactInputSingleParams({
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        fee: uint24(fee), //@audit unsafe casting
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
            address(tokenOut), uint24(pathFee[1]), stablecoin, uint24(pathFee[0]), tokenIn //@audit q? what if pathFee.length != 2?
        ),
        recipient: receiver,
        deadline: block.timestamp,
        amountIn: amountIn,
        amountOutMinimum: 0
    });
...
```

  

This lack of slippage protection means that swap transactions can succeed even when the output is significantly lower than expected, exposing users to unfavorable trades and potential fund loss. In Uniswap V3, the `amountOutMinimum` parameter is crucial to prevent execution under poor liquidity conditions or adverse price movements.

##### BVSS

[AO:A/AC:M/AX:M/C:N/I:M/A:M/D:H/Y:H/R:N/S:U (5.3)](/bvss?q=AO:A/AC:M/AX:M/C:N/I:M/A:M/D:H/Y:H/R:N/S:U)

##### Recommendation

Replace the hardcoded `amountOutMinimum` with a dynamic value passed as an argument to the function. This value should represent the minimum acceptable amount of tokens the user expects to receive, protecting them from slippage. For example:

```
function swapExactInput(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 minAmountOut,
    uint256 fee
) external {
    IRouter.ExactInputSingleParams memory params = IRouter.ExactInputSingleParams({
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        fee: uint24(fee),
        recipient: msg.sender,
        deadline: block.timestamp,
        amountIn: amountIn,
        amountOutMinimum: minAmountOut,
        sqrtPriceLimitX96: 0
    });

    router.exactInputSingle(params);
}
```

This ensures that the swap only proceeds if the output meets or exceeds the user-specified minimum amount, safeguarding users against slippage and improving overall protocol security.

##### Remediation

**RISK ACCEPTED:** The **Tren Finance team** accepted the risk of this finding, emphasizing that their swaps primarily involve low-volatility pools where slippage risk is minimal, following design precedents from other audited protocols. They acknowledged the potential for edge cases, but plan to explore optional user-defined slippage protection for added flexibility.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

