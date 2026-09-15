---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: uncategorized
vulnerability_type: vote

# Attack Vector Details
attack_type: vote
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7011
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
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
  - vote
  - don't_update_state

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

Oracle.removeMember could, in the same epoch, allow members to vote multiple times and other members to not vote at all

### Overview


This bug report is about an exploit found in the Oracle.1.sol code which allows an oracle member to vote multiple times in the same epoch. The exploit occurs when an oracle member is removed from the list of members and the information relating to the removed member is not removed from the ReportsPositions and ReportsVariants. This allows the same member that has already voted to vote again. A test case is provided in the Appendix to reproduce this issue. 

The recommendation is to remove the information relating to the removed member from both ReportsPositions and ReportsVariants. If this is not possible, then the entire state of both ReportsPositions and ReportsVariants should be cleared, which would require all active members to vote again for the same epoch. This recommendation has been implemented in SPEARBIT/2.

It is suggested to document this behaviour to clear any confusion for active oracle members.

### Original Finding Content

## Oracle Vulnerability Report

**Severity:** High Risk  
**Context:** Oracle.1.sol#L213-L222  

## Description

The current implementation of `removeMember` is introducing an exploit that allows an oracle member to vote multiple times in the same epoch, while preventing another oracle that has never voted from casting a vote during the same epoch.

Due to the implementation of `OracleMembers.deleteItem`, the last item of the array is swapped with the item that is being deleted, and then the last element is popped.

### Example Scenario

1. At T0, add member `m0` to the list of members: `members[0] = m0`.
2. At T1, add member `m1` to the list of members: `members[1] = m1`.
3. At T3, `m0` calls `reportBeacon(...)`. This action triggers a call to `ReportsPositions.register(uint256(0));` which registers that the member at index 0 has voted.
4. At T4, the oracle admin calls `removeMember(m0)`. This operation swaps `m0`’s address from the last position of the array with the position of the member being deleted. After this, it pops the last position of the array. The state changes from:
   - `members[0] = m0; members[1] = m1`
   - to `members[0] = m1;`.

At this point, the oracle member `m1` will not be able to vote during this epoch because when he/she calls `reportBeacon(...)`, the function will check:

```solidity
if (ReportsPositions.get(uint256(memberIndex))) {
    revert AlreadyReported(_epochId, msg.sender);
}
```

This is because `int256 memberIndex = OracleMembers.indexOf(msg.sender);` will return `0` (the position of the `m0` member who has already voted), and `ReportsPositions.get(uint256(0))` will return `true`.

If, for any reason, an admin of the contract re-adds the deleted oracle, it would be added to position `1` of the members array, allowing the same member who has already voted to vote again.

**Note:** While the scenario where a removed member can vote multiple times indicates a corrupted admin (who would re-add the same member), the situation preventing a user from voting would be more common.

Check the **Appendix** for a test case to reproduce this issue.

## Recommendation

After removing a member from `OracleMembers`, also remove the information related to the removed member from both `ReportsPositions` and `ReportsVariants`. If individual removal is not feasible, clear the entire state of both `ReportsPositions` and `ReportsVariants`. The consequence of this would be that all active members need to vote again for the same epoch.

- **Alluvial:** Recommendation implemented in SPEARBIT/2.
- **Spearbit:** Acknowledged.

**Note:** After removing an oracle member, all the "valid" members who have already voted for the epoch must vote again (everything is erased). We suggest documenting this behavior to clarify any confusion for active oracle members.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Vote, Don't update state`

