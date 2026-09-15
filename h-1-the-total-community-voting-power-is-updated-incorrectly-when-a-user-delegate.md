---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: dao

# Attack Vector Details
attack_type: dao
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3589
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/91

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - dao

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - curiousapple
  - Trumpero
  - hansfriese
---

## Vulnerability Title

H-1: The total community voting power is updated incorrectly when a user delegates.

### Overview


This bug report is about an issue with the total community voting power being updated incorrectly when a user delegates. It was found by Trumpero, curiousapple, and hansfriese. The bug occurs when a user delegates their voting power from staked tokens, as the update logic is not correct, resulting in the wrong values for the total community voting power. The code snippet provided shows that when the total community voting power is increased in the first if statement, the msg.sender's token voting power might be positive already and community voting power might be added to total community voting power before. Additionally, the currentDelegate's token voting power might be still positive after delegation, so the community voting power should not be removed. This can lead to incorrect values for the total community voting power. The recommended solution is to add more conditions to check if the msg.sender delegated or not. The bug was fixed by zobront, who asked for a second set of eyes to double check the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/91 

## Found by 
Trumpero, curiousapple, hansfriese

## Summary
When a user delegates their voting power from staked tokens, the total community voting power should be updated. But the update logic is not correct, the the total community voting power could be wrong values.

## Vulnerability Detail

```solidity
    tokenVotingPower[currentDelegate] -= amount;
    tokenVotingPower[_delegatee] += amount; 

    // If a user is delegating back to themselves, they regain their community voting power, so adjust totals up
    if (_delegator == _delegatee) {
      _updateTotalCommunityVotingPower(_delegator, true);

    // If a user delegates away their votes, they forfeit their community voting power, so adjust totals down
    } else if (currentDelegate == _delegator) {
      _updateTotalCommunityVotingPower(_delegator, false);
    }
```
When the total community voting power is increased in the first if statement, `_delegator`'s token voting power might be positive already and community voting power might be added to total community voting power before.

Also, `currentDelegate`'s token voting power might be still positive after delegation so we shouldn't remove the communitiy voting power this time.

## Impact
The total community voting power can be incorrect.

## Code Snippet
https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L293-L313

## Tool used
Manual Review

## Recommendation
Add more conditions to check if the msg.sender delegated or not.

```solidity
    if (_delegator == _delegatee) {
        if(tokenVotingPower[_delegatee] == amount) {
            _updateTotalCommunityVotingPower(_delegator, true);
        }
        if(tokenVotingPower[currentDelegate] == 0) {
            _updateTotalCommunityVotingPower(currentDelegate, false);      
        }
    } else if (currentDelegate == _delegator) {
        if(tokenVotingPower[_delegatee] == amount) {
            _updateTotalCommunityVotingPower(_delegatee, true);
        }
        if(tokenVotingPower[_delegator] == 0) {
            _updateTotalCommunityVotingPower(_delegator, false);      
        }
    }
```

## Discussion

**zobront**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/15

Note for JTP: Please double check this one, as I'm 99% confident but would love a second set of eyes on it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | curiousapple, Trumpero, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/91
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`DAO`

