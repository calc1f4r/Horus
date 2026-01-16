---
# Core Classification
protocol: Concur Finance
chain: everychain
category: uncategorized
vulnerability_type: revert_on_0_transfer

# Attack Vector Details
attack_type: revert_on_0_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1439
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/231

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
  - revert_on_0_transfer

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
  - hyh
---

## Vulnerability Title

[M-29] `ConvexStakingWrapper` deposits and withdraws will frequently be disabled if a token that doesn't allow zero value transfers will be added as a reward one

### Overview


This bug report is about the ConvexStakingWrapper contract which is located at https://github.com/code-423n4/2022-02-concur/blob/main/contracts/ConvexStakingWrapper.sol#L182. The impact of this bug is that if deposits and withdraws are done frequently enough, the reward update operation they invoke will deal mostly with the case when there is nothing to add yet, i.e. `reward.remaining` match the reward token balance. If the reward token doesn't allow for zero value transfers, the reward update function will fail on an empty incremental reward transfer, which is now done unconditionally, reverting the caller deposit/withdrawal functionality.

The proof of concept is that when ConvexStakingWrapper isn't paused, every deposit and withdraw update current rewards via `_checkpoint` function before proceeding. The `_checkpoint` calls `_calcRewardIntegral` for each of the reward tokens of the pid. The `_calcRewardIntegral` updates the incremental reward for the token, running the logic even if reward is zero, which is frequently the case. If the reward token doesn't allow zero value transfers, this transfer will fail, reverting the corresponding deposit or withdraw.

The recommended mitigation steps is to consider checking the reward before doing transfer (and the related computations as an efficiency measure). The code should be changed from `IERC20(reward.token).transfer(address(claimContract), d_reward);` to `if (d_reward > 0) IERC20(reward.token).transfer(address(claimContract), d_reward);`.

### Original Finding Content

_Submitted by hyh_

If deposits and withdraws are done frequently enough, the reward update operation they invoke will deal mostly with the case when there is nothing to add yet, i.e. `reward.remaining` match the reward token balance.

If reward token doesn't allow for zero value transfers, the reward update function will fail on an empty incremental reward transfer, which is now done unconditionally, reverting the caller deposit/withdrawal functionality

### Proof of Concept

When ConvexStakingWrapper isn't paused, every deposit and withdraw update current rewards via `_checkpoint` function before proceeding:

[ConvexStakingWrapper.sol#L233](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/ConvexStakingWrapper.sol#L233)<br>

[ConvexStakingWrapper.sol#L260](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/ConvexStakingWrapper.sol#L260)<br>

`_checkpoint` calls `_calcRewardIntegral` for each of the reward tokens of the pid:

[ConvexStakingWrapper.sol#L220](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/ConvexStakingWrapper.sol#L220)<br>

`_calcRewardIntegral` updates the incremental reward for the token, running the logic even if reward is zero, which is frequently the case:

[ConvexStakingWrapper.sol#L182](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/ConvexStakingWrapper.sol#L182)<br>

If the reward token doesn't allow zero value transfers, this transfer will fail, reverting the corresponding deposit or withdraw.

### Recommended Mitigation Steps

Consider checking the reward before doing transfer (and the related computations as an efficiency measure):

Now:

    IERC20(reward.token).transfer(address(claimContract), d_reward);

To be:

    if (d_reward > 0)
    	IERC20(reward.token).transfer(address(claimContract), d_reward);

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/231)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-concur-findings/issues/231#issuecomment-1103083291):**
 > The warden has shown how, due to a pattern that always transfers the reward token to the claim contract, in the case of a 0 transfer, certain transfers could fail, causing reverts.
> 
> While there can be an argument that this finding may not happen in reality, I believe that ultimately the system has been shown to be flawed in it's conception, perhaps adding a storage variable for the amount to claim would be more appropriate instead of dripping the rewards each time.
> 
> For that reason, and because the finding is contingent on a reward token that does revert on 0 transfer, I believe Medium Severity to be appropriate.



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
| Finders | hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/231
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`Revert On 0 Transfer`

