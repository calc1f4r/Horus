---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57204
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 13
finders:
  - pyro
  - joicygiore
  - sovaslava
  - oxanmol
  - 0xbz
---

## Vulnerability Title

Owner Can Change Vote Results After Voting Ends by Updating Quorum Numbers for New proposals

### Overview


The `Governance.sol` contract allows the owner to change the voting requirements for proposals even after voting has ended. This can cause a previously successful proposal to fail. This is because the contract uses the current voting requirements to evaluate a proposal's success, instead of the requirements in place when the proposal was voted on. This can lead to unexpected and unfair outcomes for voters. To fix this, the contract should be modified to store the voting requirements for each proposal at the time of creation and use those values when evaluating the proposal's success. Alternatively, the contract could be changed to only allow the owner to update the requirements for future proposals. 

### Original Finding Content

## Summary

The `Governance.sol` contract allows the owner to update the `quorumNumerator`, which retroactively alters the quorum requirements for all proposals, even after voting ends. This can cause a previously successful proposal to fail.

## Vulnerability Details

This issue is because the `quorumNumerator`, which determines the percentage of total voting power needed for a proposal to reach quorum, is dynamically applied to all proposals whenever their state is checked. This parameter is initially set to 4 (representing a 4% quorum) but can be modified by the owner through the `setParameter function`. The issue is that the state function uses the current `quorumNumerator` value to evaluate a proposal’s success, not the value in place when the proposal was created or voted on.

Below is the `state` function, which determines a proposal’s status after voting

```solidity
function state(uint256 proposalId) public view override returns (ProposalState) {
    ProposalCore storage proposal = _proposals[proposalId];
    if (proposal.canceled) return ProposalState.Canceled;
    if (proposal.executed) return ProposalState.Executed;
    if (block.timestamp < proposal.startTime) return ProposalState.Pending;
    if (block.timestamp < proposal.endTime) return ProposalState.Active;

    ProposalVote storage proposalVote = _proposalVotes[proposalId];
    uint256 currentQuorum = proposalVote.forVotes + proposalVote.againstVotes;
    uint256 requiredQuorum = quorum();
    if (currentQuorum < requiredQuorum || proposalVote.forVotes <= proposalVote.againstVotes) {
        return ProposalState.Defeated;
    }
}
```

`state` doesn’t lock in the quorumNumerator from the proposal’s voting period. Instead, it fetches the current value, allowing updates to retroactively rewrite outcomes.

Imagine a proposal with a total voting power of 100M `veRAAC` tokens. During voting, `quorumNumerator` is 4, so the quorum is 4M (4% of 100M). The proposal receives 5M votes (3M “for,” 2M “against”), exceeding the 4M quorum and passing with more “for” votes. Voting ends, and the proposal enters the Succeeded state, awaiting queuing in the timelock. Later, the owner updates `quorumNumerator` to 5, making the quorum 5M (5% of 100M). When someone calls state to queue or execute it, `currentQuorum` (5M) is now exactly equal to `requiredQuorum` (5M), but if total voting power shifts slightly (e.g., to 110M due to new locks), the quorum becomes 5.5M, and the proposal fails (5M < 5.5M) despite passing earlier.

## Impact

This isn't about trust, it's about maintaining consistent, predictable governance mechanics. The owner's ability to change future quorum requirements is fine, but those changes shouldn't affect proposals that already completed voting.

1. A trusted owner might update `quorumNumerator` for a legitimate reason (e.g., adapting to a 5% increase in voting power) without realizing it affects queued proposals.
2. Proposals that were initially successful may fail later due to external changes in voting power.
3. Voters cannot rely on the fairness of the governance system since rules can be altered retroactively.

## Tools Used

Manual Review

## Recommendations

To fix this, the Governance.sol should be modified to snapshot the `quorumNumerator` for each proposal at creation. Add a `quorumNumerator` field to the `ProposalCore` struct.
Update the propose function to store it
Adjust state to use the stored value

Alternatively, restrict `setParameter` to only affect future proposals by checking active proposal states, though the snapshot approach is simpler and more robust.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | pyro, joicygiore, sovaslava, oxanmol, 0xbz, vladislavvankov0, 0xgremlincat, x1485967, udogodwin2k22, 3n0ch, adeolasola01, 1337web3 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

