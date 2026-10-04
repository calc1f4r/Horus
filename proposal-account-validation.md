---
# Core Classification
protocol: Pyth Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48828
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/governance.

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Proposal Account Validation

### Overview

See description below for full details.

### Original Finding Content

## Proposal Account Checks

When calling `update_voter_weight`, a proposal can be passed in as a remaining account, but the account owner is neither checked against the SPL governance program ID nor checked for type.

## Source Code Snippet

```rust
let proposal_account = &ctx.remaining_accounts[0];
let proposal_data: ProposalV2 = try_from_slice_unchecked(&proposal_account.data.borrow())?;
let proposal_start = proposal_data.voting_at.ok_or_else(|| error!(ErrorCode::ProposalNotActive))?;
```

## Remediation

Add a check that runs when `update_voter_weight` is called such that the owner is checked against the SPL governance program ID. We also recommend considering a PDA check against the proposal seeds.

## Source Code Snippet

```rust
let proposal_account = &ctx.remaining_accounts[0];
let governance_program = Pubkey::from_str("GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw").unwrap();
assert_eq!(proposal_account.owner, &governance_program);

let seed = &[
    PROGRAM_AUTHORITY_SEED,
    governance.as_ref(),
    governing_token_mint.as_ref(),
    proposal_index_le_bytes,
];

let (proposal_addr, _bump) = Pubkey::find_program_address(seed, &governance_program);
assert_eq!(proposal_addr, proposal_account.key());

let proposal_data: ProposalV2 = try_from_slice_unchecked(&proposal_account.data.borrow())?;
let proposal_start = proposal_data.voting_at.ok_or_else(|| error!(ErrorCode::ProposalNotActive))?;
```

## Proposal Address Seeds Function

```rust
pub fn get_proposal_address_seeds<'a>(
    governance: &'a Pubkey,
    governing_token_mint: &'a Pubkey,
    proposal_index_le_bytes: &'a [u8],
) -> [&'a [u8]; 4] {
    [
        PROGRAM_AUTHORITY_SEED,
        governance.as_ref(),
        governing_token_mint.as_ref(),
        proposal_index_le_bytes,
    ]
}
```

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: #181

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Governance |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/governance.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

