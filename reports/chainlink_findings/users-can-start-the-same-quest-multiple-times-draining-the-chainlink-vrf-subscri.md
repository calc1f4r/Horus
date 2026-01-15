---
# Core Classification
protocol: Proof of Play / Pirate Nation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50503
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

USERS CAN START THE SAME QUEST MULTIPLE TIMES DRAINING THE CHAINLINK VRF SUBSCRIPTION

### Overview


The bug report is about a vulnerability in the `QuestSystem` contract where a user can start a quest multiple times and complete it, draining all the LINK balance of the subscription. This is because the `MaxCompletions` value can be easily bypassed and there is no limit on how many times a user can start the same quest. This can be a serious issue as it can lead to a loss of funds. The report recommends accepting the risk as no mitigation has been added to prevent this issue. 

### Original Finding Content

##### Description

In the `QuestSystem` contract every time a quest is completed Chainlink VRF is used:

#### QuestSystem.sol

```
function completeQuest(uint64 activeQuestId)
    external
    nonReentrant
    whenNotPaused
{
    address account = _msgSender();
    ActiveQuest storage activeQuest = _activeQuests[activeQuestId];

    // Make sure active quest exists
    require(
        activeQuest.status == ActiveQuestStatus.IN_PROGRESS,
        "INVALID_ACTIVE_QUEST_ID: ActiveQuest is not IN_PROGRESS"
    );

    // Check to make sure sender is the quest owner
    require(
        activeQuest.account == account,
        "INVALID_ACCOUNT: Sender did not undertake this quest"
    );

    // Make sure quest is still active
    QuestDefinition storage questDef = _questDefinitions[
        activeQuest.questId
    ];
    require(
        questDef.active == true,
        "QUEST_NOT_ACTIVE: Cannot complete inactive quest"
    );

    uint256 endTime = activeQuest.startTime + questDef.completionSeconds;
    require(
        endTime <= block.timestamp,
        "NOT_READY_TO_COMPLETE: Quest is not ready to be completed"
    );

    // TODO: Maybe we fail here automatically if expire time has passed instead of error?
    require(
        questDef.expireSeconds == 0 ||
            (endTime + questDef.expireSeconds > block.timestamp),
        "QUEST_HAS_EXPIRED: Quest has expired and is no longer completeable"
    );

    // Figure out final amount of gold the player earns with some randomness
    uint256 requestId = _requestRandomWords(1);
    _vrfRequests[requestId] = VRFRequest({
        account: account,
        activeQuestId: activeQuestId
    });

    // Change status
    activeQuest.status = ActiveQuestStatus.GENERATING_RESULTS;
}

```

\color{black}
\color{white}

Considering that the `accountData.completions[questId]` mapping is only updated after a quest is completed successfully, the `QuestDefinition.MaxCompletions` value can be easily bypassed.

As explained in the `QUESTDEFINITION.MAXCOMPLETIONS CAN BE BYPASSED BY STARTING THE SAME QUEST MULTIPLE TIMES BEFORE COMPLETING THEM` issue, a user can start a quest as many times as he wants as long as he has enough inputs.

For ERC721 and ERC1155 inputs, as these assets are locked once a quest is started, it is not possible to perform the same quest twice. But for ERC20 inputs as there is an open TODO and this is not implemented yet, the ERC20 tokens are not locked when the quest is started, any user can start the same quest as many times as he wants.

Then, after waiting a certain period of time, the same user could complete all the quests that he started. Each completion would make use of Chainlink VRF subscription. It would be possible to totally drain all the LINK balance of the subscription, as there is no limit on how many times the user could start the same quest.

##### Score

Impact: 5  
Likelihood: 3

##### Recommendation

**RISK ACCEPTED**: No mitigation was added to prevent this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Proof of Play / Pirate Nation |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/proof-of-play/proof-of-play-pirate-nation-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

