---
# Core Classification
protocol: MorphL2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41882
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/207
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/186

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
finders_count: 2
finders:
  - HaxSecurity
  - underdog
---

## Vulnerability Title

M-10: Malicious sequencer can DoS proposal execution by inflating the amount of proposals to be pruned

### Overview


The report describes a bug found in the `Gov.sol` contract, which is used for governance in the Morph network. A malicious actor can inflate the number of proposals in the contract, causing it to run out of gas and making it impossible to execute proposals. This is due to a lack of limits in proposal creation and a "pruning process" that iterates through all proposals, leading to an out-of-gas error. The bug can be exploited by becoming a sequencer in the network and creating multiple proposals with unreasonable values. This can lead to a denial of service (DoS) attack and prevent sequencers from executing proposals. To mitigate this issue, a cooldown period between proposal creations can be implemented to prevent a large number of proposals being created.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/186 

## Found by 
HaxSecurity, underdog
### Summary

A malicious sequencer can inflate the amount of proposals in `Gov.sol` in order to force the previous proposals invalidation process in `_executeProposal()` to run out of gas, making it impossible to execute proposals.

### Root Cause

Found in [Gov.sol#L257-L260](https://github.com/sherlock-audit/2024-08-morphl2/blob/main/morph/contracts/contracts/l2/staking/Gov.sol#L257-L260).

The `Gov.sol` contract incorporates a “proposal pruning process”. Every time a proposal is executed, all the previous proposals since `undeletedProposalStart` will be pruned (even if they are executed or not). This is done in order to avoid a situation where older proposals get executed, overriding the governance values of newly executed proposals.

As shown in the following code snippet, the “pruning process” works by iterating all proposals since the latest `undeletedProposalStart`, and until the current proposal ID. It is also worth noting that `undeletedProposalStart` is only updated **when executing a proposal,** and is set to the ID of the proposal being executed so that next proposal executions don’t need to prune from the first proposal ID:

```solidity
// Gov.sol

function _executeProposal(uint256 proposalID) internal {
        ...

        // when a proposal is passed, the previous proposals will be invalidated and deleted
        for (uint256 i = undeletedProposalStart; i < proposalID; i++) {
            delete proposalData[i];
            delete proposalInfos[i];
            delete votes[i];
        }
        
        undeletedProposalStart = proposalID;
        
        ...
}
```

However, this iteration can lead to an out-of-gas error, as a malicious sequencer can inflate the amount of proposal ID’s due to the lack of limits in proposal creations:

```solidity
// Gov.sol
function createProposal(ProposalData calldata proposal) external onlySequencer returns (uint256) {
        require(proposal.rollupEpoch != 0, "invalid rollup epoch");
        require(proposal.maxChunks > 0, "invalid max chunks");
        require(
            proposal.batchBlockInterval != 0 || proposal.batchMaxBytes != 0 || proposal.batchTimeout != 0,
            "invalid batch params"
        );

        currentProposalID++;
        proposalData[currentProposalID] = proposal;
        proposalInfos[currentProposalID] = ProposalInfo(block.timestamp + votingDuration, false);

        emit ProposalCreated(
            currentProposalID,
            _msgSender(),
            proposal.batchBlockInterval,
            proposal.batchMaxBytes,
            proposal.batchTimeout,
            proposal.maxChunks,
            proposal.rollupEpoch
        );

        return (currentProposalID);
    }
```

As shown in the snippet, any sequencer can create a proposal, and there’s no limit to proposal creation, allowing the proposal inflation scenario to occur.

### Internal pre-conditions

- A staker in Morph needs to be a sequencer in the sequencer set (achieved by obtaining delegations, or by simply being added as a staker in the `L2Staking` contract if rewards have not started)
- The sequencer needs to call `createProposal()` several times so the amount of proposals created is inflated, and the `currentProposalID` tracker becomes a number big enough to DoS proposal pruning

### External pre-conditions

None.

### Attack Path

1. A staker stakes in `L1Staking`. A cross-layer message is sent from L1 to L2, and the staker is registered to the `L2Staking` contract as a staker.
2. If rewards have not started and the sequencer set is not filled, the staker will be directly added to the sequencer set, becoming a sequencer. Otherwise, the staker needs to have some MORPH tokens delegated so that he can become a sequencer.
3. After becoming a sequencer, `createProposal()` is called several times to inflate the amount of proposal ID’s. The sequencer can set unreasonable values so that voting and executing any of the proposals leads the system to behave dangerously, making it disappealing for sequencers to vote for any of the proposals and avoid the OOG issue by executing certain proposals.
4. Because `currentProposalID` has been inflated, any proposal created after the inflation will try to prune all the previous fake proposals, leading to a DoS and runnning out of gas. This will effectively DoS proposal creation.

### Impact

Sequencers won’t be able to execute proposals in the governance contract, making it impossible to update global network parameters used by Morph.

### PoC

_No response_

### Mitigation

Implement a cooldown period between proposal creations. This will prevent creating a huge amount of proposals, as the attacker will need to wait for the cooldown period to finish in order to create another proposal. If the owner identifies suspicious behavior, he can then remove him in the L1 staking contract, and effectively removing the attacker as sequencer in the L2.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | MorphL2 |
| Report Date | N/A |
| Finders | HaxSecurity, underdog |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/186
- **Contest**: https://app.sherlock.xyz/audits/contests/207

### Keywords for Search

`vulnerability`

