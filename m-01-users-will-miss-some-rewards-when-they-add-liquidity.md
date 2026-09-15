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
solodit_id: 41694
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

[M-01] Users will miss some rewards when they add liquidity

### Overview


The report is about a bug in the UniswapV3Staking contract, which stores the current liquidity when a user stakes their note. This value is then used to calculate rewards when the user claims them. However, if the user keeps adding liquidity to their position, the stored liquidity becomes stale and they receive fewer rewards than intended. The recommendation is to use the up-to-date liquidity instead of storing it to avoid this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In `UniswapV3Staking.stake`, the current liquidity is stored when a note is staked:

```solidity
    function stake(uint256 noteId, uint256 tokenId) external {
        require(dnft.ownerOf(noteId) == msg.sender, "You are not the Note owner");

        StakeInfo storage stakeInfo = stakes[noteId];
        require(!stakeInfo.isStaked, "Note already used for staking");

        (,,,,,,, uint128 liquidity,,,,) = positionManager.positions(tokenId);
        require(liquidity > 0, "No liquidity");

        positionManager.safeTransferFrom(msg.sender, address(this), tokenId);

        stakes[noteId] = StakeInfo({
->        liquidity: liquidity,
          lastRewardTime: block.timestamp,
          tokenId: tokenId,
          isStaked: true
        });

        emit Staked(msg.sender, noteId, tokenId, liquidity);
    }
```

This value will be used when they claim their rewards:

```solidity
    function _calculateRewards(uint256 noteId, StakeInfo storage stakeInfo) internal view returns (uint256) {
        uint256 timeDiff = block.timestamp - stakeInfo.lastRewardTime;

        uint256 xp = dyadXP.balanceOfNote(noteId);

->      return timeDiff * rewardsRate * stakeInfo.liquidity * xp;
    }
```

However, if a user keeps adding liquidity to their own position with `NonfungiblePositionManager.increaseLiquidity`, the liquidity will be stale, so they will receive fewer rewards than intended as it will use the original value (when they staked it).

## Recommendations

Consider using the up-to-date liquidity instead of storing it:

```diff
    function _calculateRewards(uint256 noteId, StakeInfo storage stakeInfo) internal view returns (uint256) {
        uint256 timeDiff = block.timestamp - stakeInfo.lastRewardTime;

        uint256 xp = dyadXP.balanceOfNote(noteId);

-       return timeDiff * rewardsRate * stakeInfo.liquidity * xp;
+       (,,,,,,, uint128 liquidity,,,,) = positionManager.positions(stakeInfo.tokenId);
+       return timeDiff * rewardsRate * liquidity * xp;
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

