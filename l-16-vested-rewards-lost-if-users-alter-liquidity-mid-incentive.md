---
# Core Classification
protocol: Ouroboros_2025-06-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63462
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-16] Vested rewards lost if users alter liquidity mid-incentive

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

When users stake their UniV3 positions in the `UniswapV3Staker` contract to earn some rewards, the owner creates incentives with a certain tick range and a vesting period, where the pool's price needs to stay in the range for a certain period of time to earn rewards. This period of time is called the vesting period.
If the time inside the ticks is < the vesting period while the incentive is active, the user will not be able to claim 100% of the rewards, but only a fraction of it.

```solidity
if (params.vestingPeriod <= params.secondsInside - params.secondsInsideInitial) {
    reward = maxReward;
} else {
    reward = maxReward * (params.secondsInside - params.secondsInsideInitial) / params.vestingPeriod;
}
```

On the other hand, users are allowed to increase their liquidity in the staked position at any time, which claims any pending rewards for the user, so that it is claimed according to the old liquidity amount. The next unstake will then claim the rewards according to the new liquidity amount, which works as expected. When increasing the liquidity, the protocol unstakes, then stakes the position again with the new liquidity amount, which automatically claims the pending rewards using the vesting logic above.
However, this contains a serious flaw, as unstake calculates the acucmlated rewards based on the time inside the ticks, and checks against the vesting period, and when increasing liquidity there's a very high chance that the vesting period is not met, which means that the user will not be able to claim 100% of the rewards, but only a fraction of it. 
This is a problem because the user has already staked the position for a certain amount of time, didn't unstake early, doesn't want to unstake early, and the price is still in range, and could stay the whole period, but still gets a fraction of the rewards, which is not what the user expects.

This leads to a loss of rewards for the user, as the other portion will be locked to be claimed later by the incentive refundee.

**Proof of Concept:**

Add the following test in `test/UniswapV3Staker.integration.spec.ts`, `time goes past the incentive end time`:

```typescript
it("increase liquidity - wrongly cutting vested rewards", async () => {
  const {
    subject: {
      createIncentiveResult,
      context: { nft, staker, token0, token1 },
      stakes: [{ tokenId }],
    },
    lpUsers: [lpUser0],
    amountDesired,
  } = { subject, lpUsers: actors.lpUsers(), amountDesired: BNe18(100) };
  const incentiveId = await subject.helpers.getIncentiveId(
    createIncentiveResult
  );

  await e20h.ensureBalancesAndApprovals(
    lpUser0,
    [token0, token1],
    amountDesired.mul(10),
    nft.address
  );

  await Time.setAndMine((await blockTimestamp()) + duration / 2);

  await token0.connect(lpUser0).approve(staker.address, amountDesired);
  await token1.connect(lpUser0).approve(staker.address, amountDesired);

  await staker
    .connect(lpUser0)
    .increaseLiquidity(
      tokenId,
      amountDesired,
      amountDesired,
      0,
      0,
      (await blockTimestamp()) + 1
    );

  await Time.set(createIncentiveResult.endTime + 1);

  await staker
    .connect(lpUser0)
    .unstakeToken(
      incentiveResultToStakeAdapter(createIncentiveResult),
      tokenId
    );

  // Total locked rewards > 0, knowing that the user didn't unstake early, and the price was in range the whole period
  expect((await staker.incentives(incentiveId)).totalRewardLocked).be.gt(0);
});
```

## Recommendations

The mitigation is non-trivial, as the current vesting mechanism penalizes any liquidity restaking—even when users intend to maintain their position for the full duration. This creates a mismatch between user expectations and protocol behavior.

Consider rethinking the vesting logic to avoid prematurely cutting rewards during liquidity modifications. One potential approach is to prorate vesting based on both:

* `secondsInside - secondsInsideInitial` (as currently implemented), and
* the elapsed time since `incentive.startTime`.




### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2025-06-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

