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
solodit_id: 48214
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

Potential Loss Of NFT Due To Unaccounted Fee

### Overview


This bug report discusses an issue with the Marketplace platform where a specific function, nft_resolve_payout_ft, may fail if the caller does not have enough funds to cover the required transaction fee. This can result in the seller losing their NFT without receiving payment. The report suggests a solution of withholding a portion of the refunded storage fee to fund the transaction. The issue has been resolved in recent updates to the platform.

### Original Finding Content

## NFT Payout and ft_transfer Overview

Requiring an attachment of one yNEAR is a common method to ensure that the caller signed the transaction with a full access key. While one yNEAR is an infinitely small value, it will potentially lead to transaction failures if the caller does not have an excessive balance to fund it.

In `nft_resolve_payout_ft`, if all previous receipts regarding NFT transfers are processed successfully, `ft_transfer` with one yNEAR attached will be called to transfer ft to each recipient.

## Code Snippets

### Core Implementation (`mb-store/src/core.rs`)

```rust
pub fn nft_resolve_payout_ft(
    &mut self,
    token_key: String,
) -> PromiseOrValue<U128> {
    ...
    for (account, amount) in payout.drain() {
        ft_transfer(ft_contract_id.clone(), account, amount.0);
    }
    if let Some(referrer_id) = offer.referrer_id {
        ft_transfer(ft_contract_id, referrer_id, ref_earning.unwrap());
    }
    ...
}
```

### Utility Function (`mb-sdk/src/utils.rs`)

```rust
pub fn ft_transfer(
    ft_contract_id: AccountId,
    receiver_id: AccountId,
    amount: Balance,
) -> Promise {
    crate::interfaces::ext_ft::ext(ft_contract_id)
        .with_attached_deposit(1)
        .with_static_gas(crate::constants::gas::FT_TRANSFER)
        .ft_transfer(receiver_id, amount.into(), None)
}
```

However, since there is no explicit funding for the attached yNEAR, the Marketplace may not have the funds required, leading to the failure of `nft_resolve_payout_ft`. 

Upon failure of `nft_resolve_payout_ft`, `ft_resolve_transfer` should roll back the previous payment and return all ft to the NFT buyer. On the other hand, changes made by `nft_transfer_payout` will not be rolled back, which leads to the seller losing NFTs without receiving payment for them. This scenario is an edge case that may only occur if the admin decides to withdraw all non-storage stake funds right before the `nft_resolve_payout_ft` receipt is processed.

The reason for the affected scenario being limited is due to NEAR distributing parts of transaction fees to contracts as developer incentives, and the reception of fees for any single transaction is likely able to cover the fee amount required for `ft_transfer` to succeed.

## Mintbase Audit 04 | Vulnerabilities

### Remediation

Withhold a part of the refunded storage fee for listing and use it to fund `ft_transfer`.

### Updated Code Snippet (`mb-interop-market/src/offers.rs`)

```rust
pub fn nft_resolve_payout_ft(
    &mut self,
    token_key: String,
) -> PromiseOrValue<U128> {
    ...
    for (account, amount) in payout.drain() {
        ft_transfer(ft_contract_id.clone(), account, amount.0);
    }
    if let Some(referrer_id) = offer.referrer_id {
        ft_transfer(ft_contract_id, referrer_id, ref_earning.unwrap());
    }
    self.listings.remove(&token_key);
    // payout length is capped at MAX_LEN_PAYOUT_FT (10)
    // withholding 11 yNEAR is enough to fund ft_transfer
    self.decrease_listings_count(&listing.nft_owner_id, 1);
    self.refund_storage_deposit(
        account,
        self.listing_storage_deposit - 11u128,
    );
    PromiseOrValue::Value(0.into())
}
```

### Patch

Resolved in commits `13d0400` and `3eef340`.

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

