---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29477
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/269

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
finders_count: 35
finders:
  - codegpt
  - qbs
  - KmanOfficial
  - savi0ur
  - mrudenko
---

## Vulnerability Title

[M-15] `sync` function in `RdpxV2Core.sol` should be called in multiple scenarios to account for the balance changes that occurs

### Overview


This bug report is about a function called 'sync' which is used in 'RdpxV2Core.sol' to synchronize the balances of the reserve assets stored in the contract. It is observed that the 'sync' function is not called in all of the situations where swaps/providing/removing liquidity is made. This can cause wrong assumptions to be taken in cases of 'lowerDepeg' or 'upperDepeg', or any other functions that uses the balances of assets stored, if 'sync' was not called before.

Proof of Concept: It is seen that 'sync' is called in 'UniV3LiquidityAmo.sol' after '_sendTokensToRdpxV2Core' is called to occur for all of the balances change after modifying the liquidity in UniswapV3. However, it is not called functions like 'collectFees' where funds are directly transferred to 'RdpxV2Core.sol' or in '_sendTokensToRdpxV2Core' in the 'UniV2LiquidityAmo.sol' which transfers tokens to 'RdpxV2Core'.

Recommended Mitigation Steps: It is recommended to call 'sync' in 'collectFees' and '_sendTokensToRdpxV2Core' from 'UniV2LiquidityAmo.sol' also to accounts for any balance changes, which will protect the protocol against errors. It is also seen that 'sync' is called in 'UniV3LiquidityAmo.sol' after '_sendTokensToRdpxV2Core' is called to occur for all of the balances change after modifying the liquidity in UniswapV3.

It is also observed that this bug can potentially impact the functions like '_purchaseOptions', '_stake', 'settle', 'provideFunding', 'lowerDepeg' and 'getReserveTokenInfo' is no longer a reliable source for external integration to retrieve the token balance state. It is also mentioned that this bug could have been an opportunity for a higher exploit.

### Original Finding Content


<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV2LiquidityAmo.sol#L160-L178> 

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV3LiquidityAmo.sol#L118-L133>

The function `sync` is used in `RdpxV2Core.sol` to synchronize the balances of the reserve assets stored in the contract, but it is not called in all of the situations where swaps/providing/removing liquidity is made.

### Proof of Concept

As you can see `sync` is called in `UniV3LiquidityAmo.sol` after `_sendTokensToRdpxV2Core` is called to occur for all of the balances change after modifying the liquidity in UniswapV3 <br><https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV3LiquidityAmo.sol#L361><br>
But it is not called functions like `collectFees` where funds are directly transferred to `RdpxV2Core.sol` <br><https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV3LiquidityAmo.sol#L118-L133><br>
Or in `_sendTokensToRdpxV2Core` in the `UniV2LiquidityAmo.sol` which transfers tokens to `RdpxV2Core` <br><https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV2LiquidityAmo.sol#L157-L178><br>
Because of that wrong assumptions can be taken in cases of `lowerDepeg` or `upperDepeg`, or any other functions that uses the balances of assets stored, if `sync` was not called before.

### Recommended Mitigation Steps

Since you already call `sync` in `_sendTokensToRdpxV2Core` from `UniV3LiquidityAmo.sol`, call it in `collectFees` and `_sendTokensToRdpxV2Core` from `UniV2LiquidityAmo.sol` also to accounts for any balance changes, which will protect the protocol against errors.

**[bytes032 (Lookout) commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/269#issuecomment-1712408116):**
 > * [This is related to Uni V2, in the implementation for V3 it is called.](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/amo/UniV3LiquidityAmo.sol#L361)
> * This will cause less than expected backing reserves, which can lead to underflow when performing various other actions such as when providing funding for APP options (provideFunding()), settling options (settle()).
> * The [function getReserveTokenInfo](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L1135) is no longer a reliable source for external integration to retrieve the token balance state.
> 
> Potentially impacts the following functions:
> - [_purchaseOptions](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L486)
> - [_stake](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L570)
> - [settle](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L780)
> - [provideFunding](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L803)
> - [lowerDepeg](https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L1106)
> 
> Edit: It’s actually not called in [collectFee’s](https://github.com/code-423n4/2023-08-dopex-findings/issues/934) as well. I’m duplicating all of these under a single primary issue, because #269 mentions both.

**[witherblock (Dopex) confirmed](https://github.com/code-423n4/2023-08-dopex-findings/issues/269#issuecomment-1734174462)**

**[Alex the Entreprenerd (Judge) commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/269#issuecomment-1759127851):**
 > Seems like an opportunity for a higher exploit was missed by stopping at the broken sync.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | codegpt, qbs, KmanOfficial, savi0ur, mrudenko, wintermute, nemveer, T1MOH, MohammedRizwan, Vagner, tapir, Evo, zzebra83, said, Viktor\_Cortess, Yanchuan, peakbolt, Aymen0909, alexzoid, 0Kage, oakcobalt, bin2chen, pep7siup, 1, 2, 0xCiphky, hals |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/269
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`vulnerability`

