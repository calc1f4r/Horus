---
# Core Classification
protocol: RabbitHole
chain: everychain
category: dos
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8854
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/552

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
  - denial-of-service
  - dos

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 27
finders:
  - glcanvas
  - ladboy233
  - cryptojedi88
  - Tointer
  - mookimgo
---

## Vulnerability Title

[M-03] DOS risk if enough tokens are minted in Quest.claim can lead, at least, to transaction fee lost

### Overview


This bug report is about a potential Denial of Service (DOS) risk in the Quest.claim function of the RabbitHole Protocol. The function is dependent on the RabbitHoleReceipt.getOwnedTokenIdsOfQuest, which can be summarized in four steps: getting the queried balance, getting the claiming address' owned tokens, filtering tokens corresponding to the questId, and returning the token of the claiming address corresponding to the questId.

If a user participates in multiple quests and accumulates a large number of tokens, the claim function may eventually reach the block gas limit. As a result, the user may be unable to successfully claim their earned tokens, incurring network fees if a griefer, who has already claimed their rewards, sends their tokens to the user with the intent of causing a DOS and inducing loss of gas. Even if the user has not claimed any rewards from their accumulated tokens, they will still be forced to burn at least some of their tokens, resulting in a loss of these assets.

The bug can be mitigated by allowing the user to send a token list as a parameter to the claim function. This can be done by adding a checkTokenCorrespondToQuest function to the RabbitHoleReceipt.sol, and modifying the Quest.claim function to check if the token corresponds to the questId.

### Original Finding Content


<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Quest.sol#L99><br>
<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/RabbitHoleReceipt.sol#L117-L133>

`claim` function can be summaraized in next steps:

1.  Check that the quest is active
2.  Check the contract is not paused
3.  Get tokens corresponding to msg.sender for `questId` using `rabbitHoleReceiptContract.getOwnedTokenIdsOfQuest`: **DOS**
4.  Check that msg.sender owns at least one token
5.  Count non claimed tokens
6.  Check there is at least 1 unclaimed token
7.  Calculate redeemable rewards: `_calculateRewards(redeemableTokenCount);`
8.  Set all token to claimed state
9.  Update `redeemedTokens`
10. Emit claim event

The problem with this functions relays in its dependency on `RabbitHoleReceipt.getOwnedTokenIdsOfQuest`. It's behaviour can be summarized in next steps:

1.  Get queried balance (claimingAddress\_)
2.  Get claimingAddress\_ owned tokens
3.  Filter tokens corresponding to questId\_
4.  Return token of claimingAddress\_ corresponding to questId\_

If a user actively participates in multiple quests and accumulates a large number of tokens, the claim function may eventually reach the block gas limit. As a result, the user may be unable to successfully claim their earned tokens.

### Impact

It can be argued that function `ERC721.burn` can address the potential DOS risk in the claim process. However, it is important to note the following limitations and drawbacks associated with this approach:

1.  Utilizing `ERC721.burn` does not prevent the user from incurring network fees if a griefer, who has already claimed their rewards, sends their tokens to the user with the intent of causing a DOS and inducing loss of gas.
2.  If the user has not claimed any rewards from their accumulated tokens, they will still be forced to burn at least some of their tokens, resulting in a loss of these assets.

### Proof of Concept

**Griefing**

1.  Alice has took part in many quests, and want to recieve her rewards, so she call Quest.claim() function
2.  Bob also has already claimed many rewards from many quest, and decide to frontrun alice an send her all his tokens to DOS her
3.  Alice run out of gas, she lose transaction fees.

**Lose of unclaimed rewards**

1.  Alice always takes part in many quests, but never claims her rewards. She trusts RabbitHole protocol and is waiting to have much more rewards to claim in order to save some transaction fees.
2.  When Alice decide to call claim function she realizes that she has run out of gas.

Then, Alice can only burn some of her tokens to claim at least some rewards.

**Code**

[Code sample](https://gist.github.com/carlitox477/85e37d26c6f810304c849c93235ee99e)

### Recommended Mitigation steps

If a user can send a token list by parameter to claim function, then this vector attack can be mitigated.

To do this add next function to `RabbitHoleReceipt.sol`:

```solidity
function checkTokenCorrespondToQuest(uint tokenId, string memory questId_) external view returns(bool){
    return keccak256(bytes(questIdForTokenId[tokenId])) == keccak256(bytes(questId_));
}
```

Then modify `Quest.claim`:

```diff
// Quest.sol
-   function claim() public virtual onlyQuestActive {
+   function claim(uint[] memory tokens) public virtual onlyQuestActive {
        if (isPaused) revert QuestPaused();

-       uint[] memory tokens = rabbitHoleReceiptContract.getOwnedTokenIdsOfQuest(questId, msg.sender);

        // require(tokens.length > 0)
        if (tokens.length == 0) revert NoTokensToClaim();

        uint256 redeemableTokenCount = 0;
        for (uint i = 0; i < tokens.length; i++) {
            // Check that the token correspond to this quest
            require(rabbitHoleReceiptContract.checkTokenCorrespondToQuest(tokens[i],questId))

-           if (!isClaimed(tokens[i])) {
+           if (!isClaimed(tokens[i]) && rabbitHoleReceiptContract.checkTokenCorrespondToQuest(tokens[i],questId)) {
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

**[kirk-baird (judge) decreased severity to Medium](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/552#issuecomment-1429385027)**

**[waynehoover (RabbitHole) acknowledged](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/552#issuecomment-1504020208)**



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
| Finders | glcanvas, ladboy233, cryptojedi88, Tointer, mookimgo, lukris02, minhquanym, adriro, p4st13r4, IllIllI, simon135, 0xbepresent, betweenETHlines, UdarTeam, 0xRobocop, Atarpara, trustindistrust, horsefacts, ArmedGoose, luxartvinsec, manikantanynala97, gzeon, evan, thekmj, carlitox477, libratus |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/552
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`Denial-Of-Service, DOS`

