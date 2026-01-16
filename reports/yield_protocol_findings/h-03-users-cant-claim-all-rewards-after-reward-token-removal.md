---
# Core Classification
protocol: Increment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31610
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Increment-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Users can't claim all rewards after reward token removal

### Overview


Summary:

The bug report is about a method called `removeRewardToken()` which is not properly accounting for pending but not yet accrued rewards. This means that when the method is used, it transfers too many tokens to governance and leaves users without their full rewards. The severity of this bug is high as it affects users' ability to claim their rewards, and the likelihood is medium as token removal is not a common operation but can still happen. The recommended solution is to leave enough tokens in reserve after removal to cover current rewards, but the fix is not straightforward due to other factors that affect the calculation of rewards. 

### Original Finding Content

**Severity**

**Impact:** High, there are always users who can't claim reward

**Likelihood:** Medium, token removal is not a usual operation but is possible

**Description**

There is a method `removeRewardToken()` which leaves only accrued but not yet claimed rewards in reserve, transferring the other part to governance. The issue is that the method doesn't take into consideration pending but not yet accrued rewards.

Relevant code block:

```solidity
    function removeRewardToken(address _rewardToken) external onlyRole(GOVERNANCE) {
        ...
        // Determine how much of the removed token should be sent back to governance
        uint256 balance = _rewardTokenBalance(_rewardToken);
        uint256 unclaimedAccruals = _totalUnclaimedRewards[_rewardToken];
        uint256 unaccruedBalance;
        if (balance >= unclaimedAccruals) {
            unaccruedBalance = balance - unclaimedAccruals;
            // Transfer remaining tokens to governance (which is the sender)
            IERC20Metadata(_rewardToken).safeTransferFrom(ecosystemReserve, msg.sender, unaccruedBalance);
        }
    }
```

Variable `_totalUnclaimedRewards` is updated only on reward claim and position updates, therefore doesn't contain pending rewards

**Recommendations**

Leave enough tokens in reserve after token removal to cover current rewards to users. However fix is not obvious due to `earlyWithdrawalPenalty` and `rewardMultiplier` which depend on the user and can't be calculated in advance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Increment |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Increment-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

