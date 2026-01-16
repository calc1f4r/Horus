---
# Core Classification
protocol: Rubicon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48942
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 68
finders:
  - 0xStalin
  - sinarette
  - J4de
  - AlexCzm
  - jasonxiale
---

## Vulnerability Title

[H-03] Reward accounting is incorrect in `BathBuddy` contract

### Overview


The BathBuddy contract, which rewards liquidity providers for holding BathTokens, has a critical flaw in its implementation. Unlike the similar Synthetix contract, the BathBuddy contract does not account for rewards when tokens are minted, burned, or transferred. This means that rewards are not correctly distributed to holders of BathTokens. There are two possible solutions to this issue - adding staking and withdrawing functions to the BathBuddy contract, or modifying the BathToken contract to trigger updates in the BathBuddy contract when tokens are modified. 

### Original Finding Content


The `BathBuddy` contracts implements rewards for liquidity providers (holders of `BathToken`). The contract is modeled after the famous Synthetix staking contract, with some tweaks to support rewards for multiple tokens at the same time.

The implementation overall is correct; however, there is a critical difference with the Synthetix contract that is ignored in the `BathBuddy` contract. In the Synthetix implementation, the main actions related to rewards accounting are the `stake` and `withdraw` actions. These trigger the `updateReward` modifier to ensure correct reward accounting. Staked tokens cannot be transferred, as these are held in the staking contract. In the `BathBuddy` implementation, things are very different as there is no staking. Rewards are intended to be distributed directly to holders of the `BathToken` without any need of staking the tokens in the contract. This means that, as there is no "staking" action in the `BathBuddy` implementation (i.e. depositing funds in the contract), rewards fail to be correctly accounted whenever   `BathToken` are minted, burned or transferred between different accounts.

These are two critical places in the code where the `BathBuddy` contract uses the state from the `BathToken`, but fails to be triggered whenever the state in the `BathToken` is modified. The first is `rewardPerToken`, which calculates the amount of rewards that should correspond to one unit of the `BathToken` token. This is logically dependent on the total supply of the token (lines 124 and 133):

<https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/periphery/BathBuddy.sol#L121-L135>

```solidity
121:     function rewardPerToken(address token) public view returns (uint256) {
122:         require(friendshipStarted, "I have not started a bathToken friendship");
123: 
124:         if (IERC20(myBathTokenBuddy).totalSupply() == 0) {
125:             return rewardsPerTokensStored[token];
126:         }
127:         return
128:             rewardsPerTokensStored[token].add(
129:                 lastTimeRewardApplicable(token)
130:                     .sub(lastUpdateTime[token])
131:                     .mul(rewardRates[token])
132:                     .mul(1e18)
133:                     .div(IERC20(myBathTokenBuddy).totalSupply())
134:             );
135:     }
```

The other place is in the `earned` function which uses the `BathToken` `balanceOf` function of an account (lines 146-147):

<https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/periphery/BathBuddy.sol#L139-L161>

```solidity
139:     function earned(
140:         address account,
141:         address token
142:     ) public view override returns (uint256) {
143:         require(friendshipStarted, "I have not started a bathToken friendship");
144: 
145:         return
146:             IERC20(myBathTokenBuddy) // Care with this?
147:                 .balanceOf(account)
148:                 .mul(
149:                     rewardPerToken(token).sub(
150:                         userRewardsPerTokenPaid[token][account]
151:                     )
152:                 )
153:                 .div(1e18)
154:                 .add(tokenRewards[token][account]);
155:     }
156: 
157:     function getRewardForDuration(
158:         address token
159:     ) external view returns (uint256) {
160:         return rewardRates[token].mul(rewardsDuration[token]);
161:     }
```

Since the whole `BathBuddy` contract is dependent on the total supply and account balance state of the paired `BathToken` contract, the following actions in the token should update the rewards state in `BathBuddy`:

*   `mint` and `burn`, as these modify the total supply of the token and the balances of the account whose tokens are minted or burned.
*   `transfer` and `transferFrom`, as these modify the balances of the sender and recipient accounts.

As the `BathBuddy` `updateReward` modifier fails to be triggered when the mentioned state in the `BathToken` is modified, reward accounting will be incorrect for many different scenarios. We'll explore one of these in the next section.

### Proof of Concept

In the following test, we demonstrate one of the possible scenarios where reward accounting is broken. This is a simple case in which rewards fail to be updated when a token transfer is executed. Alice has 1e18 `BathTokens`, at the middle of the rewards duration period she sends all her tokens to Bob. The expected outcome should be that Alice would earn half of the rewards, as she held the tokens for the half of the duration period. But when the duration period has ended, we call `getReward` for both Alice and Bob and we can see that Alice got nothing and Bob earned 100% of the rewards.

