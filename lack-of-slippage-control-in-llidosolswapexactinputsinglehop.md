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
solodit_id: 40681
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
finders_count: 24
finders:
  - innertia
  - 0xRizwan
  - ladboy233
  - deth
  - 0xrex
---

## Vulnerability Title

Lack of slippage control in llido.sol::swapexactinputsinglehop 

### Overview


Summary:

The bug report discusses various vulnerabilities and issues found in the code of a protocol. These issues include potential exposure to sandwich attacks and MEV attacks, the possibility of funds being locked forever, and exploitable voting rules. The report also suggests possible solutions and recommendations for fixing these issues. Some of the issues have already been fixed, while others are yet to be addressed.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
When swapping the tokens with function `LLido.sol::swapExactInputSingleHop`, the slippage control is disabled by configuring the `amountOutMin` to zero. This can potentially expose the swap/trade to sandwich attacks and MEV (Miner Extractable Value) attacks, resulting in a suboptimal amount of tokens received from the swap/trade.

## In `LLido.sol::swapExactInputSingleHop`
```solidity
function swapExactInputSingleHop(
    address tokenIn,
    address tokenOut,
    uint amountIn
) internal returns (uint amountOut) {
    ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
        tokenIn: tokenIn,
        tokenOut: tokenOut,
        fee: POOL_FEE,
        recipient: address(this),
        // deadline: block.timestamp,
        amountIn: amountIn,
        amountOutMinimum: 0, // erictee-issue: No slippage check.
        sqrtPriceLimitX96: 0
    });
    amountOut = router.exactInputSingle(params);
}
```

## Recommendation
One possible solution is to dynamically compute the minimum amount of tokens to be received after the swap based on the maximum allowable slippage percentage (e.g. 5%) and the exchange rate (Source Token <> Destination Token) from a source that cannot be manipulated (e.g. Chainlink, Custom TWAP). 

Alternatively, consider restricting access to these functions to only certain actors who can be trusted to define an appropriate slippage parameter where possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Goat Tech |
| Report Date | N/A |
| Finders | innertia, 0xRizwan, ladboy233, deth, 0xrex, Tripathi, twcctop, 0xTheBlackPanther, tutkata, erictee, Auditism, 0xRajkumar, zigtur, john-femi, Bauchibred, walter, 0xhashiman, Rotciv Egaf, Lefg, smbv19192323, b0g0, merlin, Said, jesjupyter |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5

### Keywords for Search

`vulnerability`

