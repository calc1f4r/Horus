---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29700
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/55

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - adriro
---

## Vulnerability Title

[M-03] Increase liquidity in close position may not cover original borrowed liquidity

### Overview


This bug report is about a potential issue in the Particle LAMM protocol. When a position is closed, there is no check to ensure that the added liquidity covers the original borrowed liquidity from the LP. This means that the LP may not get their liquidity back, regardless of the outcome of the trade. The report recommends adding a check to ensure that the added liquidity covers the borrowed amount. The team behind Particle has acknowledged the issue and commented on it, stating that they have intentionally omitted the check but may consider adding it in the future. 

### Original Finding Content


<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/protocol/ParticlePositionManager.sol#L424> 

<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/protocol/ParticlePositionManager.sol#L432>

When a position is closed, there is no check to ensure that the effective added liquidity covers the original borrowed liquidity from the LP.

### Impact

Closing a position in the Particle LAMM protocol must ensure that the borrowed liquidity gets fully added back to the LP. Independently of the outcome of the trade, the LP should get its liquidity back. The implementation of `_closePosition()` calculates the required amounts and executes a call to `LiquidityPosition.increaseLiquidity()`, which ends up calling `increaseLiquidity()` in the Uniswap Position Manager.

<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/protocol/ParticlePositionManager.sol#L422-L439>

```solidity
422:         // add liquidity back to borrower
423:         if (lien.zeroForOne) {
424:             (cache.liquidityAdded, cache.amountToAdd, cache.amountFromAdd) = LiquidityPosition.increaseLiquidity(
425:                 cache.tokenTo,
426:                 cache.tokenFrom,
427:                 lien.tokenId,
428:                 cache.amountToAdd,
429:                 cache.amountFromAdd
430:             );
431:         } else {
432:             (cache.liquidityAdded, cache.amountFromAdd, cache.amountToAdd) = LiquidityPosition.increaseLiquidity(
433:                 cache.tokenFrom,
434:                 cache.tokenTo,
435:                 lien.tokenId,
436:                 cache.amountFromAdd,
437:                 cache.amountToAdd
438:             );
439:         }
```

As we can see in lines 424 and 432, the effective results of the liquidity increment are returned from the call to Uniswap NPM. Both `amountToAdd` and `amountFromAdd` are correctly overwritten with the actual amounts used by the `addLiquidity()` action, but `liquidityAdded` is simply assigned to the cache and never checked.

The effective added liquidity may fall short to cover the original borrowed liquidity, and if so the lien will be closed without returning the full amount to the LP.

### Recommendation

Ensure the effective added liquidity covers the original borrowed amount.

```diff
        // add liquidity back to borrower
        if (lien.zeroForOne) {
            (cache.liquidityAdded, cache.amountToAdd, cache.amountFromAdd) = LiquidityPosition.increaseLiquidity(
                cache.tokenTo,
                cache.tokenFrom,
                lien.tokenId,
                cache.amountToAdd,
                cache.amountFromAdd
            );
        } else {
            (cache.liquidityAdded, cache.amountFromAdd, cache.amountToAdd) = LiquidityPosition.increaseLiquidity(
                cache.tokenFrom,
                cache.tokenTo,
                lien.tokenId,
                cache.amountFromAdd,
                cache.amountToAdd
            );
        }
        
+       require(cache.liquidityAdded >= lien.liquidity, "Failed to cover borrowed liquidity");
```

**[wukong-particle (Particle) acknowledged and commented](https://github.com/code-423n4/2023-12-particle-findings/issues/55#issuecomment-1868222714):**
 > We omit the check intentionally because the amount required to repay is calculated with uniswap math in the contract: https://github.com/code-423n4/2023-12-particle/blob/main/contracts/protocol/ParticlePositionManager.sol#L410. 
> 
> However, in our experience, this calculation might be tiny bit off when the actual amount is returned in `cache.liquidityAdded`.
> 
> If we need to check, we should do something like
> 
> ```
> require(cache.liquidityAdded + lien.liquidity / 1_000_000 >= lien.liquidity, "Failed to cover borrowed liquidity");
> ```
> 
> where `1_000_000` is a buffer. But getting this `1_000_000` check is only just to satisfy the calculation..
> 
> Unless this opens some other attack angle -- can someone somehow flash loan and change price dramatically to make this calculation off by a lot?
> 
> If not, we tend to skip this extra check. Thanks!


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | adriro |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/55
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`vulnerability`

