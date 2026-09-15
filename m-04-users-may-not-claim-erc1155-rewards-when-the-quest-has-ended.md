---
# Core Classification
protocol: RabbitHole
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8855
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/528

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 35
finders:
  - HollaDieWaldfee
  - AlexCzm
  - 0xMirce
  - holme
  - BClabs
---

## Vulnerability Title

[M-04] Users may not claim Erc1155 rewards when the Quest has ended

### Overview


This bug report is about a vulnerability in the Erc1155Quest.sol contract from the Quest Protocol. The vulnerability is that when the Quest time has ended, the owner of the contract is able to withdraw the remaining tokens from the contract without deducting the unclaimed tokens. This means that when a user attempts to call the inherited claim() from Quest.sol, the call will fail because the token balance of the contract is zero. 

The impact of this vulnerability is that users will be denied of service when attempting to call the inherited claim() from Quest.sol. The bug was identified using manual inspection. 

The recommended mitigation steps are to refactor the withdrawRemainingTokens() function to deduct the unclaimed tokens before transferring the remaining tokens from the contract. This will ensure that the users are able to call the claim() function even after the Quest time has ended.

### Original Finding Content


<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc1155Quest.sol#L60><br>
<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Quest.sol#L114><br>
<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc1155Quest.sol#L41-L43>

Unlike Erc20Quest.sol, owner of Erc1155Quest.sol is going to withdraw the remaining tokens from the contract when `block.timestamp == endTime` without deducting the `unclaimedTokens`. As a result, users will be denied of service when attempting to call the inherited `claim()` from Quest.sol.

### Proof of Concept

As can be seen from the code block below, when the Quest time has ended, `withdrawRemainingTokens()` is going to withdraw the remaining tokens from the contract on line 60:

[File: Erc1155Quest.sol#L52-L63](https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc1155Quest.sol#L52-L63)

```solidity
    /// @dev Withdraws the remaining tokens from the contract. Only able to be called by owner
    /// @param to_ The address to send the remaining tokens to
    function withdrawRemainingTokens(address to_) public override onlyOwner {
        super.withdrawRemainingTokens(to_);
        IERC1155(rewardToken).safeTransferFrom(
            address(this),
            to_,
            rewardAmountInWeiOrTokenId,
60:            IERC1155(rewardToken).balanceOf(address(this), rewardAmountInWeiOrTokenId),
            '0x00'
        );
    }
```

When a user tries to call `claim()` below, line 114 is going to internally invoke `_transferRewards()`:

[File: Quest.sol#L94-L118](https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Quest.sol#L94-L118)

```solidity
    /// @notice Allows user to claim the rewards entitled to them
    /// @dev User can claim based on the (unclaimed) number of tokens they own of the Quest
    function claim() public virtual onlyQuestActive {
        if (isPaused) revert QuestPaused();

        uint[] memory tokens = rabbitHoleReceiptContract.getOwnedTokenIdsOfQuest(questId, msg.sender);

        if (tokens.length == 0) revert NoTokensToClaim();

        uint256 redeemableTokenCount = 0;
        for (uint i = 0; i < tokens.length; i++) {
            if (!isClaimed(tokens[i])) {
                redeemableTokenCount++;
            }
        }

        if (redeemableTokenCount == 0) revert AlreadyClaimed();

        uint256 totalRedeemableRewards = _calculateRewards(redeemableTokenCount);
        _setClaimed(tokens);
114:        _transferRewards(totalRedeemableRewards);
        redeemedTokens += redeemableTokenCount;

        emit Claimed(msg.sender, totalRedeemableRewards);
    }
```

`safeTransferFrom()` is going to revert on line 42 because the token balance of the contract is now zero. i.e. less than `amount_`:

[File: Erc1155Quest.sol#L39-L43](https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc1155Quest.sol#L39-L43)

```solidity
    /// @dev Transfers the reward token `rewardAmountInWeiOrTokenId` to the msg.sender
    /// @param amount_ The amount of reward tokens to transfer
    function _transferRewards(uint256 amount_) internal override {
42:        IERC1155(rewardToken).safeTransferFrom(address(this), msg.sender, rewardAmountInWeiOrTokenId, amount_, '0x00');
    }
```

### Recommended Mitigation Steps

Consider refactoring `withdrawRemainingTokens()` as follows:

(Note: The contract will have to separately import {QuestFactory} from './QuestFactory.sol' and initialize `questFactoryContract`.

```diff
+    function receiptRedeemers() public view returns (uint256) {
+        return questFactoryContract.getNumberMinted(questId);
+    }

    function withdrawRemainingTokens(address to_) public override onlyOwner {
        super.withdrawRemainingTokens(to_);

+        uint unclaimedTokens = (receiptRedeemers() - redeemedTokens)
+        uint256 nonClaimableTokens = IERC1155(rewardToken).balanceOf(address(this), rewardAmountInWeiOrTokenId) - unclaimedTokens;
        IERC1155(rewardToken).safeTransferFrom(
            address(this),
            to_,
            rewardAmountInWeiOrTokenId,
-            IERC1155(rewardToken).balanceOf(address(this), rewardAmountInWeiOrTokenId),
+            nonClaimableTokens,
            '0x00'
        );
    }
```

**[kirk-baird (judge) increased severity to High](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/528#issuecomment-1425183624)**

**[waynehoover (RabbitHole) disagreed with severity and commented](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/528#issuecomment-1440959685):**
 > I agree that this is an issue, but not a high risk issue. I expect high risk issues to be issues that can be called by anyone, not owners. 
> 
> As owners there are plenty of ways we can sabotage our contracts (for example via the set* functions) it is an issue for an owner. 
> 
> The owner understands how this function works, so they can be sure not to call it before all users have called claim.

**[kirk-baird (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/528#issuecomment-1442583850):**
 > Similarly to [`#122`](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/122), this is an `onlyOwner` function and therefore the likelihood is significantly reduce. Therefore I'm going to downgrade this issue to Medium.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | RabbitHole |
| Report Date | N/A |
| Finders | HollaDieWaldfee, AlexCzm, 0xMirce, holme, BClabs, usmannk, peanuts, rbserver, minhquanym, CodingNameKiki, adriro, AkshaySrivastav, Josiah, csanuragjain, hihen, cccz, peakbolt, RaymondFam, Aymen0909, wait, chaduke, zaskoh, KIntern_NA, MiniGlome, StErMi, omis, bin2chen, ElKu, gzeon, ubermensch, rvierdiiev, libratus, timongty |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/528
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`vulnerability`

