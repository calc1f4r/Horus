---
# Core Classification
protocol: Ajna
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6293
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/105

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

H-7: ERC721Pool's mergeOrRemoveCollateral allows to remove collateral while auction is clearable

### Overview


This bug report is about an issue in the ERC721Pool contract, which is part of the Sherlock-Audit 2023-01-ajna-judging project. The issue was found by hyh and is related to the mergeOrRemoveCollateral() function, which allows users to remove collateral from the pool. The problem is that the function does not include a _revertIfAuctionClearable() check, which means that it allows users to remove collateral while the auction is still clearable. 

The impact of this issue is that collateral can be removed while the auction result can change the allocation of the collateral in the buckets, which means that the mergeOrRemoveCollateral() result will not correspond to the current state of the pool. This could result in either a lender who initiated the call benefiting at the expense of other bucket LPs, or vice versa. In either case, it is a gain for some LP at the expense of the others, and a distribution based on a stale pool state (i.e. without auction result).

The severity of this issue is high, as auctions are regular and so there is no low probability prerequisites. The recommendation is to add a _revertIfAuctionClearable() check to the mergeOrRemoveCollateral() function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/105 

## Found by 
hyh

## Summary

User facing mergeOrRemoveCollateral() can effectively remove collateral, but lacks _revertIfAuctionClearable() check, i.e. allows to remove it while auction wasn't cleared.

## Vulnerability Detail

mergeOrRemoveCollateral() can remove collateral funds from the pool with _transferFromPoolToAddress() when the amount requested has been merged. As settling the auction can alter the collateral in some buckets its removal is generally restricted in the protocol when auction wasn't yet cleared.

## Impact

Collateral can be removed while auction result can change the allocation of the collateral in the buckets, i.e. can alter collateral amount per LP shares. This way mergeOrRemoveCollateral() result will not correspond to the current state of the pool and will lead to either a lender who initiated the call benefiting at the expense of other bucket LPs or vice versa, caller will have less collateral for the LP shares spent as some will be added to the bucket as a result of auction settlement.

Either way it is a gain for some LP at the expense of the others and a distribution based on a stale pool state (i.e. without auction result). As mergeOrRemoveCollateral() can be called by a lender at will an attacker will use it exactly when it is beneficial, at the expense of other participants.

Due to that setting the severity to be high as auctions are regular and so there is no low probability prerequisites.

## Code Snippet

mergeOrRemoveCollateral() allows for removing a collateral when the auction is clearable: 

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L280-L322

```solidity
    function mergeOrRemoveCollateral(
        uint256[] calldata removalIndexes_,
        uint256 noOfNFTsToRemove_,
        uint256 toIndex_
    ) external override nonReentrant returns (uint256 collateralMerged_, uint256 bucketLPs_) {
        PoolState memory poolState = _accruePoolInterest();
        uint256 collateralAmount = Maths.wad(noOfNFTsToRemove_);

        (
            collateralMerged_,
            bucketLPs_
        ) = LenderActions.mergeOrRemoveCollateral(
            buckets,
            deposits,
            removalIndexes_,
            collateralAmount,
            toIndex_
        );

        emit MergeOrRemoveCollateralNFT(msg.sender, collateralMerged_, bucketLPs_);

        // update pool interest rate state
        _updateInterestState(poolState, _lup(poolState.debt));

        if (collateralMerged_ == collateralAmount) {
            // Total collateral in buckets meets the requested removal amount, noOfNFTsToRemove_
            _transferFromPoolToAddress(msg.sender, bucketTokenIds, noOfNFTsToRemove_);
        }

    }

    /**
     *  @inheritdoc IPoolLenderActions
     *  @dev write state:
     *          - update bucketTokenIds arrays
     *  @dev emit events:
     *          - RemoveCollateral
     */
    function removeCollateral(
        uint256 noOfNFTsToRemove_,
        uint256 index_
    ) external override nonReentrant returns (uint256 collateralAmount_, uint256 lpAmount_) {
        _revertIfAuctionClearable(auctions, loans);
```

_revertIfAuctionClearable() checks whether pool state is ready to be altered by a result of the current auction:

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/libraries/helpers/RevertsHelper.sol#L47-L59

```solidity
    function _revertIfAuctionClearable(
        AuctionsState storage auctions_,
        LoansState    storage loans_
    ) view {
        address head     = auctions_.head;
        uint256 kickTime = auctions_.liquidations[head].kickTime;
        if (kickTime != 0) {
            if (block.timestamp - kickTime > 72 hours) revert AuctionNotCleared();

            Borrower storage borrower = loans_.borrowers[head];
            if (borrower.t0Debt != 0 && borrower.collateral == 0) revert AuctionNotCleared();
        }
    }
```

## Tool used

Manual Review

## Recommendation

Consider adding the check:

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L280-L286

```solidity
    function mergeOrRemoveCollateral(
        uint256[] calldata removalIndexes_,
        uint256 noOfNFTsToRemove_,
        uint256 toIndex_
    ) external override nonReentrant returns (uint256 collateralMerged_, uint256 bucketLPs_) {
+       _revertIfAuctionClearable(auctions, loans);
        PoolState memory poolState = _accruePoolInterest();
        uint256 collateralAmount = Maths.wad(noOfNFTsToRemove_);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/105
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Business Logic`

