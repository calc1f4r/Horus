---
# Core Classification
protocol: Dyad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41695
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
github_link: none

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
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Reward time is updated even when no rewards are sent

### Overview


This bug report is about the `UniswapV3Staking` function which allows users to claim rewards. The issue is that even when users receive zero rewards, the `lastRewardTime` is still updated. This can cause problems when rewards are temporarily disabled and then re-enabled, as users will receive fewer rewards. The report suggests a change to the code to fix this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In `UniswapV3Staking` users can claim rewards by calling the `claimRewards` function. However, the `lastRewardTime` is always updated even when they get zero rewards:

```solidity
    function _claimRewards(uint256 noteId, StakeInfo storage stakeInfo, address recipient) internal {
        require(dnft.ownerOf(noteId) == msg.sender, "You are not the Note owner");
        require(stakeInfo.isStaked, "Note not staked");
        uint256 rewards = _calculateRewards(noteId, stakeInfo);
->      stakeInfo.lastRewardTime = block.timestamp;

        if (rewards > 0) {
            rewardsToken.transferFrom(rewardsTokenHolder, recipient, rewards);
            emit RewardClaimed(recipient, rewards);
        }
    }
```

Suppose the scenario where rewards are temporarily disabled by setting `rewardsRate` to zero. Then, any user that calls `claimRewards` during this period will update their `lastRewardTime` even if they don't get anything back. The next time, they will receive fewer rewards after they are enabled again.

## Recommendations

Consider applying the following change:

```diff
    function _claimRewards(uint256 noteId, StakeInfo storage stakeInfo, address recipient) internal {
        require(dnft.ownerOf(noteId) == msg.sender, "You are not the Note owner");
        require(stakeInfo.isStaked, "Note not staked");
        uint256 rewards = _calculateRewards(noteId, stakeInfo);
-       stakeInfo.lastRewardTime = block.timestamp;

        if (rewards > 0) {
+           stakeInfo.lastRewardTime = block.timestamp;
            rewardsToken.transferFrom(rewardsTokenHolder, recipient, rewards);
            emit RewardClaimed(recipient, rewards);
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

