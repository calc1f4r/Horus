---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17681
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
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
finders_count: 3
finders:
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

Trades are vulnerable to sandwich attacks

### Overview


This bug report is about a Denial of Service vulnerability in CrossLayerPortal/core/nativeSwappers/MosaicNativeSwapperETH.sol and MosaicNativeSwapperAVAX.sol. The vulnerability is caused by the lack of a minAmountOut parameter in the swapToNative function. This parameter is meant to protect users from trades that are executed through illiquid pools and sandwich attacks. Without this parameter, users may not receive any ETH in exchange for their tokens and may incur high slippage. 

The exploit scenario is that a relayer makes a trade on behalf of a user with the minAmountOut value set to zero, allowing a malicious user to sandwich the trade and profit off the spread at the user's expense. 

The short-term recommendation is to allow users to input a slippage tolerance and add access controls to the swapToNative function. The long-term recommendation is to consider the risks of integrating with other protocols such as Uniswap and implement mitigations for those risks.

### Original Finding Content

## Denial of Service Vulnerability Report

**Difficulty:** Medium  
**Type:** Denial of Service

## Target
- CrossLayerPortal/core/nativeSwappers/MosaicNativeSwapperETH.sol
- MosaicNativeSwapperAVAX.sol

## Description
The `swapToNative` function does not allow users to specify the `minAmountOut` parameter of `swapExactTokensForETH`, which indicates the minimum amount of ETH that a user will receive from a trade. Instead, the value is hard-coded to zero, meaning that there is no guarantee that users will receive any ETH in exchange for their tokens. By using a bot to sandwich a user’s trade, an attacker could increase the slippage incurred by the user and profit off of the spread at the user’s expense.

The `minAmountOut` parameter is meant to prevent the execution of trades through illiquid pools and to provide protection against sandwich attacks. The current implementation lacks protections against high slippage and may cause users to lose funds. This applies to the AVAX version as well. Composable Finance indicated that only the relayer will call this function, but the function lacks access controls to prevent users from calling it directly. Importantly, it is highly likely that if a relayer does not implement proper protections, all of its trades will suffer from high slippage, as they will represent pure-profit opportunities for sandwich bots.

```solidity
uint256 [] memory amounts = swapRouter.swapExactTokensForETH(
    _amount,
    0,
    path,
    _to,
    deadline
);
```
*Figure 2.1: Part of the `SwapToNative` function in `MosaicNativeSwapperETH.sol`: 44–50*

## Exploit Scenario
Bob, a relayer, makes a trade on behalf of a user. The `minAmountOut` value is set to zero, which means that the trade can be executed at any price. As a result, when Eve sandwiches the trade with a buy and sell order, Bob sells the tokens without purchasing any, effectively giving away tokens for free.

## Recommendations
- **Short term:** Allow users (relayers) to input a slippage tolerance, and add access controls to the `swapToNative` function.
- **Long term:** Consider the risks of integrating with other protocols such as Uniswap and implement mitigations for those risks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Troy Sargent, Anish Naik, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf

### Keywords for Search

`vulnerability`

