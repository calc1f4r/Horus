---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: uncategorized
vulnerability_type: allowance

# Attack Vector Details
attack_type: allowance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6265
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/339

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - allowance

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - jprod15
  - 0x52
  - Bahurum
  - cccz
  - Jeiwan
---

## Vulnerability Title

M-7: Rebalancing a negative Perp PnL via a Uniswap V3 token swap is broken due to the lack of token spending allowance

### Overview


This bug report is about a vulnerability in the `ISwapper spotSwapper` (i.e., `Uniswapper`) helper contract, used by the `PerpDepository._rebalanceNegativePnlWithSwap` function to perform the actual Uniswap V3 token swap. The required `assetToken` spending allowance for the `ISwapper spotSwapper` is missing, which leads to a revert due to insufficient allowance. This issue was found by 0x52, Jeiwan, berndartmueller, koxuan, jprod15, Bahurum, cccz, CRYP70, rvierdiiev, and GimelSec, and was identified through manual review. 

The impact of this issue is that rebalancing a negative Perp PnL via a Uniswap swap is missing the token approval and leads to a revert. The code snippet from line 507 of the PerpDepository.sol file is provided in the report. The recommendation is to consider adding the appropriate token approval before the swap in line 507.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/339 

## Found by 
0x52, Jeiwan, berndartmueller, koxuan, jprod15, Bahurum, cccz, CRYP70, rvierdiiev, GimelSec

## Summary

The `ISwapper spotSwapper` (i.e., `Uniswapper`) helper contract, used by the `PerpDepository._rebalanceNegativePnlWithSwap` function to perform the actual Uniswap V3 token swap, is missing the required `assetToken` spending allowance due to a lack of calling the `assetToken.approve` function.

## Vulnerability Detail

Rebalancing a negative Perp PnL with the `PerpDepository.rebalance` function calls the `_rebalanceNegativePnlWithSwap` function, which performs a Uniswap swap. However, the required `assetToken` spending allowance for the `ISwapper spotSwapper` (i.e. `Uniswapper`) helper contract is missing. This leads to a revert due to insufficient allowance.

## Impact

Rebalancing a negative Perp PnL via a Uniswap swap is missing the token approval and leads to a revert.

## Code Snippet

[integrations/perp/PerpDepository.sol#L507](https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L507)

```solidity
function _rebalanceNegativePnlWithSwap(
    uint256 amount,
    uint256 amountOutMinimum,
    uint160 sqrtPriceLimitX96,
    uint24 swapPoolFee,
    address account
) private returns (uint256, uint256) {
    uint256 normalizedAmount = amount.fromDecimalToDecimal(
        ERC20(quoteToken).decimals(),
        18
    );
    _checkNegativePnl(normalizedAmount);
    bool isShort = false;
    bool amountIsInput = true;
    (uint256 baseAmount, uint256 quoteAmount) = _placePerpOrder(
        normalizedAmount,
        isShort,
        amountIsInput,
        sqrtPriceLimitX96
    );
    vault.withdraw(assetToken, baseAmount);
    SwapParams memory params = SwapParams({
        tokenIn: assetToken,
        tokenOut: quoteToken,
        amountIn: baseAmount,
        amountOutMinimum: amountOutMinimum,
        sqrtPriceLimitX96: sqrtPriceLimitX96,
        poolFee: swapPoolFee
    });
    uint256 quoteAmountOut = spotSwapper.swapExactInput(params); // @audit-info missing token approval

    // [...]
}
```

## Tool used

Manual Review

## Recommendation

Consider adding the appropriate token approval before the swap in L507.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | jprod15, 0x52, Bahurum, cccz, Jeiwan, koxuan, berndartmueller, CRYP70, rvierdiiev, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/339
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`Allowance`

