---
# Core Classification
protocol: Ajna Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20090
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-ajna
source_link: https://code4rena.com/reports/2023-05-ajna
github_link: https://github.com/code-423n4/2023-05-ajna-findings/issues/224

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
finders_count: 1
finders:
  - nobody2018
---

## Vulnerability Title

[M-11] `StandardFunding.fundingVote` should not allow users who didn't vote in screening stage to vote

### Overview


This bug report is about an issue in the code of the Ajna GrantFund contract, which is used to fund projects. The issue is that users who did not vote in the screening stage but voted in the funding stage are not allowed to claim rewards via the `claimDelegateReward` function. This is because voting in the funding stage locks the rewards to the caller, but there is no code to calculate the amount of these rewards that can never be claimed.

The code for the `StandardFunding.claimDelegateReward` function should be changed so that it checks whether the caller voted in the screening stage. This can be done by adding a line of code at the beginning of the function that reverts the transaction if the delegatee did not vote in the screening stage.

The `StandardFunding.fundingVote` function should also be changed so that it does not allow users who didn't vote in the screening stage. Alternatively, the code on line L240 can be deleted. 

This issue was confirmed by MikeHathaway (Ajna).

### Original Finding Content


<https://github.com/code-423n4/2023-05-ajna/blob/main/ajna-grants/src/grants/base/StandardFunding.sol#L519-L569><br>
<https://github.com/code-423n4/2023-05-ajna/blob/main/ajna-grants/src/grants/base/StandardFunding.sol#L519>

Users who did not vote in the screening stage but voted in the funding stage are not allowed to claim rewards via `claimDelegateReward`. **Voting in the funding stage will occupy the distribution ratio of rewards**. Since these rewards cannot be claimed, in the long run, the ajnaToken balance of the GrantFund contract is inconsistent with `treasury`.

### Proof of Concept

At the beginning of the `StandardFunding.claimDelegateReward` function, check whether the caller voted in the screening stage.

```solidity
function claimDelegateReward(
        uint24 distributionId_
    ) external override returns(uint256 rewardClaimed_) {
        // Revert if delegatee didn't vote in screening stage
->      if(screeningVotesCast[distributionId_][msg.sender] == 0) revert DelegateRewardInvalid();

        QuarterlyDistribution memory currentDistribution = _distributions[distributionId_];
        ...
    }
```

`StandardFunding.fundingVote` is used to vote in the funding stage. This function does not check whether the caller voted in the screening stage. `fundingVote` subcalls [\_fundingVote](https://github.com/code-423n4/2023-05-ajna/blob/main/ajna-grants/src/grants/base/StandardFunding.sol#L612), which affects the allocation of rewards. `_getDelegateReward` is used by `claimDelegateReward` to calculate the reward distributed to the caller.

```solidity
function _getDelegateReward(
        QuarterlyDistribution memory currentDistribution_,
        QuadraticVoter memory voter_
    ) internal pure returns (uint256 rewards_) {
        // calculate the total voting power available to the voter that was allocated in the funding stage
        uint256 votingPowerAllocatedByDelegatee = voter_.votingPower - voter_.remainingVotingPower;

        // if none of the voter's voting power was allocated, they receive no rewards
        if (votingPowerAllocatedByDelegatee == 0) return 0;

        // calculate reward
        // delegateeReward = 10 % of GBC distributed as per delegatee Voting power allocated
->      rewards_ = Maths.wdiv(
            Maths.wmul(
                currentDistribution_.fundsAvailable,	//total funds in current distribution
                votingPowerAllocatedByDelegatee		//voter's vote power
            ),
            currentDistribution_.fundingVotePowerCast	//total vote power in current distribution
        ) / 10;						// 10% fundsAvailable
    }
```

As long as `fundingVote` is successfully called, it means that **the reward is locked to the caller**. However, the caller cannot claim these rewards. **There is no code to calculate the amount of these rewards that can never be claimed**.

### Recommended Mitigation Steps

Two ways to fix this problem:

1.  `FundingVote` does not allow users who didn't vote in screening stage.
2.  Delete the code on line [L240](https://github.com/code-423n4/2023-05-ajna/blob/main/ajna-grants/src/grants/base/StandardFunding.sol#L240).

**[MikeHathaway (Ajna) confirmed](https://github.com/code-423n4/2023-05-ajna-findings/issues/224#issuecomment-1555111296)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ajna Protocol |
| Report Date | N/A |
| Finders | nobody2018 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-ajna
- **GitHub**: https://github.com/code-423n4/2023-05-ajna-findings/issues/224
- **Contest**: https://code4rena.com/reports/2023-05-ajna

### Keywords for Search

`vulnerability`

