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
solodit_id: 46761
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

Utilization of Improper Payer Account

### Overview


This bug report discusses an issue with the use of two different accounts in the marketplace program. In the first function, the list_state account is used as the payer for a Cross-Program Invocation, which can result in the transaction failing if the account does not have enough funds. In the second function, the rent_destination account is also used as the payer, which can cause the delisting process to fail if the account is not a signer. To fix this issue, the report suggests using a user-provided payer account in the first function and utilizing the DelistCore.owner account in the second function. This issue has been resolved in a recent patch.

### Original Finding Content

## Close Expired Listing and Delist Core Functionality

In `close_expired_listing::process_close_expired_listing_core`, the `list_state` account is currently utilized as the payer for the `TransferV1CpiBuilder` CPI (Cross-Program Invocation). The `list_state` account is a program-owned account that holds metadata and operational data for the listing. Such accounts are generally funded only with enough lamports to cover rent. If the `list_state` account lacks sufficient lamports to cover the cost of the CPI invocation, the transaction will fail, resulting in the cleanup of the expired listing to revert.

> _ marketplace/program/src/instructions/mpl_core/close_expired_listing.rs rust
```rust
pub fn process_close_expired_listing_core<'info>(
    ctx: Context<'_, '_, '_, 'info, CloseExpiredListingCore<'info>>,
) -> Result<()> {
    [...]
    TransferV1CpiBuilder::new(&ctx.accounts.mpl_core_program)
        .asset(&ctx.accounts.asset)
        .authority(Some(&ctx.accounts.list_state.to_account_info()))
        .new_owner(&ctx.accounts.owner.to_account_info())
        .payer(&ctx.accounts.list_state.to_account_info()) // pay for what?
        .collection(ctx.accounts.collection.as_ref().map(|c| c.as_ref()))
        .invoke_signed(&[&ctx.accounts.list_state.seeds()])?;
    [...]
}
```

Similarly, in `delist::process_delist_core`, the `rent_destination` account is utilized as the payer in the `TransferV1CpiBuilder`. This enforces an unnecessary requirement that the `rent_destination` account should be a signer. The `rent_destination` account is not supposed to be responsible for paying transaction fees. Its role is to receive any refunded rent when the `list_state` account is closed, not to pay for the transfer itself. As a result of the constraint, the delisting may fail if the `rent_destination` is not a signer.

> _ marketplace/program/src/instructions/mpl_core/delist.rs rust
```rust
pub fn process_delist_core<'info>(
    ctx: Context<'_, '_, '_, 'info, DelistCore<'info>>,
) -> Result<()> {
    [...]
    TransferV1CpiBuilder::new(&ctx.accounts.mpl_core_program)
        .asset(&ctx.accounts.asset)
        .authority(Some(&ctx.accounts.list_state.to_account_info()))
        .new_owner(&ctx.accounts.owner.to_account_info())
        .payer(&ctx.accounts.rent_destination) // pay for what?
        .collection(ctx.accounts.collection.as_ref().map(|c| c.as_ref()))
        .invoke_signed(&[&ctx.accounts.list_state.seeds()])?;
    [...]
}
```

## Remediation

Replace `list_state` with a user-provided payer account in `process_close_expired_listing_core`, and utilize the `DelistCore.owner` account in `process_delist_core`.

## Patch

Resolved in #62.

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

