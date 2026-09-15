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
solodit_id: 21379
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

Rebase rewards cannot be claimed after a veNFT expires

### Overview


This bug report is about the RewardsDistributor.claim and RewardsDistributor.claimMany functions, which are used to claim rebase rewards. When a user claims their rewards, the VotingEscrow.depositFor function is triggered. This function contains a require statement at line 812 which verifies that the veNFT performing the claim has not expired yet. If the veNFT's lock has expired, the function will revert and the accumulated rebase rewards will be stuck in the RewardsDistributor contract.

The recommendation is to consider sending the claimed VELO rewards to the owner of the veNFT if the veNFT's lock has already expired. This has been fixed in commit 8a71a8 and verified by Spearbit.

### Original Finding Content

## Security Issue Report

## Severity
**High Risk**

## Context
- `RewardsDistributor.sol#L271`
- `RewardsDistributor.sol#L283`

## Description
> Note: This issue affects both the `RewardsDistributor.claim` and `RewardsDistributor.claimMany` functions.

A user will claim their rebase rewards via the `RewardsDistributor.claim` function, which will trigger the `VotingEscrow.depositFor` function.

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

Within the `VotingEscrow.depositFor` function, the require statement at line 812 below will verify that the `veNFT` performing the claim has not expired yet.

```solidity
function depositFor(uint256 _tokenId, uint256 _value) external nonReentrant {
    LockedBalance memory oldLocked = _locked[_tokenId];
    require(_value > 0, "VotingEscrow: zero amount");
    require(oldLocked.amount > 0, "VotingEscrow: no existing lock found");
    require(oldLocked.end > block.timestamp, "VotingEscrow: cannot add to expired lock, withdraw");
    _depositFor(_tokenId, _value, 0, oldLocked, DepositType.DEPOSIT_FOR_TYPE);
}
```

If a user claims the rebase rewards after their `veNFT`'s lock has expired, the `VotingEscrow.depositFor` function will always revert. As a result, the accumulated rebase rewards will be stuck in the `RewardsDistributor` contract, and users will not be able to retrieve them.

## Recommendation
Consider sending the claimed VELO rewards to the owner of the `veNFT` if the `veNFT`'s lock has already expired.

Updated code:

```solidity
function claim(uint256 _tokenId) external returns (uint256) {
    if (block.timestamp >= timeCursor) _checkpointTotalSupply();
    uint256 _lastTokenTime = lastTokenTime;
    _lastTokenTime = (_lastTokenTime / WEEK) * WEEK;
    uint256 amount = _claim(_tokenId, _lastTokenTime);
    if (amount != 0) {
        IVotingEscrow.LockedBalance memory _locked = IVotingEscrow(ve).locked(_tokenId);
        if (_locked.end < block.timestamp) {
            address _nftOwner = IVotingEscrow(ve).ownerOf(_tokenId);
            IERC20(token).transfer(_nftOwner, amount);
        } else {
            IVotingEscrow(ve).depositFor(_tokenId, amount);
        }
        tokenLastBalance -= amount;
    }
    return amount;
}
```

## Status
- **Velodrome**: Fixed in commit `8a71a8`.
- **Spearbit**: Verified.

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

