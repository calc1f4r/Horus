---
# Core Classification
protocol: bunker.finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2217
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-bunkerfinance-contest
source_link: https://code4rena.com/reports/2022-05-bunker
github_link: https://github.com/code-423n4/2022-05-bunker-findings/issues/105

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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-04] `COMP` Distributions Can Be Manipulated And Duplicated Across Any Number Of Accounts

### Overview


This bug report concerns the Bunker Protocol, a fork of Compound with NFT integration. Part of the original functionality of Compound appears to have been mistakenly commented out, which means that whenever users enter or exit the protocol, token distributions will not be correctly calculated for suppliers. This can be exploited as suppliers can manipulate their yield by supplying tokens, calling certain functions, removing their tokens and repeating the same process on other accounts. This breaks all yield distributions and there is currently no way to upgrade the contracts to alter the contract's behaviour. The recommended mitigation steps are to either comment all behaviour associated with token distributions if token distributions are not meant to be supported, or to uncomment all occurrences of the related functions.

### Original Finding Content

_Submitted by leastwood_

[Comptroller.sol#L240-L242](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L240-L242)<br>
[Comptroller.sol#L260-L262](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L260-L262)<br>
[Comptroller.sol#L469-L472](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L469-L472)<br>
[Comptroller.sol#L496-L499](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L496-L499)<br>
[Comptroller.sol#L1139-L1155](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L1139-L1155)<br>
[Comptroller.sol#L1222-L1243](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/Comptroller.sol#L1222-L1243)<br>

The `updateCompSupplyIndex()` and `distributeSupplierComp()` functions are used by Compound to track distributions owed to users for supplying funds to the protocol. Bunker protocol is a fork of compound with NFT integration, however, part of the original functionality appears to have been mistakenly commented out. As a result, whenever users enter or exit the protocol, `COMP` distributions will not be correctly calculated for suppliers. At first glance, its possible that this was intended, however, there is nothing stated in the docs that seems to indicate such. Additionally, the `COMP` distribution functionality has not been commented out for borrowers. Therefore, tokens will still be distributed for borrowers.

Both the `updateCompSupplyIndex()` and `updateCompBorrowIndex()` functions operate on the same `compSpeeds` value which dictates how many tokens are distributed on each block. Therefore, you cannot directly disable the functionality of supplier distributions without altering how distributions are calculated for borrowers. Because of this, suppliers can manipulate their yield by supplying tokens, calling `updateCompSupplyIndex()` and `distributeSupplierComp()`, removing their tokens and repeating the same process on other accounts. This completely breaks all yield distributions and there is currently no way to upgrade the contracts to alter the contract's behaviour. Tokens can be claimed by redepositing in a previously "checkpointed" account, calling `claimComp()` and removing tokens before re-supplying on another account.

### Recommended Mitigation Steps

Consider commenting all behaviour associated with token distributions if token distributions are not meant to be supported. Otherwise, it is worthwhile uncommenting all occurrences of the `updateCompSupplyIndex()` and `distributeSupplierComp()` functions.

**[bunkerfinance-dev (bunker.finance) acknowledged, but disagreed with High severity and commented](https://github.com/code-423n4/2022-05-bunker-findings/issues/105#issuecomment-1129626056):**
 > We are not going to use the COMP code. We could fix documentation or comment more code to make this clearer though.

**[gzeon (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-bunker-findings/issues/105#issuecomment-1140432093):**
 > Comptroller.sol is [in scope](https://github.com/code-423n4/2022-05-bunker) of this contest, and there are no indication that token distribution will be disabled despite the sponsor claim they are not going to use the $COMP code. However, it is also true the deployment setup within contest repo lack the deployment of $COMP and its distribution. I believe this is a valid Med Risk issue given fund(reward token) can be lost in certain assumptions.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | bunker.finance |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-bunker
- **GitHub**: https://github.com/code-423n4/2022-05-bunker-findings/issues/105
- **Contest**: https://code4rena.com/contests/2022-05-bunkerfinance-contest

### Keywords for Search

`vulnerability`

