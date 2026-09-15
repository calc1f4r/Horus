---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3596
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/54

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 1

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - 0x52
  - cccz
  - neumo
  - WATCHPUG
  - Trumpero
---

## Vulnerability Title

M-4: `queue()` should increase `proposalsPassed` instead of `proposalsCreated`

### Overview


This bug report is about the `queue()` function in the code of a smart contract called FrankenDAO. The bug is that `proposalsCreated` is increased in `verifyProposal()`, but `queue()` should increase `proposalsPassed` instead. This issue was found by Trumpero, rvierdiiev, 0x52, WATCHPUG, neumo, cccz, John, and hansfriese.

The impact of this bug is that due to the presence of `setProposalsCreatedMultiplier()` and `setProposalsPassedMultiplier()`, the multiplier of both scores can be different, so the proposer's voting power bonuses will be wrongly calculated because `proposalsPassed` is not correctly increased in `queue()`.

The code snippet for this bug can be found in the following two files: 
- Governance.sol: Lines 467-495
- Staking.sol: Lines 592-601

The bug was fixed with a pull request on GitHub by ZakkMan. The recommendation was to change the code in the `queue()` function so that `proposalsPassed` is increased instead of `proposalsCreated`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/54 

## Found by 
Trumpero, rvierdiiev, 0x52, WATCHPUG, neumo, cccz, John, hansfriese

## Summary

`proposalsCreated` will be increased in `verifyProposal()`, `queue()` should increase `proposalsPassed`.

## Vulnerability Detail

Based on the context, `queue()` should increase `userCommunityScoreData[proposal.proposer].proposalsPassed` and `totalCommunityScoreData.proposalsPassed` instead.

## Impact

Due to the presence of `setProposalsCreatedMultiplier()` and `setProposalsPassedMultiplier()`, the multiplier of both scores can be different, when that's the case, the proposer's voting power bonuses will be wrongly calculated because `proposalsPassed` is not correctly increased in `queue()`.

## Code Snippet

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Governance.sol#L467-L495

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L592-L601

## Tool used

Manual Review

## Recommendation

Change to:

```diff
    function queue(uint256 _proposalId) external {
        // Succeeded means we're past the endTime, yes votes outweigh no votes, and quorum threshold is met
        if(state(_proposalId) != ProposalState.Succeeded) revert InvalidStatus();
        
        Proposal storage proposal = proposals[_proposalId];

        // Set the ETA (time for execution) to the soonest time based on the Executor's delay
        uint256 eta = block.timestamp + executor.DELAY();
        proposal.eta = eta.toUint32();

        // Queue separate transactions for each action in the proposal
        uint numTargets = proposal.targets.length;
        for (uint256 i = 0; i < numTargets; i++) {
            executor.queueTransaction(proposal.targets[i], proposal.values[i], proposal.signatures[i], proposal.calldatas[i], eta);
        }

        // If a proposal is queued, we are ready to award the community voting power bonuses to the proposer
-        ++userCommunityScoreData[proposal.proposer].proposalsCreated;
+        ++userCommunityScoreData[proposal.proposer].proposalsPassed;

        // We don't need to check whether the proposer is accruing community voting power because
        // they needed that voting power to propose, and once they have an Active Proposal, their
        // tokens are locked from delegating and unstaking.
-        ++totalCommunityScoreData.proposalsCreated;
+        ++totalCommunityScoreData.proposalsPassed;
        
        // Remove the proposal from the Active Proposals array
        _removeFromActiveProposals(_proposalId);

        emit ProposalQueued(_proposalId, eta);
    }
```

## Discussion

**ZakkMan**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/20

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | 0x52, cccz, neumo, WATCHPUG, Trumpero, hansfriese, John, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/54
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`vulnerability`

