---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6864
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
github_link: none

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - DefSec
  - Jay Jonah8
  - Gerard Persoon
---

## Vulnerability Title

Accidental call of addQuest could block contracts

### Overview


This bug report is about the MultiMerkleDistributor.sol and QuestBoard.sol contracts. The addQuest() function in the QuestBoard.sol contract uses an onlyAllowed access control modifier, which checks if the msg.sender is questBoard or owner. However, the QuestBoard.sol contract has a QuestID registration and a token whitelisting mechanism which should be used in combination with the addQuest() function. If the owner accidentally calls the addQuest() function, the QuestBoard.sol contract will not be able to call addQuest() for that questID. As soon as createQuest() tries to add that same questID, the function will revert and become uncallable because nextID still maintains that same value.

To fix this issue, the modifier on the addQuest() function should be replaced with a modifier like onlyQuestBoard(), which requires that the msg.sender is equal to the questBoard. This implementation was implemented in #5.

### Original Finding Content

## Severity: Medium Risk

## Context
- MultiMerkleDistributor.sol#L240
- QuestBoard.sol#L276-L369

## Description
The `addQuest()` function uses an `onlyAllowed` access control modifier. This modifier checks if `msg.sender` is `questBoard` or `owner`. However, the `QuestBoard.sol` contract has a QuestID registration and a token whitelisting mechanism which should be used in combination with the `addQuest()` function. If `owner` accidentally calls `addQuest()`, the `QuestBoard.sol` contract will not be able to call `addQuest()` for that `questID`. As soon as `createQuest()` tries to add that same `questID`, the function will revert, becoming uncallable because `nextID` still maintains that same value.

```solidity
function createQuest(...) {
    uint256 newQuestID = nextID;
    nextID += 1;
    require(MultiMerkleDistributor(distributor).addQuest(newQuestID, rewardToken), "QuestBoard: Fail add to Distributor");
}
```

```solidity
function addQuest(uint256 questID, address token) external onlyAllowed returns(bool) {
    require(questRewardToken[questID] == address(0), "MultiMerkle: Quest already listed");
    require(token != address(0), "MultiMerkle: Incorrect reward token");
    // Add a new Quest using the QuestID, and list the reward token for that Quest
    questRewardToken[questID] = token;
    emit NewQuest(questID, token);
    return true;
}
```

**Note:** Set to medium risk because the likelihood of this happening is low, but the impact is high.

## Recommendation
Replace the modifier on `addQuest()` with a modifier like `onlyQuestBoard()`:

```solidity
modifier onlyQuestBoard() {
    require(msg.sender == questBoard, "MultiMerkle: Not allowed");
    _;
}
```

**Paladin:** Choice to put only a require instead of a one-time use modifier. Implemented in #5.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | DefSec, Jay Jonah8, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

