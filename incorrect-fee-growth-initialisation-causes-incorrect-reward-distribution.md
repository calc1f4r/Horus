---
# Core Classification
protocol: Sorella Angstrom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41907
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sorella-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sorella-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 2
finders:
  - Milotruck
  - Desmond Ho
---

## Vulnerability Title

Incorrect fee growth initialisation causes incorrect reward distribution

### Overview


This bug report discusses a high-risk issue with the initialisation of the rewardGrowthOutside in the PoolUpdates.sol file. The current implementation differs from Uniswap's and allows for the creation of new positions with non-zero rewards. A proof of concept is provided to demonstrate the issue and a recommendation is made to align with Uniswap's implementation. The bug has been fixed in a recent commit, which required several changes including using different math methods and aligning with Uniswap's calculations. The report also suggests further changes to prevent accumulation overflows.

### Original Finding Content

Severity: High Risk
Context: PoolUpdates.sol#L74-L92
Description: The initialisation of the rewardGrowthOutside of a tick differs from Uniswap 's. It is set to
maintain the following invariant:
for all ticks: if (tick > current_tick) then
for all ticks: if (tick ' > tick) then
growthOutside[tick] >= growthOutside[tick ' ]
However, it is possible to re-initialise the rewardGrowthOutside when it shouldn 't. For instance, one could
create multiple positions with the same uninitialised lower tick, but different upper ticks that may have
different growth outside values in the same block. This results in being able to create a new position being
initialised with non-zero rewards.
Proof of Concept: Insert into PoolUpdates.t.sol :
function test_IncorrectFeeGrowthInside() public {
uint128 liq1 = 8.2e21;
address lp1 = makeAddr("lp_1");
handler.addLiquidity(lp1, 120, 180, liq1);
handler.addLiquidity(lp1, 120, 300, liq1);
handler.addLiquidity(lp1, 120, 360, liq1);
uint128 amount1 = 23.872987e18;
handler.rewardTicks(re(TickReward({tick: 180, amount: amount1})));
bumpBlock();
handler.rewardTicks(re(TickReward({tick: 300, amount: amount1})));
bumpBlock();
uint128 liq2 = 0.64e21;
address lp2 = makeAddr("lp_2");
handler.addLiquidity(lp2, 60, 300, liq2);
handler.addLiquidity(lp2, 60, 180, liq2);
uint256 positionRewardsUpperTick300 = positionRewards(lp2, 60, 300, liq2);
uint256 positionRewardsUpperTick180= positionRewards(lp2, 60, 180, liq2);
assertEq(positionRewardsUpperTick180, 0);
// the position with 300 as the upper tick was initialised with non-zero rewards
assertGt(positionRewardsUpperTick300, 0);
}
Recommendation: Consider initialising to the way Uniswap does, to the global growth outside value.
However, this will affect the way feeGrowthInside and pastRewards is calculated too.
Sorella: Fixed in commit 26db3bbd, requiring several changes:
• Initializing tick growth-outside-accumulators that are below or at the current to the global accumu-
lator (just as is done in Uniswap V4).
• Making sure relevant arithmetic is unchecked to allow for wrapping based on how relevant accumu-
lators are initialized.
Swap out Solady 's "WAD Math" (ﬁxed point arithmetic with a base of 10**18 ) with so-called "x128"
math, ﬁxed point arithmetic with a base of 2**128 . This was necessary due to large rounding errors
diminishing LP rewards discovered during further testing.
Spearbit: Fixed. Consider having cumulativeGrowth and globalGrowth math to be unchecked as well, to
be aligned with Uniswap. Accumulation overﬂows once reward accumulation exceeds type(uint128).max ,
though it take a long time before it occurs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sorella Angstrom |
| Report Date | N/A |
| Finders | Milotruck, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sorella-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sorella-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

