---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54307
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
github_link: none

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
finders_count: 1
finders:
  - J4X98
---

## Vulnerability Title

Locks unlocking at the nexttimestamp will not trigger noactivelocks 

### Overview


The report discusses a bug in the Opal protocol's governance mechanism, specifically in the `_voteForGaugeweight()` function. This bug causes the voting system to not work properly due to three conflicting conditions that are supposed to check the `unlockTime` of locks. The recommendation is to change all three conditions to follow the same rule of `unlockTime > vars.nextTimestamp` to fix the bug.

### Original Finding Content

## GaugeController.sol#L494

## Description

The Opal protocol implements a governance mechanism that allows the users to vote on the weight of gauges. This is facilitated in the `_voteForGaugeweight()` function. This function imposes three checks on the `unlockTime` of locks:

```solidity
if (locks[vars.len - 1].unlockTime < vars.nextTimestamp) revert NoActiveLocks();
```

This check enforces that the last lock (the one that will be locked for the longest) needs to unlock at `unlockTime >= vars.nextTimestamp`, otherwise all the locks are invalid for this voting period.

The second check is enforced later when the voting power from all locks is summed:

```solidity
Unlocks[] memory unlocks = new Unlocks[](vars.len);
uint256 i = vars.len - 1;
IVoteLocker.LockedBalance memory currentLock = locks[i];
while (currentLock.unlockTime > vars.nextTimestamp) {
    uint256 weightedAmount = currentLock.amount * voteWeight / 10_000;
    newUserVote.amount += weightedAmount;
    unlocks[i] = Unlocks({
        amount: uint208(weightedAmount),
        unlockTime: currentLock.unlockTime
    });
    if (i > 0) {
        i--;
        currentLock = locks[i];
    } else {
        break;
    }
}
```

Now all locks where `unlockTime > vars.nextTimestamp` get summed up (are eligible to vote). The third check implements another invariant:

```solidity
for (uint256 l; l < vars.len; l++) {
    // Also covers case where unlockTime is 0 (empty array item)
    if (unlocks[l].unlockTime <= block.timestamp) continue;
    userVoteUnlocks[user][gauge].push(unlocks[l]);
}
```

This time the invariant of who is allowed to vote is `unlocks[l].unlockTime > block.timestamp`. Here, the cut-off date is the `block.timestamp` instead of the `vars.nextTimestamp`.

Unfortunately, these 3 invariants contradict each other, resulting in a broken voting system.

## Recommendation

The issue can be mitigated by changing the three conditionals to follow the same invariant. This recommended invariant would be `unlockTime > vars.nextTimestamp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | J4X98 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

