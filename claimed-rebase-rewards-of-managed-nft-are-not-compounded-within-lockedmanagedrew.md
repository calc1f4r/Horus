---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21380
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
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
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Claimed rebase rewards of managed NFT are not compounded within LockedManagedReward

### Overview


This bug report is about the rebase rewards of a managed NFT not being compounded within the LockedManagedRewards contract. When someone calls the RewardsDistributor.claim with a managed NFT, the rewards are locked via the VotingEscrow.depositFor function, but the VotingEscrow.depositFor function fails to notify the LockedManagedRewards contract of the incoming rewards, leading to the rewards not accruing in the LockedManagedRewards. This is a problem because the purpose of the LockedManagedRewards contract is to accrue rebase rewards so that users will receive their pro-rata portion of the rebase rewards when they withdraw their normal NFTs from the managed NFT.

The bug was fixed by modifying the depositFor function, so that it validates that the depositFor function cannot be called against a Locked NFT, and that if it is called against a Managed NFT, the deposited amount will be treated as locked rewards and it will notify the LockedManagedReward contract. It was also observed that the claimed rebase rewards of managed NFT are now compounded within the LockedManagedReward contract.

### Original Finding Content

## Severity: High Risk

## Context
- **Files**: 
  - VotingEscrow.sol#L165
  - RewardsDistributor.sol#L271

## Description
Rebase rewards of a managed NFT should be compounded within the `LockedManagedRewards` contract. However, this was not currently implemented.

When someone calls the `RewardsDistributor.claim` with a managed NFT, the claimed rebase rewards will be locked via the `VotingEscrow.depositFor` function (Refer to Line 277 below). However, the `VotingEscrow.depositFor` function fails to notify the `LockedManagedRewards` contract of the incoming rewards. Thus, the rewards do not accrue in the `LockedManagedRewards`.

```solidity
function claim(uint256 _tokenId) external returns (uint256) {
    if (block.timestamp >= timeCursor) _checkpointTotalSupply();
    uint256 _lastTokenTime = lastTokenTime;
    _lastTokenTime = (_lastTokenTime / WEEK) * WEEK;
    uint256 amount = _claim(_tokenId, _lastTokenTime);
    if (amount != 0) {
        IVotingEscrow(ve).depositFor(_tokenId, amount);
        tokenLastBalance -= amount;
    }
    return amount;
}
```

One of the purposes of the `LockedManagedRewards` contract is to accrue rebase rewards claimed by the managed NFT so that the users will receive their pro-rata portion of the rebase rewards based on their contribution to the managed NFT when they withdraw their normal NFTs from the managed NFT via the `VotingEscrow.withdrawManaged` function.

```solidity
/// @inheritdoc IVotingEscrow
function withdrawManaged(uint256 _tokenId) external nonReentrant {
    ..SNIP..
    uint256 _reward = IReward(_lockedManagedReward).earned(address(token), _tokenId);
    ..SNIP..
    // claim locked rewards (rebases + compounded reward)
    address[] memory rewards = new address[](1);
    rewards[0] = address(token);
    IReward(_lockedManagedReward).getReward(_tokenId, rewards);
}
```

If the rebase rewards are not accrued in the `LockedManagedRewards`, users will not receive their pro-rata portion of the rebase rewards during withdrawal.

## Recommendation
Ensure that rebase rewards claimed by a managed NFT are accrued to the `LockedManagedRewards` contract. The `depositFor` function could be modified so that any deposits to a managed NFT will notify the `LockedManagedRewards` contract.

## Acknowledgements
**Velodrome**: Acknowledged and will fix. Fixed in commit 632c36 and commit e98472.

**Spearbit**: Observed the following fixes in commit 632c36:
- Added validation to ensure that the `depositFor` function cannot be called against a locked NFT.
- If the `depositFor` function is called against a managed NFT, the deposited amount will be treated as locked rewards and it will notify the `LockedManagedReward` contract.

Observed the following fixes in commit e98472:
- `depositFor` function cannot be called with a locked NFT.
- Only `RewardDistributor` can call `depositFor` function with a managed NFT.
- If `depositFor` function is called with a managed NFT, the function will notify the `LockedManagedReward` contract.

Based on the above, it was observed that the claimed rebase rewards of the managed NFT are compounded within the `LockedManagedReward` contract. Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

