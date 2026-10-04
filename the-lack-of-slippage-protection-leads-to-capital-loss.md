---
# Core Classification
protocol: Goat Tech
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40680
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
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
finders_count: 3
finders:
  - Bauchibred
  - Bauer
  - 0xRajkumar
---

## Vulnerability Title

The lack of slippage protection leads to capital loss 

### Overview


The bug report is about a vulnerability in the Controller.earningPulls() function of a protocol. The function converts wstETH to WETH and transfers it to the user as ETH. However, the protocol does not have any protection against slippage, making it vulnerable to sandwich attacks. The recommendation is to set parameters for slippage protection to fix the issue. 

### Original Finding Content

## Vulnerability Report

## Context
(No context files were provided by the reviewer)

## Description
In the `Controller.earningPulls()` function, if `bountyPullerTo_` is not equal to `account_`, the protocol calculates `amountForPuller`, converts this amount of wstETH to WETH, and then transfers it to the user as ETH:

```solidity
if (bountyPullerTo_ == account_) {
    _geth.transfer(address(_eEarning), _geth.balanceOf(address(this)));
} else {
    uint256 amountForPuller = _geth.balanceOf(address(this)) * _bountyPullEarningPercent / LPercentage.DEMI;
    LLido.sellWsteth(amountForPuller);
    LLido.wethToEth();
    payable(bountyPullerTo_).transfer(address(this).balance);
    _geth.transfer(address(_eEarning), _geth.balanceOf(address(this)));
}
```

When converting wstETH to WETH in Uniswap v3, we found that `amountOutMinimum` is set to 0, indicating no protection against slippage. This leaves the protocol vulnerable to sandwich attacks:

```solidity
ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
    tokenIn: tokenIn,
    tokenOut: tokenOut,
    fee: POOL_FEE,
    recipient: address(this),
    // deadline: block.timestamp,
    amountIn: amountIn,
    amountOutMinimum: 0,
    sqrtPriceLimitX96: 0
});
amountOut = router.exactInputSingle(params);
```

## Recommendation
Setting parameters for slippage protection.

**Goat Fixed.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Goat Tech |
| Report Date | N/A |
| Finders | Bauchibred, Bauer, 0xRajkumar |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5

### Keywords for Search

`vulnerability`

