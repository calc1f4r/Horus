---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27547
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/329

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cergyk
---

## Vulnerability Title

[H-57] twAML::participate - reentrancy via _safeMint can be used to brick reward distribution

### Overview


This bug report is about a malicious user exploiting a vulnerability in twAML's `participate` function. The vulnerability lies in the fact that the `_safeMint` function executes a callback on the destination contract, `onERC721Received`, which can be used to reenter and release the position. This can be done since the `position.expiry` is not set yet. This can have a direct impact on reward distribution since the malicious user can use reentrancy to increase `weekTotals[w0 + 1].netActiveVotes` by large amounts without locking their tokens. As a result, when the operator wants to distribute rewards, `totals.totalDistPerVote[_rewardTokenId]` becomes zero.

To mitigate this vulnerability, two recommended steps are suggested. The first is to move the effects before `_safeMint` and the second is to use the nonReentrant modifier. Both of these steps can help prevent malicious users from exploiting the vulnerability.

### Original Finding Content


A malicious user can use reentrancy in twAML to brick reward distribution

### Proof of Concept

As we can see in `participate` in twAML, the function `_safeMint` is used to mint the voting position to the user;

However this function executes a callback on the destination contract: `onERC721Received`, which can then be used to reenter:

```solidity
// Mint twTAP position
tokenId = ++mintedTWTap;
_safeMint(_participant, tokenId);
```

The `_participant` contract can reenter in `exitPosition`, and release the position since,

```solidity
require(position.expiry <= block.timestamp, "twTAP: Lock not expired");
```

`position.expiry` is not set yet.

However we see that the following effects are executed after `_safeMint`:

    weekTotals[w0 + 1].netActiveVotes += int256(votes);
    weekTotals[w1 + 1].netActiveVotes -= int256(votes);

And these have a direct impact on reward distribution;
The malicious user can use reentrancy to increase `weekTotals[w0 + 1].netActiveVotes` by big amounts without even locking her tokens;

Later when the operator wants to distribute the rewards:

```solidity
function distributeReward(
    uint256 _rewardTokenId,
    uint256 _amount
) external {
    require(
        lastProcessedWeek == currentWeek(),
        "twTAP: Advance week first"
    );
    WeekTotals storage totals = weekTotals[lastProcessedWeek];
    IERC20 rewardToken = rewardTokens[_rewardTokenId];
    // If this is a DBZ then there are no positions to give the reward to.
    // Since reward eligibility starts in the week after locking, there is
    // no way to give out rewards THIS week.
    // Cast is safe: `netActiveVotes` is at most zero by construction of
    // weekly totals and the requirement that they are up to date.
    // TODO: Word this better
    totals.totalDistPerVote[_rewardTokenId] +=
        (_amount * DIST_PRECISION) /
        uint256(totals.netActiveVotes);
    rewardToken.safeTransferFrom(msg.sender, address(this), _amount);
}
```

totals.totalDistPerVote\[\_rewardTokenId] becomes zero

### Recommended Mitigation Steps

Use any of these:

*   Move effects before \_safeMint
*   Use nonReentrant modifier

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/329#issuecomment-1680836999)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/329
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

