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
solodit_id: 6860
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

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

Tokens could be sent / withdrawn multiple times by accident

### Overview


This bug report is about the QuestBoard.sol code and its two functions, closeQuestPeriod() and closePartOfQuestPeriod() which have similar functionality but interfere with each other. 

The first problem is that if the first quest of a period is closed with closePartOfQuestPeriod(), closeQuestPeriod() won't be able to close the rest of the periods. The second problem is that if the second quest of a period is closed with closePartOfQuestPeriod(), closeQuestPeriod() will close it again and send the rewards of the second quest to the distributor again, as well as setting the withdrawableAmount value one more time, so the creator can do withdrawUnusedRewards() once more.

The report also notes that the two functions have a lot of code duplication, which increases the risk of issues with future code changes.

The severity of this bug is high risk because the likelihood of it happening is medium, but the impact is high. The recommendation is to let closeQuestPeriod() call closePartOfQuestPeriod(), and to make closePartOfQuestPeriod() more robust by checking the status of each period and skipping the already closed periods. The bug has been implemented in #9, and acknowledged by Spearbit.

### Original Finding Content

## Severity: High Risk

## Context
`QuestBoard.sol#L678-L815`

## Description
Functions `closeQuestPeriod()` and `closePartOfQuestPeriod()` have similar functionality but interfere with each other.

1. Suppose you have closed the first quest of a period via `closePartOfQuestPeriod()`. Now you cannot use `closeQuestPeriod()` to close the rest of the periods, as `closeQuestPeriod()` checks the state of the first quest.
2. Suppose you have closed the second quest of a period via `closePartOfQuestPeriod()`, but `closeQuestPeriod()` continues to work. It will close the second quest again and send the rewards of the second quest to the distributor again. Also, the function `closeQuestPeriod()` sets the `withdrawableAmount` value one more time, so the creator can do `withdrawUnusedRewards()` once more.

Although both `closeQuestPeriod()` and `closePartOfQuestPeriod()` are authorized, the problems above could occur by accident. Additionally, there is a lot of code duplication between `closeQuestPeriod()` and `closePartOfQuestPeriod()`, with a high risk of issues with future code changes.

```solidity
function closeQuestPeriod(uint256 period) external isAlive onlyAllowed nonReentrant {
    ...
    // We use the 1st QuestPeriod of this period to check it was not Closed
    uint256[] memory questsForPeriod = questsByPeriod[period];
    require(
        periodsByQuest[questsForPeriod[0]][period].currentState == PeriodState.ACTIVE, // only checks first
        "QuestBoard: Period already closed"
    );
    ... // no further checks on currentState
    _questPeriod.withdrawableAmount = .... // sets withdrawableAmount (again)
    IERC20(_quest.rewardToken).safeTransfer(distributor, toDistributeAmount); // sends tokens (again)
    ...
}

function closePartOfQuestPeriod(uint256 period, uint256[] calldata questIDs) external isAlive onlyAllowed nonReentrant {
    ...
    _questPeriod.currentState = PeriodState.CLOSED;
    ...
    _questPeriod.withdrawableAmount = _questPeriod.rewardAmountPerPeriod - toDistributeAmount;
    IERC20(_quest.rewardToken).safeTransfer(distributor, toDistributeAmount);
    ...
}
```

**Note:** Set to high risk because the likelihood of this happening is medium, but the impact is high.

## Recommendation
Let the function `closeQuestPeriod()` call `closePartOfQuestPeriod()`. Make `closePartOfQuestPeriod()` more robust by:
- Checking the status of each period.
- Skipping the already closed periods.

**Paladin:** Implemented in #9.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

