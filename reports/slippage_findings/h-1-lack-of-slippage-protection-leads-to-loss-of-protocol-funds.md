---
# Core Classification
protocol: Cork Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41475
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/506
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/66

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
finders_count: 15
finders:
  - 0xjoi
  - Abhan1041
  - 4b
  - 0x6a70
  - 0xnbvc
---

## Vulnerability Title

H-1: Lack of slippage protection leads to loss of protocol funds

### Overview


This bug report discusses a vulnerability in the Cork Protocol, specifically the lack of slippage protection when removing liquidity and swapping tokens in the automated market maker (AMM). This can potentially lead to loss of protocol funds and reduce the yield for users. The vulnerability was found by several users and can be exploited by frontrunning the transaction and manipulating the price, or by setting a high slippage when executing the transaction. The code snippet and tool used for this report were a manual review. The recommendation is for the protocol to implement slippage protection and set a deadline while removing liquidity and swapping tokens in the AMM. The issue has already been fixed by the protocol team in previous PRs/commits.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/66 

## Found by 
0x6a70, 0x73696d616f, 0xjoi, 0xnbvc, 4b, 4gontuk, Abhan1041, MohammedRizwan, Pheonix, StraawHaat, alphacipher, boringslav, ivanonchain, sakshamguruji, vinica\_boy
## Summary

There is no slippage protection while removing liquidity and swap tokens from AMM.

## Vulnerability Detail

There are 2 intances where slippage protection is missing which are as below:

1. When LV token holder redeem before expiry `vaultLib::redeemEarly` function is called in which `_liquidateLpPartial` function and in that  `_redeemCtDsAndSellExcessCt` is called. In `_redeemCtDsAndSellExcessCt` function CT tokens are swapped for RA tokens in AMM as below:

```solidity
...
ra += ammRouter.swapExactTokensForTokens(ctSellAmount, 0, path, address(this), block.timestamp)[1];
...
```
As stated above, `swapExactTokensForTokens` function's 2nd parameter is 0 which shows that there is no slippage protection for this 
swap and also deadline is block.timestamp.

2. In `vaultLib::_liquidateLpPartial` function `__liquidateUnchecked` is called in which liquidity is removed from AMM of RA-CT token pair by burning LP tokens of protocol as below:

```solidity
...
(raReceived, ctReceived) =
            ammRouter.removeLiquidity(raAddress, ctAddress, lp, 0, 0, address(this), block.timestamp);
...
```
As stated above, `removeLiquidity` function's 4th & 5th parameter is 0 which shows that there is no slippage protection for this swap and also deadline is block.timestamp.

In such cases, an attacker can frontrun the transaction by seeing it in the mempool and manipulate the price such that protocol transaction have to bear heavy slippage which will leads to loss of protocol funds.

Also, there is block.timestamp as deadline so malicious node can prevent transaction to execute temporary and  execute the transaction when there is high slippage which will also leads to loss of protocol funds.

## Impact

Loss of protocol funds which will reduce the yield of users.

## Code Snippet

https://github.com/sherlock-audit/2024-08-cork-protocol/blob/db23bf67e45781b00ee6de5f6f23e621af16bd7e/Depeg-swap/contracts/libraries/VaultLib.sol#L282

https://github.com/sherlock-audit/2024-08-cork-protocol/blob/db23bf67e45781b00ee6de5f6f23e621af16bd7e/Depeg-swap/contracts/libraries/VaultLib.sol#L345

## Tool used

Manual Review

## Recommendation

Protocol should implement slippage protection and set deadline while removing liquidity and also swap from AMM.



## Discussion

**ziankork**

Yes this is a valid issue, we've already fixed this prior to our trading competition except for the `deadline` vulnerability.

**v-kirilov**

#75 is a duplicate of this one!

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Cork-Technology/Depeg-swap/pull/76

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cork Protocol |
| Report Date | N/A |
| Finders | 0xjoi, Abhan1041, 4b, 0x6a70, 0xnbvc, Pheonix, 4gontuk, MohammedRizwan, StraawHaat, 0x73696d616f, boringslav, sakshamguruji, vinica\_boy, alphacipher, ivanonchain |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/66
- **Contest**: https://app.sherlock.xyz/audits/contests/506

### Keywords for Search

`vulnerability`

