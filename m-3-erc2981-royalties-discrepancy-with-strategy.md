---
# Core Classification
protocol: TITLES Publishing Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33128
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/326
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-titles-judging/issues/144

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
finders_count: 3
finders:
  - ComposableSecurity
  - cducrest-brainbot
  - sammy
---

## Vulnerability Title

M-3: ERC2981 royalties discrepancy with strategy

### Overview


The bug report is about a discrepancy found in the code related to ERC2981 royalties. The function `setFeeStrategy()` and `publish()` in the `Edition.sol` file do not properly set the ERC2981 internal token royalty value. This can cause incorrect values to be returned and can lead to incorrect royalty payments. The bug was found through manual review and the recommendation is to call `_setTokenRoyalty()` at the end of `setFeeStrategy()`. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-titles-judging/issues/144 

## Found by 
ComposableSecurity, cducrest-brainbot, sammy
## Summary

In `Edition.sol`, functions that set the value of `works[tokenId].strategy` which includes `works[tokenId].strategy.royaltyBps` do not set ERC2981's internal token royalty value.

## Vulnerability Detail

The function `setFeeStrategy()` sets the public mapping value `works[tokenId_].strategy` which may update the `roylatyBps` value but does not call `_setTokenRoyalty(...)`:

```solidity
    function setFeeStrategy(uint256 tokenId_, Strategy calldata strategy_) external {
        if (msg.sender != works[tokenId_].creator) revert Unauthorized();
        works[tokenId_].strategy = FEE_MANAGER.validateStrategy(strategy_);  // @audit does not set royalties
    }
```

Similarly, the `publish()` function to create a new work sets the strategy but does not call `_setTokenRoyalty()`:

```solidity
    function publish(
        address creator_,
        uint256 maxSupply_,
        uint64 opensAt_,
        uint64 closesAt_,
        Node[] calldata attributions_,
        Strategy calldata strategy_,
        Metadata calldata metadata_
    ) external override onlyRoles(EDITION_MANAGER_ROLE) returns (uint256 tokenId) {
        tokenId = ++totalWorks;

        _metadata[tokenId] = metadata_;
        works[tokenId] = Work({
            creator: creator_,
            totalSupply: 0,
            maxSupply: maxSupply_,
            opensAt: opensAt_,
            closesAt: closesAt_,
            strategy: FEE_MANAGER.validateStrategy(strategy_)
        });

        Node memory _node = node(tokenId);
        for (uint256 i = 0; i < attributions_.length; i++) {
            // wake-disable-next-line reentrancy, unchecked-return-value
            GRAPH.createEdge(_node, attributions_[i], attributions_[i].data);
        }

        emit Published(address(this), tokenId);
    } 
```

This latter case may be less of a problem since `TitlesCore` calls `edition_.setRoyaltyTarget()` right after publishing a new work. However it remains a problem if publishers are expected to interact directly with `Edition` and not only through `TitlesCore`

## Impact

The value returned by `works[tokenId].strategy.royaltyBps` and `ERC2981.royaltyInfo(tokenId, salePrice)` will not be coherent. Users may expect to set a certain royalty bps while the value is not updated. Core values used for royalty payments may become incorrect after updates.

## Code Snippet

https://github.com/vectorized/solady/blob/main/src/tokens/ERC2981.sol

https://github.com/sherlock-audit/2024-04-titles/blob/d7f60952df22da00b772db5d3a8272a988546089/wallflower-contract-v2/src/editions/Edition.sol#L368-L371

https://github.com/sherlock-audit/2024-04-titles/blob/d7f60952df22da00b772db5d3a8272a988546089/wallflower-contract-v2/src/editions/Edition.sol#L121

## Tool used

Manual Review

## Recommendation

Call `_setTokenRoyalty(tokenId, FeeManager.feeReceiver(address(this), tokenId), works[tokenId].strategy.royaltyBps);` at the end of `setFeeStrategy()`. 



## Discussion

**pqseags**

This is valid and should be fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | TITLES Publishing Protocol |
| Report Date | N/A |
| Finders | ComposableSecurity, cducrest-brainbot, sammy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-titles-judging/issues/144
- **Contest**: https://app.sherlock.xyz/audits/contests/326

### Keywords for Search

`vulnerability`

