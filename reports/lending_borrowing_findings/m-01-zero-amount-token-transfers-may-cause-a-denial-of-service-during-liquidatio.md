---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29698
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/61

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
  - erc20
  - weird_erc20
  - liquidation
  - revert_on_0_transfer

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - adriro
  - bin2chen
  - immeas
---

## Vulnerability Title

[M-01] Zero amount token transfers may cause a denial of service during liquidations

### Overview


This bug report discusses an issue with some ERC20 implementations that revert on zero value transfers. This can cause an accidental denial of service in the LAMM protocol, preventing successful liquidations. The impact of this bug is that liquidations may not be properly incentivized, leading to potential issues with protocol liveness. The recommendation is to check that transfer amounts are greater than zero before executing them. The severity of this bug is considered medium, as it can affect the protocol's functionality, but it is not as severe as other issues with blocklisted tokens.

### Original Finding Content


Some ERC20 implementations revert on zero value transfers. Since liquidation rewards are based on a fraction of the available position's premiums, this may cause an accidental denial of service that prevents the successful execution of liquidations.

### Impact

Liquidations in the LAMM protocol are incentivized by a reward that is calculated as a fraction of the premiums available in the position.

<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/protocol/ParticlePositionManager.sol#L348-L354>

```solidity
348:         // calculate liquidation reward
349:         liquidateCache.liquidationRewardFrom =
350:             ((closeCache.tokenFromPremium) * LIQUIDATION_REWARD_FACTOR) /
351:             uint128(Base.BASIS_POINT);
352:         liquidateCache.liquidationRewardTo =
353:             ((closeCache.tokenToPremium) * LIQUIDATION_REWARD_FACTOR) /
354:             uint128(Base.BASIS_POINT);
```

These amounts are later transferred to the caller, the liquidator, at the end of the `liquidatePosition()` function.

<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/protocol/ParticlePositionManager.sol#L376-L378>

```solidity
376:         // reward liquidator
377:         TransferHelper.safeTransfer(closeCache.tokenFrom, msg.sender, liquidateCache.liquidationRewardFrom);
378:         TransferHelper.safeTransfer(closeCache.tokenTo, msg.sender, liquidateCache.liquidationRewardTo);
```

Reward amounts, `liquidationRewardFrom` and `liquidationRewardTo`, can be calculated as zero if `tokenFromPremium` or `tokenToPremium` are zero, if the liquidation ratio gets rounded down to zero, or if `LIQUIDATION_REWARD_FACTOR` is zero.

Coupled with that fact that some ERC20 implementations [revert on zero value transfers](https://github.com/d-xo/weird-erc20?tab=readme-ov-file#revert-on-zero-value-transfers), this can cause an accidental denial of service in the implementation of `liquidatePosition()`, blocking certain positions from being liquidated.

### Recommendation

Check that the amounts are greater than zero before executing the transfer.

```diff
        // reward liquidator
+       if (liquidateCache.liquidationRewardFrom > 0) {
          TransferHelper.safeTransfer(closeCache.tokenFrom, msg.sender, liquidateCache.liquidationRewardFrom);
+       }
+       if (liquidateCache.liquidationRewardTo > 0) {
          TransferHelper.safeTransfer(closeCache.tokenTo, msg.sender, liquidateCache.liquidationRewardTo);
+       }
```


**[0xleastwood (Judge) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/61#issuecomment-1866972456):**
 > Unlikely token type to even support in the first place. Probably more of a QA issue.

**[wukong-particle (Particle) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/61#issuecomment-1868223734):**
 > Agree with the judge. Though we can add a zero check to all transfers to potentially save gas. 

**[adriro (Warden) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/61#issuecomment-1872538647):**
 > I believe this is similar to the issue that mentions tokens with blocklists (#31, judged as high) as both of these are non standard (in the strict sense of the standard), though it is of course fair to say that blocklists are more frequent (eg usdc, usdt). 
> 
> Note that the protocol doesn't have any sort of allow list to control which ERC20 tokens are supported inside the protocol, and anyone can open a position using any Uniswap pool, which also means any token. The main problem here is that liquidations can be blocked after a position is open, that's why I consider the med severity justified.

**[0xleastwood (Judge) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/61#issuecomment-1872943231):**
 > The difference being that there are little to no tokens supported across all lending platforms which revert on zero token transfer where there are almost always tokens supported with blocklists. 
 >
 > I guess this can remain medium because anyone can LP into a position and protocol liveness should be highlighted here.

 **[wukong-particle (Particle) confirmed](https://github.com/code-423n4/2023-12-particle-findings/issues/61#issuecomment-1889804514)**

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
| Finders | adriro, bin2chen, immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/61
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`ERC20, Weird ERC20, Liquidation, Revert On 0 Transfer`

