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
solodit_id: 8859
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/119

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
finders_count: 9
finders:
  - StErMi
  - rbserver
  - ElKu
  - ladboy233
  - CodingNameKiki
---

## Vulnerability Title

[M-08] Buyer on secondary NFT market can lose fund if they buy a NFT that is already used to claim the reward

### Overview


This bug report is about a vulnerability in the Quest Protocol that allows a buyer on a secondary NFT market to lose funds if they buy a NFT that is already used to claim a reward. The vulnerability is caused by a function in the Quest.sol smart contract called claim(). This function sets the NFT as claimed, preventing it from being used to claim the reward again, but does not prevent it from being traded in the secondary market. 

The bug can be exploited in the following way. User A has 1 NFT, which they can use to claim 1 ETH reward. User A then places a sell order in Opensea and sells the NFT for 0.9 ETH. User B sees the sell order and decides to buy the NFT. User A and B both submit their transactions at the same time, and User A's claim transaction executes first, meaning the reward goes to User A and the NFT ownership goes to User B. However, User B cannot claim the reward because it has already been claimed by User A.

The bug was discovered through manual review. The recommended mitigation steps are to disable NFT transfer and trade once the NFT is used to claim the reward.

### Original Finding Content


<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Quest.sol#L113>

Let us look closely into the `Quest.sol#claim` function

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
	_transferRewards(totalRedeemableRewards);
	redeemedTokens += redeemableTokenCount;

	emit Claimed(msg.sender, totalRedeemableRewards);
}
```

After the NFT is used to claim, the \_setClaimed(token) is called to mark the NFT as used to prevent double claiming.

```solidity
/// @notice Marks token ids as claimed
/// @param tokenIds_ The token ids to mark as claimed
function _setClaimed(uint256[] memory tokenIds_) private {
	for (uint i = 0; i < tokenIds_.length; i++) {
		claimedList[tokenIds_[i]] = true;
	}
}
```

The NFT is also tradeable in the secondary marketplace. I would like to make a reasonable assumption that user wants to buy the NFT because they can use the NFT to claim the reward, which means after the reward is claimed, the NFT lose value.

Consider the case below:

1.  User A has 1 NFT, has he can use the NFT to claim 1 ETH reward.
2.  User A place a sell order in opensea and sell the NFT for 0.9 ETH.
3.  User B see the sell order and find it a good trae, he wants to buy the NFT.
4.  User B submit a buy order, User A at the same time submit the claimReward transaction.
5.  User A's transaction executed first, reward goes to User A, then User B transaction executed, NFT ownership goes to User B, but user B find out that the he cannot claim the reward becasue the reward is already claimed by User A.

User A can intentionally front-run User B's buy transaction by monitoring the mempool in polygon using the service

<https://www.blocknative.com/blog/polygon-mempool>

Or it could be just two users submit transactions at the same time and User A's claim transaction happens to execute first.

### Recommended Mitigation Steps

Disable NFT transfer and trade once the NFT is used to claim the reward.

**[waynehoover (RabbitHole) acknowledged](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/119)**



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
| Finders | StErMi, rbserver, ElKu, ladboy233, CodingNameKiki, Tricko, 0xmrhoodie, adriro, 0x4non |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/119
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`vulnerability`

