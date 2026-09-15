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
solodit_id: 48217
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

NFT State Not Restored On Transfer Failure

### Overview


The bug report states that there is an issue with the function nft_resolve_transfer, which is supposed to rollback the state of a non-fungible token (NFT) if a transfer call fails or returns true. However, the current implementation does not properly restore the fields split_owners and approvals to their original state. This means that even if the transfer fails, these fields are still cleared.

To fix this issue, the report suggests restoring the split_owners and approvals fields if the transfer fails. The proposed solution involves cloning the current values of these fields and using them to restore the original values if needed.

The report also includes code snippets showing the current implementation and the proposed solution. It also mentions that the issue has been resolved in a specific code commit.

In summary, the bug report highlights a problem with the nft_resolve_transfer function and suggests a solution to fix it. It also provides relevant code snippets and mentions that the issue has been resolved in a recent code commit.

### Original Finding Content

## NFT Transfer Resolution

## Summary

The `nft_resolve_transfer` function should fully rollback the NFT state if the `nft_on_transfer` call fails or returns true. The current implementation does not properly restore `split_owners` and `approvals` to their original state, as both fields are cleared regardless of the transfer result.

## Remediation

To fix this issue, `token.split_owners` and `token.approvals` should be restored if the transfer fails.

## Code Diff

### File: `mb-store/src/core.rs`

```rust
#[payable]
pub fn nft_transfer_call(
    &mut self,
    receiver_id: AccountId,
    token_id: U64,
    approval_id: Option<u64>,
    msg: String,
) -> Promise {
    ...
    // prevent race condition, temporarily lock-replace owner
    let owner_id = AccountId::new_unchecked(token.owner_id.to_string());
    + let approvals = token.approvals.clone();
    + let split_owners = token.split_owners.clone();
    self.transfer_internal(&mut token, receiver_id.clone(), true);
    log_nft_transfer(
        &receiver_id,
        token_id_u64,
        &None,
        owner_id.to_string(),
    );
    self.lock_token(&mut token);
    ext_nft_on_transfer::ext(receiver_id.clone())
        .with_static_gas(gas::NFT_TRANSFER_CALL)
        .nft_on_transfer(pred, owner_id.clone(), token_id, msg)
        .then(
            store_self::ext(env::current_account_id())
                .with_static_gas(gas::NFT_TRANSFER_CALL)
                .nft_resolve_transfer(
                    owner_id,
                    receiver_id,
                    token_id.0.to_string(),
                    None,
                    + approvals,
                    + split_owners,
                ),
        )
}

#[private]
pub fn nft_resolve_transfer(
    &mut self,
    owner_id: AccountId,
    receiver_id: AccountId,
    token_id: String,
    // NOTE: might borsh::maybestd::collections::HashMap be more appropriate?
    approved_account_ids: Option<HashMap<AccountId, u64>>,
    + approvals: HashMap<AccountId, u64>,
    + split_owners: Option<SplitOwners>,
) -> bool {
    let l = format!(
        - "owner_id={} receiver_id={} token_id={} split_owners={:?} pred={}",
        + "owner_id={} receiver_id={} token_id={} approved_ids={:?} approvals={:?} split_owners={:?} pred={}",
        owner_id,
        receiver_id,
        token_id,
        approved_account_ids,
        + approvals,
        + split_owners,
        env::predecessor_account_id()
    );
    ...
    if !must_revert {
        true
    } else {
        self.transfer_internal(&mut token, owner_id.clone(), true);
        + token.approvals = approvals;
        + token.split_owners = split_owners;
        log_nft_transfer(
            &owner_id,
            token_id_u64,
            &None,
            receiver_id.to_string(),
        );
        false
    }
}
```

## Patch

Resolved in commit `189b0bb`.

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

