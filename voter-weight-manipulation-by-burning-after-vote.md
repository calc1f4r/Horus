---
# Core Classification
protocol: SPL Governance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48616
audit_firm: OtterSec
contest_link: https://solana.com/
source_link: https://solana.com/
github_link: https://github.com/solana-labs/governance-program-library

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
finders_count: 3
finders:
  - Kevin Chow
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Voter weight manipulation by burning after vote

### Overview


The bug report describes a problem where a voter can manipulate their voting weight after the voting period ends and before the proposal is finalized. This can be done by relinquishing their vote, withdrawing their governing tokens, and burning them, which reduces the maximum voting weight. This allows the voter to have a greater influence on the final outcome of the proposal. The report provides a proof of concept and a suggested solution to prevent this manipulation in the future. 

### Original Finding Content

## Vote Relinquishment Process

A voter can influence their vote weight after voting ends and before proposal finalization. The voter relinquishes his/her vote, withdraws their governing tokens, burns to lower the mint supply (and therefore max_voter_weight) and finalizes.

## Proof of Concept

1. Deposit 33% of mint supply.
2. Create a proposal and vote on it.
3. Between voting time ending and proposal finalization, relinquish vote and withdraw tokens. The vote persists.
4. Burn withdrawn tokens (33%) and finalize. 
   - 33/66 = 50%

### Code Snippet

```rust
governance/program/src/processor/process_relinquish_vote.rs
```

```rust
} else {
    vote_record_data.is_relinquished = true;
    vote_record_data.serialize(&mut *vote_record_info.data.borrow_mut())?;
}
// If the Proposal has been already voted on then we only have to
// decrease unrelinquished_votes_count
token_owner_record_data.unrelinquished_votes_count =
    token_owner_record_data.unrelinquished_votes_count
        .checked_sub(1)
        .unwrap();
token_owner_record_data.serialize(&mut *token_owner_record_info.data.borrow_mut())?;
Ok(())
```

## Remediation

Prevent vote relinquishment before the vote is finalized. Resolved in #3210.

© 2022 OtterSec LLC. All Rights Reserved.

## Vulnerabilities

```rust
governance/program/src/processor/process_relinquish_vote.rs
```

```rust
} else {
// After Proposal voting time ends and it's not tipped then it
// enters implicit (time based) Finalizing state
// and releasing tokens in this state should be disallowed
// In other words releasing tokens is only possible once Proposal
// is manually finalized using FinalizeVote
if proposal_data.state == ProposalState::Voting {
    return Err(GovernanceError::CannotRelinquishInFinalizingState.into());
}
vote_record_data.is_relinquished = true;
vote_record_data.serialize(&mut *vote_record_info.data.borrow_mut())?;
// If the Proposal has been already voted on then we only have to
// decrease unrelinquished_votes_count
token_owner_record_data.unrelinquished_votes_count =
    token_owner_record_data.unrelinquished_votes_count
        .checked_sub(1)
        .unwrap();
token_owner_record_data.serialize(&mut *token_owner_record_info.data.borrow_mut())?;
Ok(())
```

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | SPL Governance V3 |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://solana.com/
- **GitHub**: https://github.com/solana-labs/governance-program-library
- **Contest**: https://solana.com/

### Keywords for Search

`vulnerability`

