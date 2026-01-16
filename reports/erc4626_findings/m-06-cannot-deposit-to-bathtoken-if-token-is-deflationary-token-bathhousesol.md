---
# Core Classification
protocol: Rubicon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2503
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-rubicon-contest
source_link: https://code4rena.com/reports/2022-05-rubicon
github_link: https://github.com/code-423n4/2022-05-rubicon-findings/issues/126

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
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - unforgiven
  - camden
  - GimelSec
  - PP1004
---

## Vulnerability Title

[M-06] Cannot deposit to BathToken if token is Deflationary Token (BathHouse.sol)

### Overview


This bug report is about the function `openBathTokenSpawnAndSignal` in the code found in the given link. It is possible that the function will always revert when `newBathTokenUnderlying` or `desiredPairedAsset` is a deflationary token. This was found through manual review. 

Deflationary tokens are ERC20 tokens that charge a certain fee for every `transfer()` or `transferFrom()` operation. This fee can cause the deposit call to revert due to there not being enough funds to transfer. 

The recommended mitigation steps for this bug are to set `initialLiquidityNew = newBathTokenUnderlying.balanceOf(address(this))` after line 163 and `initialLiquidityExistingBathToken  = desiredPairedAsset.balanceOf(address(this))` after line 178. This should ensure that the deposit call does not revert.

### Original Finding Content

_Submitted by PP1004, also found by unforgiven, GimelSec, and camden_

Function `openBathTokenSpawnAndSignal` will alway revert when `newBathTokenUnderlying` or `desiredPairedAsset` is deflationary token

### Proof of Concept

There are ERC20 tokens that may make certain customizations to their ERC20 contracts.
One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()`
For example, I will assume that `newBathTokenUnderlying` is deflationary token. After [line 163](https://github.com/code-423n4/2022-05-rubicon/blob/8c312a63a91193c6a192a9aab44ff980fbfd7741/contracts/rubiconPools/BathHouse.sol#L156-L163), the actual amount of `newBathTokenUnderlying` that BathHouse gained will be smaller than `initialLiquidityNew`. It will make the [deposit call](https://github.com/code-423n4/2022-05-rubicon/blob/8c312a63a91193c6a192a9aab44ff980fbfd7741/contracts/rubiconPools/BathHouse.sol#L168) reverted because there are not enough fund to transfer.

### Recommended Mitigation Steps

set `initialLiquidityNew = newBathTokenUnderlying.balanceOf(address(this))`  after [line 163](https://github.com/code-423n4/2022-05-rubicon/blob/8c312a63a91193c6a192a9aab44ff980fbfd7741/contracts/rubiconPools/BathHouse.sol#L156-L163) and `initialLiquidityExistingBathToken  = desiredPairedAsset.balanceOf(address(this))` after [line 178](https://github.com/code-423n4/2022-05-rubicon/blob/8c312a63a91193c6a192a9aab44ff980fbfd7741/contracts/rubiconPools/BathHouse.sol#L171-L178)

**[bghughes (Rubicon) acknowledged and commented](https://github.com/code-423n4/2022-05-rubicon-findings/issues/126#issuecomment-1146333694):**
 > This is correct, though I believe un needed. If the user wants to create a vault for a deflationary token they need only account for said transfer fee when calculating their `initialLiquidityNew` value.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-05-rubicon-findings/issues/126#issuecomment-1163386042):**
 > Not sure how you can account for transfer fee in `initialLiquidityNew` since it's the same amount used for approval and deposit: `IBathToken(newOne).deposit(initialLiquidityNew, msg.sender);`
> 
> It simply means that deflationary / FoT tokens arent supported at all, which isn't necessarily a bad thing. There isn't a loss of assets, though `function of the protocol or its availability could be impacted`. Keeping it at medium severity, although could've potentially lowered to QA too.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | unforgiven, camden, GimelSec, PP1004 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-rubicon
- **GitHub**: https://github.com/code-423n4/2022-05-rubicon-findings/issues/126
- **Contest**: https://code4rena.com/contests/2022-05-rubicon-contest

### Keywords for Search

`vulnerability`

