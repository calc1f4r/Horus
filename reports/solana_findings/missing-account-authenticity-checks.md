---
# Core Classification
protocol: Tensor Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46757
audit_firm: OtterSec
contest_link: https://tensor.foundation/
source_link: https://tensor.foundation/
github_link: https://github.com/tensor-foundation

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Missing Account Authenticity Checks

### Overview


The bug report discusses a vulnerability in the MplxShared structure related to NFTs (non-fungible tokens). The issue is that there are no checks in place to verify the existence of the metadata and edition accounts for a specific NFT. This means that the uniqueness and associated data of the NFT cannot be properly validated. 
Additionally, in the transfer functionality, only the metadata is verified and the master_edition is not utilized. This means that for non-pNFTs (non-permanent NFTs), there is no confirmation that the mint is truly non-fungible. 
To fix this issue, the report suggests implementing PDA (Program Derived Address) and initialization checks to ensure that the metadata, edition, and master_edition accounts are properly validated. This issue has been resolved in #94.

### Original Finding Content

## Summary

In `shared_accounts` within the `MplxShared` structure, the metadata and edition accounts are essential to validate an NFT’s properties, such as its uniqueness and associated data. The vulnerability concerns the lack of seed checks to verify the existence of the metadata and edition for the provided mint.

## Code Snippet

```rust
pub struct MplxShared<'info> {
    // [...]
    
    /// The Token Metadata metadata account of the NFT.
    /// CHECK: ownership, structure and mint are checked in assert_decode_metadata.
    #[account(mut)]
    pub metadata: UncheckedAccount<'info>,
    // --------------------------------------- pNft
    
    /// The Token Metadata edition account of the NFT.
    /// CHECK: seeds checked on Token Metadata CPI
    // note that MASTER EDITION and EDITION share the same seeds, and so it's valid to check them
    // → here
    pub edition: UncheckedAccount<'info>,
    // [...]
}
```

Additionally, in the transfer functionality, only the metadata is verified, and the `master_edition` is not utilized for the non-pNFT case. Thus, the `master_edition` account is not utilized or checked in the non-pNFT case. This is crucial because without verifying the existence of the `master edition`, there is no confirmation that the mint is truly non-fungible.

## Remediation

Implement PDA (Program Derived Address) and initialization checks to ensure that the `metadata`, `edition`, and `master_edition` accounts are properly validated.

## Patch

Resolved in #94.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Foundation |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://tensor.foundation/
- **GitHub**: https://github.com/tensor-foundation
- **Contest**: https://tensor.foundation/

### Keywords for Search

`vulnerability`