*Note: the snippet shows only the relevant code for the test. Full test file can be found [here](https://gist.github.com/romeroadrian/f3b7d6f9ab043340de7deb67a9c515e5).*

```solidity
function test_BathBuddy_IncorrectRewardAccounting() public {
    // Setup rewards
    uint256 startTime = block.timestamp;
    uint256 duration = 10_000 seconds;
    vm.prank(bathBuddyOwner);
    bathBuddy.setRewardsDuration(duration, address(rewardToken));

    uint256 rewardAmount = 100 ether;
    rewardToken.mint(address(bathBuddy), rewardAmount);
    vm.prank(bathBuddyOwner);
    bathBuddy.notifyRewardAmount(rewardAmount, rewardToken);

    // Mint bathTokens to Alice
    uint256 bathTokenAmount = 1 ether;
    bathToken.mint(alice, bathTokenAmount);

    // Simulate half of the duration time passes
    vm.warp(startTime + duration / 2);

    // Alice transfers tokens for Bob at middle of the period
    vm.prank(alice);
    bathToken.transfer(bob, bathTokenAmount);

    // Simulate complete duration time passes
    vm.warp(startTime + duration);

    // Trigger getRewards for Alice
    vm.prank(bathBuddyHouse);
    bathBuddy.getReward(rewardToken, alice);

    // Trigger getRewards for Bob
    vm.prank(bathBuddyHouse);
    bathBuddy.getReward(rewardToken, bob);

    // Alice gets nothings and Bob gets the full rewards, even though Alice held the tokens for half the duration time
    assertEq(rewardToken.balanceOf(alice), 0);
    assertEq(rewardToken.balanceOf(bob), rewardAmount);
}
```

### Recommendation

There are two recommended paths here. The easy path would be to just add the `stake` and `withdraw` functions to the `BathBuddy` contract similar to how the original `StakingRewards` contract works on Synthetix. However, this may change the original intention of the protocol as rewards won't be earned just by holding `BathTokens`, they will need to be staked (rewards will only be distributed to stakers).

The other path, and a bit more complex, would be to modify the `BathToken` contract (the `cToken`) so that burn, mint and transfer actions trigger the update on the paired `BathBuddy` contract.

**[daoio (Rubicon) confirmed](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279#issuecomment-1532544961)**

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279#issuecomment-1578131592):**
 > This write-up encapsulates the issues arising from forking the staking contract, but doing away with the staking portion through the usage of `balanceOf()` and `totalSupply()`.
> - No initialisation of `userRewardsPerTokenPaid`
> - Doesn't account for holding duration 

**[0xepley (warden) commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279#issuecomment-1590923406):**
 > I think that in the duplicate, two categories of issues have been merged into one.
> 
> So the two separate problems that have been merged into one are:
> 
> 1. Difference of implementation from synthetix, where there is no modifier on stake and withdraw. Hence, the calculation is flawed, leading to being able to claim the reward for whole duration by minting at the last moment, reducing others' rewards.
> 
> 2. Second, is the ability to transfer the token and claim (again and again, etc) until the contract is drained.
> 
> Both are different issues and require different solutions.
> 
> Just for example, two marked duplicates are: [#1074](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1074) and [#1168](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1168). Each explain separate issues of uneven distribution and draining.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279#issuecomment-1590933212):**
 > (2) is enabled by (1). 
> 
> The removal of staking & withdrawing (1) also led to the removal of initialisation of the `rewardsPerToken`, which allows you to do (2).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | 0xStalin, sinarette, J4de, AlexCzm, jasonxiale, markus\_ether, Dug, kaden, Ace-30, Emmanuel, 0xTheC0der, nobody2018, bytes032, shalaamum, Delvir0, mjmoonwalker, carrotsmuggler, Juntao, zhuXKET, rbserver, RedTiger, yellowBirdy, joestakey, T1MOH, 0xmichalis, SpicyMeatball, teddav, KingNFT, ktg, ljmanini, adriro, 0xDING99YA, 117l11, ast3ros, Lilyjjo, Banditx0x, nirlin, cducrest, SaeedAlipoor01988, immeas, cccz, sces60107, lopotras, Lirios, chaduke, mrpathfindr, dontonka, 0Kage, kutugu, Fanz, John, \_\_141345\_\_, Toshii, dec3ntraliz3d, rvierdiiev, R2 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1279
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

