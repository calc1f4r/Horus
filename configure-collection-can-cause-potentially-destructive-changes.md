---
# Core Classification
protocol: SPL Governance Civic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48760
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

Configure collection can cause potentially destructive changes

### Overview


The bug report describes a potential issue with the configure_collection function in a program called SPL Governance Plugins Audit 04. This function can cause changes to the max_voter_weight, which is used to determine if a proposal can be tipped. The report includes a proof of concept and a code snippet showing how the function can lead to unintended tipping of proposals. The bug has been resolved in a recent update.

### Original Finding Content

## Potentially Destructive Changes with `configure_collection`

The `configure_collection` function can cause potentially destructive changes to `max_voter_weight`, tipping previously untipped proposals. As seen below, collection configuration updates the max voter weight which is used to determine if a proposal can be tipped.

## Proof of Concept

1. Call `configure_collection` with collection configurations that sum to a `MaxVoterWeight` of 100.
2. Create a proposal with a `VoterWeight` of 49.
3. Call `configure_collection` with collection configurations that sum to a `MaxVoterWeight` of 90.
4. Tip the proposal in `spl-governance`.

### Code Example

```rust
// Update MaxVoterWeightRecord based on max voting power of the collections
let max_voter_weight_record = &mut ctx.accounts.max_voter_weight_record;
max_voter_weight_record.max_voter_weight = registrar
    .collection_configs
    .iter()
    .try_fold(0u64, |sum, cc| sum.checked_add(cc.get_max_weight()))
    .unwrap();
```

## Remediation

Resolved in #56.

© 2022 OtterSec LLC. All Rights Reserved.

---

## SPL Governance Plugins Audit 04 | Vulnerabilities

### Code Example

```rust
// Changes to the collections config can accidentally tip the scales for outstanding proposals and hence we disallow it
if realm.voting_proposal_count > 0 {
    return err!(NftVoterError::CannotConfigureCollectionWithVotingProposals);
}
```

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | SPL Governance Civic |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://solana.com/
- **GitHub**: https://github.com/solana-labs/governance-program-library
- **Contest**: https://solana.com/

### Keywords for Search

`vulnerability`

