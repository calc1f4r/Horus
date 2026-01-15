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
solodit_id: 48210
audit_firm: OtterSec
contest_link: https://www.mintbase.xyz/
source_link: https://www.mintbase.xyz/
github_link: https://github.com/Mintbase/mb-contracts

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

NFT Not Returned On Transfer Failure

### Overview


The function nft_resolve_transfer is responsible for handling state rollback in case of a failure in nft_on_transfer or nft_transfer_call. However, there is a bug where the function does not properly return the NFT back to its original owner. This is because the function calls transfer_internal with the wrong recipient. The solution to this bug is to transfer the NFT to the original owner instead of the current recipient. This bug has been fixed in the latest patches 6a69314 and 23ecd80.

### Original Finding Content

## nft_resolve_transfer Callback Function

The `nft_resolve_transfer` is a callback function responsible for handling state rollback upon failure in `nft_on_transfer` or `nft_transfer_call`. A crucial aspect of rolling back states is to return NFTs to their `original_owner`. 

However, `nft_resolve_transfer` calls `transfer_internal` with an incorrect recipient and fails to return the NFT back to the original owner properly.

## Code Example

### Original Code (mb-store/src/core.rs)
```rust
#[private]
pub fn nft_resolve_transfer(
    ...
) -> bool {
    ...
    if !must_revert {
        true
    } else {
        self.transfer_internal(&mut token, receiver_id.clone(), true);
        log_nft_transfer(
            &receiver_id,
            token_id_u64,
            &None,
            owner_id.to_string(),
        );
        false
    }
}
```

## Remediation

Transfer NFTs to `owner_id` instead of `receiver_id`.

### Updated Code (mb-store/src/core.rs)
```diff
if !must_revert {
    true
} else {
-   self.transfer_internal(&mut token, receiver_id.clone(), true);
+   self.transfer_internal(&mut token, owner_id.clone(), true);
    log_nft_transfer(
-       &receiver_id,
+       &owner_id,
        token_id_u64,
        &None,
-       owner_id.to_string(),
+       receiver_id.to_string(),
    );
    false
}
```

## Patch

Resolved in commits `6a69314` and `23ecd80`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

