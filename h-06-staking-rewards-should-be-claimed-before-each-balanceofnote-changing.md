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
solodit_id: 41693
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
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

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-06] Staking rewards should be claimed before each `balanceOfNote` changing

### Overview


This bug report is about a medium severity bug that has a high likelihood of occurring. The `claimRewards` function is not being invoked when the `balanceOfNote` changes, which can lead to incorrect calculations and cause losses in assets. The recommendation is to claim rewards for notes with `stakes[noteId].isStaked == true` before any changes are made to the `balanceOfNote`. This should be done before any of the following functions are called: `deposit`, `withdraw`, `mintDyad`, `burnDyad`, `liquidate` (for both `id` and `to` notes).

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Since staking rewards depend on `balanceOfNote` the `claimRewards` function should be invoked on each `balanceOfNote` changing. But this functionality is not implemented. This way reward can be calculated incorrectly which can cause sufficient asset losses.

```solidity
    function _calculateRewards(uint256 noteId, StakeInfo storage stakeInfo) internal view returns (uint256) {
        uint256 timeDiff = block.timestamp - stakeInfo.lastRewardTime;

>>      uint256 xp = dyadXP.balanceOfNote(noteId);

>>      return timeDiff * rewardsRate * stakeInfo.liquidity * xp;
    }
```

## Recommendations

Consider claiming rewards for notes with `stakes[noteId].isStaked == true` before any `balanceOfNote` changing: `deposit`, `withdraw`, `mintDyad`, `burnDyad`, `liquidate` (for both `id` and `to` notes).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

