---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: vote

# Attack Vector Details
attack_type: vote
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3597
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/25

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:
  - vote
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
  - Trumpero
  - 0x52
  - hansfriese
---

## Vulnerability Title

M-5: castVote can be called by anyone even those without votes

### Overview


This bug report concerns the Governance#castVote function of the FrankenDAO smart contract. The issue is that this function can be called by anyone, even users who do not have any votes, allowing them to maliciously burn vault funds by voting and claiming the vote refund. The code snippet provided in the report shows that the function only reverts if 1) the proposal isn't active 2) support > 2 or 3) if the user has already voted, meaning users can vote even if they don't have any votes. The impact of this vulnerability is that the vault can be drained maliciously by users with no votes. A recommendation is given to add a check to Governance#_castVote to revert if the user calling it doesn't actually have any votes. A discussion follows between two users, with the issue eventually being fixed in a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/25 

## Found by 
Trumpero, 0x52, hansfriese

## Summary

Governance#castVote can be called by anyone, even users that don't have any votes. Since the voting refund is per address, an adversary could use a large number of addresses to vote with zero votes to drain the vault.

## Vulnerability Detail

    function _castVote(address _voter, uint256 _proposalId, uint8 _support) internal returns (uint) {
        // Only Active proposals can be voted on
        if (state(_proposalId) != ProposalState.Active) revert InvalidStatus();
        
        // Only valid values for _support are 0 (against), 1 (for), and 2 (abstain)
        if (_support > 2) revert InvalidInput();

        Proposal storage proposal = proposals[_proposalId];

        // If the voter has already voted, revert        
        Receipt storage receipt = proposal.receipts[_voter];
        if (receipt.hasVoted) revert AlreadyVoted();

        // Calculate the number of votes a user is able to cast
        // This takes into account delegation and community voting power
        uint24 votes = (staking.getVotes(_voter)).toUint24();

        // Update the proposal's total voting records based on the votes
        if (_support == 0) {
            proposal.againstVotes = proposal.againstVotes + votes;
        } else if (_support == 1) {
            proposal.forVotes = proposal.forVotes + votes;
        } else if (_support == 2) {
            proposal.abstainVotes = proposal.abstainVotes + votes;
        }

        // Update the user's receipt for this proposal
        receipt.hasVoted = true;
        receipt.support = _support;
        receipt.votes = votes;

        // Make these updates after the vote so it doesn't impact voting power for this vote.
        ++totalCommunityScoreData.votes;

        // We can update the total community voting power with no check because if you can vote, 
        // it means you have votes so you haven't delegated.
        ++userCommunityScoreData[_voter].votes;

        return votes;
    }

Nowhere in the flow of voting does the function revert if the user calling it doesn't actually have any votes. staking#getVotes won't revert under any circumstances. Governance#_castVote only reverts if 1) the proposal isn't active 2) support > 2 or 3) if the user has already voted. The result is that any user can vote even if they don't have any votes, allowing users to maliciously burn vault funds by voting and claiming the vote refund. 

## Impact

Vault can be drained maliciously by users with no votes

## Code Snippet

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Governance.sol#L607-L646

## Tool used

Manual Review

## Recommendation

Governance#_castVote should revert if msg.sender doesn't have any votes:

        // Calculate the number of votes a user is able to cast
        // This takes into account delegation and community voting power
        uint24 votes = (staking.getVotes(_voter)).toUint24();

    +   if (votes == 0) revert NoVotes();

        // Update the proposal's total voting records based on the votes
        if (_support == 0) {
            proposal.againstVotes = proposal.againstVotes + votes;
        } else if (_support == 1) {
            proposal.forVotes = proposal.forVotes + votes;
        } else if (_support == 2) {
            proposal.abstainVotes = proposal.abstainVotes + votes;
        }

## Discussion

**zobront**

This is great and will fix, but an adversary being able to burn a small pool put aside for gas refunds for no personal benefit seems like a Medium, not a High.

**ZakkMan**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | Trumpero, 0x52, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/25
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`Vote, DAO`

