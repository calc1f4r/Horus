---
# Core Classification
protocol: Brahma Fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13258
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/05/brahma-fi/
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

protocol_categories:
  - dexes
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  George Kobakhidze

  - David Oz Kashi
  -  Sergii Kravchenko
---

## Vulnerability Title

Harvester.harvest swaps have no slippage parameters

### Overview


This bug report is related to the Convex ETH-stETH pool, where all reward tokens for staking are claimed and swapped into ETH. The swap for one reward token, LDO, is implemented through the Uniswap router, and is called with `amountOutMinimum: 0`, meaning that there is no slippage protection in this swap. This could result in a significant loss of yield from this reward as MEV bots could manipulate the price before this transaction and immediately reversing their action after the transaction, profiting at the expense of our swap. The other two tokens, CVX and CRV, are being swapped through their Curve pools, which also have a `min_dy` argument set to 0. 

The recommendation is to introduce some slippage parameters into the swaps, to prevent MEV bots from manipulating the price and profiting at the expense of the swap. This could help protect the yield from the reward tokens, and ensure that the rewards are swapped with minimal losses.

### Original Finding Content

#### Description


As part of the vault strategy, all reward tokens for staking in the Convex ETH-stETH pool are claimed and swapped into ETH. The swaps for these tokens are done with no slippage at the moment, i.e. the expected output amount for all of them is given as 0.


In particular, one reward token that is most susceptible to slippage is LDO, and its swap is implemented through the Uniswap router:


**code/contracts/ConvexExecutor/Harvester.sol:L142-L155**



```
function \_swapLidoForWETH(uint256 amountToSwap) internal {
    IUniswapSwapRouter.ExactInputSingleParams
        memory params = IUniswapSwapRouter.ExactInputSingleParams({
            tokenIn: address(ldo),
            tokenOut: address(weth),
            fee: UNISWAP\_FEE,
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: amountToSwap,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });
    uniswapRouter.exactInputSingle(params);
}

```
The swap is called with `amountOutMinimum: 0`, meaning that there is no slippage protection in this swap. This could result in a significant loss of yield from this reward as MEV bots could “sandwich” this swap by manipulating the price before this transaction and immediately reversing their action after the transaction, profiting at the expense of our swap. Moreover, the Uniswap pools seem to have low liquidity for the LDO token as opposed to Balancer or Sushiswap, further magnifying slippage issues and susceptibility to frontrunning.


The other two tokens - CVX and CRV - are being swapped through their Curve pools, which have higher liquidity and are less susceptible to slippage. Nonetheless, MEV strategies have been getting more advanced and calling these swaps with 0 as expected output may place these transactions in danger of being frontrun and “sandwiched” as well.


**code/contracts/ConvexExecutor/Harvester.sol:L120-L126**



```
if (cvxBalance > 0) {
    cvxeth.exchange(1, 0, cvxBalance, 0, false);
}
// swap CRV to WETH
if (crvBalance > 0) {
    crveth.exchange(1, 0, crvBalance, 0, false);
}

```
In these calls `.exchange` , the last `0` is the `min_dy` argument in the Curve pools swap functions that represents the minimum expected amount of tokens received after the swap, which is 0 in our case.


#### Recommendation


Introduce some slippage parameters into the swaps.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Brahma Fi |
| Report Date | N/A |
| Finders |  George Kobakhidze
, David Oz Kashi,  Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/05/brahma-fi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

