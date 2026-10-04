---
# Core Classification
protocol: Mintbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48219
audit_firm: OtterSec
contest_link: https://www.mintbase.xyz/
source_link: https://www.mintbase.xyz/
github_link: https://github.com/Mintbase/mb-contracts

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
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Updating Token Owner Does Not Charge Caller

### Overview


This bug report discusses an issue where a token can be transferred to an account without any NFTs, resulting in the receiving account being added to tokens_per_owner. However, the storage cost for this is not accounted for, allowing attackers to lock up funds by repeatedly transferring NFTs to new accounts. The suggested solution is to require NFT minters to fully sponsor storage fees for potential listings. The bug has been resolved in the latest patch.

### Original Finding Content

## Token Transfer and Storage Costs

When a token is transferred to an account without any NFTs, the receiving account will be added to `tokens_per_owner`.

```rust
// mb-store/src/lib.rs
fn update_tokens_per_owner(
    ...
) {
    ...
    if let Some(to) = to {
        let mut new_owner_owned_set = self.get_or_make_new_owner_set(&to);
        new_owner_owned_set.insert(&token_id);
        self.tokens_per_owner.insert(&to, &new_owner_owned_set);
    }
}
```

The storage cost for this is not accounted for in `update_tokens_per_owner` and its callers, thus allowing attackers to lock up funds by repeatedly transferring NFTs to new accounts.

## Remediation

Require NFT minters to fully sponsor storage fees for potential listings.

```diff
// mb-store/src/minting.rs
fn storage_cost_to_mint(
    ...
) -> near_sdk::Balance {
    - // create an entry in tokens_per_owner
    - self.storage_costs.common
    - // create a metadata record
    - + metadata_storage as u128 * self.storage_costs.storage_price_per_byte
    + // create a metadata record
    + metadata_storage as u128 * self.storage_costs.storage_price_per_byte
    // create a royalty record
    + num_royalties as u128 * self.storage_costs.common
    // create n tokens each with splits stored on-token
    - + num_tokens as u128 * (self.storage_costs.token + num_splits as u128 * self.storage_costs.common)
    + + num_tokens as u128 * (
    + // token base storage
    + self.storage_costs.token
    + // dynamic split storage
    + + num_splits as u128 * self.storage_costs.common
    + // create an entry in tokens_per_owner
    + + self.storage_costs.common
    + )
}
```

## Patch

Resolved in a434371.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mintbase |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.mintbase.xyz/
- **GitHub**: https://github.com/Mintbase/mb-contracts
- **Contest**: https://www.mintbase.xyz/

### Keywords for Search

`vulnerability`

