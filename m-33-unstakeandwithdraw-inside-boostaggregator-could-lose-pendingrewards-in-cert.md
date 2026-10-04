---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26102
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/287

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
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - said
  - Audinarey
  - T1MOH
---

## Vulnerability Title

[M-33] `unstakeAndWithdraw` inside `BoostAggregator` could lose `pendingRewards` in certain cases

### Overview


This bug report is about a bug in the `BoosAggregator`'s `unstakeAndWithdraw` function, which is triggered when a user tries to unstake their uniswap NFT position token from the staker and get the pending rewards. If the pendingRewards is lower than the DIVISIONER, the accounting update for protocolRewards and claim rewards for strategy will not happen. This can lead to reward loss. 

The recommended mitigation steps are to either just claim rewards to strategy without taking the protocol fee, or take the amount fully for the protocol. The bug has been addressed and confirmed by two members of the Maia team.

### Original Finding Content


When `BoosAggregator`'s `unstakeAndWithdraw` is triggered, it will try to unstake the uniswap NFT position token from the staker and get the pending rewards. If conditions are met, it will update the strategy and protocol rewards accounting, claim the rewards for strategy and finally, withdraw the NFT position tokens from the staker. However, if `pendingRewards` is lower than `DIVISIONER`, the accounting will not happen and can cause reward loss.

### Proof of Concept

Inside `unstakeAndWithdraw`, if `pendingRewards` is lower than `DIVISIONER`, the accounting update for `protocolRewards` and claim rewards for strategy will not happen:

<https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L109-L136>

```solidity
    function unstakeAndWithdraw(uint256 tokenId) external {
        address user = tokenIdToUser[tokenId];
        if (user != msg.sender) revert NotTokenIdOwner();

        // unstake NFT from Uniswap V3 Staker
        uniswapV3Staker.unstakeToken(tokenId);

        uint256 pendingRewards = uniswapV3Staker.tokenIdRewards(tokenId) - tokenIdRewards[tokenId];

        if (pendingRewards > DIVISIONER) {
            uint256 newProtocolRewards = (pendingRewards * protocolFee) / DIVISIONER;
            /// @dev protocol rewards stay in stake contract
            protocolRewards += newProtocolRewards;
            pendingRewards -= newProtocolRewards;

            address rewardsDepot = userToRewardsDepot[user];
            if (rewardsDepot != address(0)) {
                // claim rewards to user's rewardsDepot
                uniswapV3Staker.claimReward(rewardsDepot, pendingRewards);
            } else {
                // claim rewards to user
                uniswapV3Staker.claimReward(user, pendingRewards);
            }
        }

        // withdraw rewards from Uniswap V3 Staker
        uniswapV3Staker.withdrawToken(tokenId, user, "");
    }
```

However, when the token is staked again via `BoosAggregator` by sending the NFT position back, the `tokenIdRewards` rewards are updated, so the previous unaccounted rewards will be lost:

<https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L79-L93>

```solidity
    function onERC721Received(address, address from, uint256 tokenId, bytes calldata)
        external
        override
        onlyWhitelisted(from)
        returns (bytes4)
    {
        // update tokenIdRewards prior to staking
        tokenIdRewards[tokenId] = uniswapV3Staker.tokenIdRewards(tokenId);
        // map tokenId to user
        tokenIdToUser[tokenId] = from;
        // stake NFT to Uniswap V3 Staker
        nonfungiblePositionManager.safeTransferFrom(address(this), address(uniswapV3Staker), tokenId);

        return this.onERC721Received.selector;
    }
```

### Recommended Mitigation Steps

Two things can be done here, either just claim rewards to strategy without taking the protocol fee, or take the amount fully for the protocol.

### Assessed type

Error

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/287#issuecomment-1709218882):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/287).

**[0xBugsy (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/287#issuecomment-1719576951)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | said, Audinarey, T1MOH |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/287
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

