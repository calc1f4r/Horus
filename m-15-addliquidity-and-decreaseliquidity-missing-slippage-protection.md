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
solodit_id: 29712
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/2

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
finders_count: 5
finders:
  - said
  - immeas
  - bin2chen
  - ladboy233
  - adriro
---

## Vulnerability Title

[M-15] AddLiquidity and decreaseLiquidity missing slippage protection

### Overview


This bug report discusses an issue with the code for a project called Particle. When users mint NFTs to add liquidity, they can specify two parameters, amount0Min and amount1Min. However, the code currently sets these parameters to 0, which can lead to a vulnerability. If the user's transaction is frontrun, a smaller amount of tokens can be minted or released. The report recommends not hardcoding these parameters to 0 and instead allowing users to control them. The project team has confirmed the issue and plans to make changes to address it.

### Original Finding Content


<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/libraries/LiquidityPosition.sol#L195> 

<https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/libraries/LiquidityPosition.sol#L258>

When user mint NFT add liquidity, user can specify two parameter, params.amount0Min and params.amount1Min

            // mint the position
            (tokenId, liquidity, amount0Minted, amount1Minted) = Base.UNI_POSITION_MANAGER.mint(
                INonfungiblePositionManager.MintParams({
                    token0: params.token0,
                    token1: params.token1,
                    fee: params.fee,
                    tickLower: params.tickLower,
                    tickUpper: params.tickUpper,
                    amount0Desired: params.amount0ToMint,
                    amount1Desired: params.amount1ToMint,
                    amount0Min: params.amount0Min,
                    amount1Min: params.amount1Min,
                    recipient: address(this),
                    deadline: block.timestamp
                })
            );

If the minted amount is too small, transaction revert [in this check](https://github.com/Uniswap/v3-periphery/blob/697c2474757ea89fec12a4e6db16a574fe259610/contracts/base/LiquidityManagement.sol#L88) in Uniswap position manager when addling liquidity.

```solidity
(amount0, amount1) = pool.mint(
	params.recipient,
	params.tickLower,
	params.tickUpper,
	liquidity,
	abi.encode(MintCallbackData({poolKey: poolKey, payer: msg.sender}))
);

require(amount0 >= params.amount0Min && amount1 >= params.amount1Min, 'Price slippage check');
```

However, when addling liquidity, the parameter [amount0Min and amount1Min is set to 0](https://github.com/code-423n4/2023-12-particle/blob/a3af40839b24aa13f5764d4f84933dbfa8bc8134/contracts/libraries/LiquidityPosition.sol#L195).

```solidity
// increase liquidity via position manager
(liquidity, amount0Added, amount1Added) = Base.UNI_POSITION_MANAGER.increaseLiquidity(
	INonfungiblePositionManager.IncreaseLiquidityParams({
		tokenId: tokenId,
		amount0Desired: amount0,
		amount1Desired: amount1,
		amount0Min: 0,
		amount1Min: 0,
		deadline: block.timestamp
	})
);
```

As Uniswap V3 docs highlight:

<https://docs.uniswap.org/contracts/v3/guides/providing-liquidity/mint-a-position#calling-mint>

> We set amount0Min and amount1Min to zero for the example - but this would be a vulnerability in production. A function calling mint with no slippage protection would be vulnerable to a frontrunning attack designed to execute the mint call at an inaccurate price.

If the user transaction suffers from frontrunning, a much less amount of token can be minted.

Same issue happens when user decrease liquidity:

```solidity
    function decreaseLiquidity(uint256 tokenId, uint128 liquidity) internal returns (uint256 amount0, uint256 amount1) {
        (amount0, amount1) = Base.UNI_POSITION_MANAGER.decreaseLiquidity(
            INonfungiblePositionManager.DecreaseLiquidityParams({
                tokenId: tokenId,
                liquidity: liquidity,
                amount0Min: 0,
                amount1Min: 0,
                deadline: block.timestamp
            })
        );
    }
```

The amount0 and amount1Min are set to 0.

When MEV bot frontruns the decrease liquidity, much less amount0 and amount1 are released.

### Recommended Mitigation Steps

Recommend do not hardcode slippage protection parameter amount0Min and amount1Min to 0 when increase liquidity or decrease liquidity.

**[0xleastwood (Judge) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/2#issuecomment-1866962114):**
 > This seems valid and serious. Worth adding as user-controlled parameters.

**[wukong-particle (Particle) confirmed and commented](https://github.com/code-423n4/2023-12-particle-findings/issues/2#issuecomment-1868137592):**
 > Agreed. Will add slippage protection when increase/decrease liquidity. 

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
| Finders | said, immeas, bin2chen, ladboy233, adriro |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/2
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`vulnerability`

