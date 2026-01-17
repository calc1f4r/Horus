---
# Core Classification
protocol: Concur Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1419
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/209

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
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-09] `StakingRewards.sol#notifyRewardAmount()` Improper reward balance checks can make some users unable to withdraw their rewards

### Overview


This bug report is about an issue found in the smart contract code of the StakingRewards.sol file. The issue is that the contract only checks if the balance of rewardsToken is greater than or equal to the future rewards. This means that if the rewardsDistribution mistakenly sends a larger amount, some users may not be able to claim their rewards. 

A proof of concept (PoC) is provided to demonstrate how the issue can occur. In the PoC, Alice stakes 1,000 stakingToken, the rewardsDistribution sends 100 rewardsToken to the contract, and the rewardsDistribution calls notifyRewardAmount() with an amount of 100. Seven days later, Alice calls earned() and it returns 100 rewardsToken, but Alice does not getReward(). The rewardsDistribution then calls notifyRewardAmount() with an amount of 100 without sending any funds to the contract. Seven days later, Alice calls earned() and it returns 200 rewardsToken, but when Alice tries to call getReward(), the transaction fails due to insufficient balance of rewardsToken.

The expected result of the PoC is that the transaction in step 5 should revert. 

The recommendation is to change the function notifyRewardAmount to addRward and use transferFrom to transfer rewardsToken into the contract. This would ensure that the contract has enough amount of rewardsToken and users can claim their rewards.

### Original Finding Content

_Submitted by WatchPug_

[StakingRewards.sol#L154-L158](https://github.com/code-423n4/2022-02-concur/blob/72b5216bfeaa7c52983060ebfc56e72e0aa8e3b0/contracts/StakingRewards.sol#L154-L158)<br>

```solidity
    uint256 balance = rewardsToken.balanceOf(address(this));
    require(
        rewardRate <= balance / rewardsDuration,
        "Provided reward too high"
    );
```

In the current implementation, the contract only checks if balanceOf `rewardsToken` is greater than or equal to the future rewards.

However, under normal circumstances, since users can not withdraw all their rewards in time, the balance in the contract contains rewards that belong to the users but have not been withdrawn yet. This means the current checks can not be sufficient enough to make sure the contract has enough amount of rewardsToken.

As a result, if the `rewardsDistribution` mistakenly `notifyRewardAmount` with a larger amount, the contract may end up in a wrong state that makes some users unable to claim their rewards.

### Proof of Concept

Given:

*   rewardsDuration = 7 days;

1.  Alice stakes `1,000` stakingToken;
2.  `rewardsDistribution` sends `100` rewardsToken to the contract;
3.  `rewardsDistribution` calls `notifyRewardAmount()` with `amount` = `100`;
4.  7 days later, Alice calls `earned()` and it returns `100` rewardsToken, but Alice choose not to `getReward()` for now;
5.  `rewardsDistribution` calls `notifyRewardAmount()` with `amount` = `100` without send any fund to contract, the tx will succees;
6.  7 days later, Alice calls `earned()` `200` rewardsToken, when Alice tries to call `getReward()`, the transaction will fail due to insufficient balance of rewardsToken.

Expected Results:

The tx in step 5 should revert.

### Recommended Mitigation Steps

Consider changing the function `notifyRewardAmount` to `addRward` and use `transferFrom` to transfer rewardsToken into the contract:

```solidity
function addRward(uint256 reward)
    external
    updateReward(address(0))
{
    require(
        msg.sender == rewardsDistribution,
        "Caller is not RewardsDistribution contract"
    );

    if (block.timestamp >= periodFinish) {
        rewardRate = reward / rewardsDuration;
    } else {
        uint256 remaining = periodFinish - block.timestamp;
        uint256 leftover = remaining * rewardRate;
        rewardRate = (reward + leftover) / rewardsDuration;
    }

    rewardsToken.safeTransferFrom(msg.sender, address(this), reward);

    lastUpdateTime = block.timestamp;
    periodFinish = block.timestamp + rewardsDuration;
    emit RewardAdded(reward);
}
```

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/209)**

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-02-concur-findings/issues/209#issuecomment-1104079338):**
 > Given the code available, the warden has shown a possible scenario where certain depositors cannot receive reward tokens.
> 
> Because this is contingent on an improper configuration and because this relates to loss of Yield, I believe Medium Severity to be more appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Concur Finance |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/209
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`vulnerability`

