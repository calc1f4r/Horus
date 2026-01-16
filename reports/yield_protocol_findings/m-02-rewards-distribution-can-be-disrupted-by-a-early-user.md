---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1352
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-yield-convex-contest
source_link: https://code4rena.com/reports/2022-01-yield
github_link: https://github.com/code-423n4/2022-01-yield-findings/issues/116

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-02] Rewards distribution can be disrupted by a early user

### Overview


A bug report has been filed regarding the reward distribution in the ConvexStakingWrapper.sol smart contract on the WatchPug platform. The bug occurs when a user mints a small amount of convexToken (e.g. 1 Wei) and transfers a large amount of reward_token (e.g. 5e18) to the contract, causing the reward.reward_integral to exceed the maximum value of uint128 and overflow, disrupting the rewards distribution.

The recommendation to fix this bug is to consider wrapping a certain amount of initial totalSupply (e.g. 1e8) and never burning it. Additionally, it is suggested to use uint256 instead of uint128 for reward.reward_integral and to lower the 1e20 value down to 1e12.

### Original Finding Content

_Submitted by WatchPug_

<https://github.com/code-423n4/2022-01-yield/blob/e946f40239b33812e54fafc700eb2298df1a2579/contracts/ConvexStakingWrapper.sol#L206-L224>

```solidity
function _calcRewardIntegral(
    uint256 _index,
    address[2] memory _accounts,
    uint256[2] memory _balances,
    uint256 _supply,
    bool _isClaim
) internal {
    RewardType storage reward = rewards[_index];

    uint256 rewardIntegral = reward.reward_integral;
    uint256 rewardRemaining = reward.reward_remaining;

    //get difference in balance and remaining rewards
    //getReward is unguarded so we use reward_remaining to keep track of how much was actually claimed
    uint256 bal = IERC20(reward.reward_token).balanceOf(address(this));
    if (_supply > 0 && (bal - rewardRemaining) > 0) {
        rewardIntegral = uint128(rewardIntegral) + uint128(((bal - rewardRemaining) * 1e20) / _supply);
        reward.reward_integral = uint128(rewardIntegral);
    }
```

`reward.reward_integral` is `uint128`, if a early user mint (wrap) just `1` Wei of `convexToken`, and make `_supply == 1`, and then tranferring `5e18` of `reward_token` to the contract.

As a result, `reward.reward_integral` can exceed `type(uint128).max` and overflow, causing the rewards distribution to be disrupted.

##### Recommendation

Consider `wrap` a certain amount of initial totalSupply, e.g. `1e8`, and never burn it. And consider using uint256 instead of uint128 for `reward.reward_integral`. Also, consdier lower `1e20` down to `1e12`.

**[alcueca (Yield) confirmed but disagreed with severity and commented](https://github.com/code-423n4/2022-01-yield-findings/issues/116#issuecomment-1028062625):**
 > Assets are not a direct risk if it is the first user disrupting the contract. We would need to redeploy better code, but that's it. I suggest this is reported as medium, as merits for a DoS attack.
> 
> As suggested elsewhere, the right solution if uint128 is to be used in storage, is to cast up to uint256 for calculations, and then back to uint128 to store again.

**[iamsahu (Yield) resolved](https://github.com/code-423n4/2022-01-yield-findings/issues/116)**

**[Alex the Entreprenerd (judge) changed severity from High to Medium and commented](https://github.com/code-423n4/2022-01-yield-findings/issues/116#issuecomment-1043687140):**
 > The warden identified a way an early depositor can grief the system, I believe the finding to be valid, and because:
> - It would conditionally disrupt the system
> - It would "brick the contract" at the loss of the griefer
> - No additional funds would be at risk
> 
> I believe medium severity to be appropriate



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-yield
- **GitHub**: https://github.com/code-423n4/2022-01-yield-findings/issues/116
- **Contest**: https://code4rena.com/contests/2022-01-yield-convex-contest

### Keywords for Search

`vulnerability`

