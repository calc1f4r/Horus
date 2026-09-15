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
solodit_id: 54916
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
finders_count: 1
finders:
  - 0x37
---

## Vulnerability Title

LPs can split their liquidity withdrawal to get more tokens 

### Overview


This bug report discusses an issue with LP rewards when withdrawing liquidity in multiple transactions. The formula used to calculate rewards is affected by a decrease in `lpSupply`, which can result in later LPs receiving more rewards than earlier ones. This can be exploited by malicious users, especially during high market activity. A proof of concept test case is provided to demonstrate the impact. The recommendation is to record `lpSupply` for each block and use the same value for all withdrawals in that block to prevent this issue.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Summary
When LPs split their liquidity withdrawal into several pieces, they may get more rewards than expected.

## Finding Description
When LPs withdraw liquidity, we calculate LP rewards according to the formula (Eq.F-3: in the docs). When we examine this formula, we find that LP reward is related to `lpSupply`. Assuming that the current timestamp does not change, and the total reward does not change in this block, after `lpSupply` decreases, LPs may withdraw more tokens with the same LP amount. 

For example, if Alice wants to withdraw 1000 liquidity, she can choose to split her withdrawal into 10 transactions of 100 liquidity each. By triggering `withdrawLiquidity` 10 times, after the first withdrawal of 100 liquidity, she will receive more LP rewards for the next 100 liquidity withdrawal.

## Impact Explanation
1. In the same block, the later LP withdrawer may get more rewards than the previous one, which is unfair.
2. Malicious users can exploit this by splitting their liquidities and triggering `withdrawLiquidity` multiple times to gain more rewards.

## Likelihood Explanation
Any LP can take advantage of this issue to extract more rewards. However, it's important to note that when total rewards are significantly smaller than `lpSupply`, the profit will be minimal. This issue becomes quite profitable during times of high market activity, where substantial swap fees are earned.

## Proof of Concept
Add the following test case into `TermMaxRouter.t.sol`. In this scenario, we perform a large number of trades, generating significant swap fees.

When Alice withdraws all her liquidity in one transaction (split = 1), the `ft amt` is 2097620090729, and `xt amt` is 2381501084289. If she splits her liquidity and withdraws all through 10 transactions, the `ft amt` becomes 2149293035341, and the `xt amt` is 2440368687106. Thus, Alice receives an additional 2.5% in both `ft amt` and `xt amt`.

```solidity
function testPocRwardRatio() public {
    // Step 1
    vm.startPrank(alice);
    res.underlying.approve(address(res.market), 10000e8);
    res.market.provideLiquidity(10000e8);
    console.log("alice lpFt amt: ", res.lpFt.balanceOf(alice));
    console.log("alice lpXt amt: ", res.lpXt.balanceOf(alice));
    vm.stopPrank();

    // Trade Ft xt to generate some swap fees
    vm.startPrank(deployer);
    for (uint i = 0; i < 1200; i++) {
        res.underlying.approve(address(res.market), 6000e8);
        res.market.buyFt(5000e8, 0);
        res.market.buyXt(1000e8, 0);
        res.ft.approve(address(res.market), res.ft.balanceOf(deployer));
        res.xt.approve(address(res.market), res.xt.balanceOf(deployer));
        res.market.sellFt(uint128(res.ft.balanceOf(deployer)), 0);
        res.market.sellXt(uint128(res.xt.balanceOf(deployer)), 0);
    }
    vm.stopPrank();

    vm.startPrank(alice);
    res.lpFt.approve(address(router), res.lpFt.balanceOf(alice));
    res.lpXt.approve(address(router), res.lpXt.balanceOf(alice));

    // ft: 2097620090729 split = 1
    // xt: 2381501084289 split = 1
    // ft: 2149293035341 split = 10
    // xt: 2440368687106 split = 10
    uint256 split = 10;
    uint256 lpFtAmt = res.lpFt.balanceOf(alice) / split;
    uint256 lpXtAmt = res.lpXt.balanceOf(alice) / split;
    
    for (uint i = 0; i < split; i++) {
        router.withdrawLiquidityToFtXt(alice, res.market, lpFtAmt, lpXtAmt, 0, 0);
    }
    
    console.log("After withdraw, alice ft token amt: ", res.ft.balanceOf(alice));
    console.log("After withdraw, alice xt token amt: ", res.xt.balanceOf(alice));
    vm.stopPrank();
}
```

## Recommendation
To prevent this issue, we should record one `lpSupply` for each block. During the first withdrawal of a block, we need to record the `lpSupply` and use the same value for all withdrawals in that block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | TermMax |
| Report Date | N/A |
| Finders | 0x37 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_term_max_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/850188b4-3c16-4d60-97aa-0eeb288b0434

### Keywords for Search

`vulnerability`

