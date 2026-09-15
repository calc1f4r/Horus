---
# Core Classification
protocol: Serum v4
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48843
audit_firm: OtterSec
contest_link: https://portal.projectserum.com/
source_link: https://portal.projectserum.com/
github_link: Repos in notes

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
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Fee tier spoofing

### Overview


This bug report is about a mistake in the new_order instruction of Dex's program. The instruction is supposed to check that a discount token account is owned by the SPL token program, but instead it checks if it is owned by the user's address. This allows an attacker to obtain fee tiers without having the necessary token balance. The fix for this issue is to replace the user's address with the SPL token program ID. This bug has already been fixed in the latest version of the program.

### Original Finding Content

## Dex's New Order Instruction Vulnerability

Dex's `new_order` instruction incorrectly checks that the `discount_token_account` account is owned by the `user_owner` address, rather than the SPL token program. This allows an attacker to obtain arbitrary fee tiers without the requisite token balance.

```rust
// dex-v4/program/src/processor/new_order.rs:L171-L177
if let Some(discount_account) = a.discount_token_account {
    check_account_owner(
        discount_account,
        a.user_owner.key,
        DexError::InvalidStateAccountOwner,
    )?;
}
```

The `user_owner` key should be compared against the parsed token authority, not the account’s intrinsic owner. Note this is already done in the `FeeTier::get` method, along with token mint validation.

```rust
// dex-v4/program/src/state.rs:L318-L330
let parsed_token_account =
    spl_token::state::Account::unpack(&account.data.borrow())?;
if &parsed_token_account.owner != expected_owner {
    msg!("The discount token account must share its owner with the user account.");
    return Err(ProgramError::InvalidArgument);
}
let (srm_held, msrm_held) = match parsed_token_account.mint {
    a if a == MSRM_MINT => (0, parsed_token_account.amount),
    a if a == SRM_MINT => (parsed_token_account.amount, 0),
    _ => {
        msg!("Invalid mint for discount token account.");
        return Err(ProgramError::InvalidArgument);
    }
};
```

## Proof of Concept
1. An attacker forges a `discount_token_account` account which is owned by their `user_owner` address rather than the SPL token program. When interpreted as an SPL token wallet, the token authority is `user_owner`, the mint is `MSRM`, and the balance is 1.
2. The attacker files a new order using `discount_token_account`, and the MSRM fee tier is applied.

To conclude, the attacker was able to use the MSRM fee tier without proving ownership of MSRM.

## Remediation
The `user_owner` key should be replaced with the SPL token program ID.

```rust
if let Some(discount_account) = a.discount_token_account {
    check_account_owner(
        discount_account,
        &spl_token::ID,
        DexError::InvalidStateAccountOwner,
    )?;
}
```

## Patch
Fixed in #49 and `47025e3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Serum v4 |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://portal.projectserum.com/
- **GitHub**: Repos in notes
- **Contest**: https://portal.projectserum.com/

### Keywords for Search

`vulnerability`

