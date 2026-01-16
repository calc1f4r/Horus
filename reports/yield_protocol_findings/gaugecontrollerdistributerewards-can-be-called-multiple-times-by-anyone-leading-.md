---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57218
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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

# Audit Details
report_date: unknown
finders_count: 18
finders:
  - patitonar
  - pyro
  - io10
  - lamsy
  - robertodf99
---

## Vulnerability Title

`GaugeController::distributeRewards` can be called multiple times by anyone, leading to excessive reward distribution

### Overview


The `GaugeController::distributeRewards` function can be called multiple times by anyone, allowing malicious users to distribute excessive rewards to a gauge within a short period of time. This can have negative effects on the token value and sustainability of the protocol. The vulnerability can be fixed by adding a time-based check to prevent frequent reward distributions.

### Original Finding Content

## Summary

The `distributeRewards` function in `GaugeController` can be called multiple times by anyone, allowing malicious users to trigger multiple reward distributions to a gauge within the same period.

## Vulnerability Details

The `distributeRewards` function lacks a time-based check between reward distributions. This means anyone can call it repeatedly to distribute rewards to a gauge multiple times, even if the gauge has already received rewards for the current period.

Key issues:

* No minimum time delay between reward distributions
* No tracking of last reward distribution time
* Function is callable by any address
* Each call calculates and distributes new rewards

## Impact

This vulnerability allows excessive rewards to be distributed to gauges:

* Gauges receive more rewards than intended by the protocol's tokenomics
* Token emissions exceed planned schedule
* Economic impact on token value and protocol sustainability
* Unfair advantage to gauges that get called more frequently

## Tools Used

Manual review

## Proof of Concept

Add the following test case to the `test/unit/core/governance/gauges/GaugeController.test.js` file:

```javascript
it("should demonstrate multiple reward distributions", async () => {
    // mint reward token to gauge to be able to distribute rewards
    await rewardToken.mint(rwaGauge.target, ethers.parseEther("100000000000000000000"));
    // mint veRAAC token to user to be able to vote
    await veRAACToken.mint(user1.address, ethers.parseEther("1000"));
    // vote for rwa gauge
    await gaugeController.connect(user1).vote(await rwaGauge.getAddress(), 5000);

    const initialPeriodState = await rwaGauge.periodState();
    const initialLastUpdateTime = await rwaGauge.lastUpdateTime();

    // No reward distribution yet
    expect(initialLastUpdateTime).to.be.eq(0);
    expect(initialPeriodState.distributed).to.be.eq(0);

    // First legitimate distribution
    await gaugeController.distributeRewards(rwaGauge.target);

    const rewardsToDistribute = ethers.parseEther("500000");
    
    const firstPeriodState = await rwaGauge.periodState();
    const firstLastUpdateTime = await rwaGauge.lastUpdateTime();

    const timeFirstReward = await time.latest();

    expect(firstLastUpdateTime).to.be.equal(timeFirstReward);
    expect(firstPeriodState.distributed).to.be.equal(rewardsToDistribute);

    // Second distribution
    await gaugeController.distributeRewards(rwaGauge.target);

    const secondPeriodState = await rwaGauge.periodState();
    const secondLastUpdateTime = await rwaGauge.lastUpdateTime();

    const timeSecondReward = await time.latest();

    expect(secondLastUpdateTime).to.be.equal(timeSecondReward);
    expect(secondPeriodState.distributed).to.be.equal(rewardsToDistribute * 2n);

    // Third distribution
    await gaugeController.distributeRewards(rwaGauge.target);

    const thirdPeriodState = await rwaGauge.periodState();
    const thirdLastUpdateTime = await rwaGauge.lastUpdateTime();

    const timeThirdReward = await time.latest();

    expect(thirdLastUpdateTime).to.be.equal(timeThirdReward);
    expect(thirdPeriodState.distributed).to.be.equal(rewardsToDistribute * 3n);

    const getPeriodDuration = await rwaGauge.getPeriodDuration();
    expect(getPeriodDuration).to.be.equal(MONTH);

    // check that period duration is greater than time between first and third reward
    expect(getPeriodDuration).to.be.gt(timeThirdReward - timeFirstReward);
});
```

## Recommendations

Add time-based checks to prevent frequent reward distributions:

```diff
function distributeRewards(
        address gauge
    ) external override nonReentrant whenNotPaused {
    if (!isGauge(gauge)) revert GaugeNotFound();
    if (!gauges[gauge].isActive) revert GaugeNotActive();

+   Gauge storage g = gauges[gauge];
+   uint256 timeSinceLastReward = block.timestamp - g.lastRewardTime;
    
+   // Require minimum time between distributions based on gauge type
+   uint256 minRewardInterval = g.gaugeType == GaugeType.RWA ? 30 days : 7 days;
+   if (timeSinceLastReward < minRewardInterval) revert RewardPeriodNotElapsed();
    
    uint256 reward = _calculateReward(gauge);
    if (reward == 0) return;
    
    IGauge(gauge).notifyRewardAmount(reward);
    emit RewardDistributed(gauge, msg.sender, reward);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | patitonar, pyro, io10, lamsy, robertodf99, waydou, holydevoti0n, air, amow, x1485967, orangesantra, sl1, petargvr94, johnlaw, frndz0ne |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

