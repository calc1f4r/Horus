---
# Core Classification
protocol: Orderly Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46775
audit_firm: OtterSec
contest_link: https://orderly.network/
source_link: https://orderly.network/
github_link: https://github.com/OrderlyNetwork

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
  - Nicholas R. Putra
  - Akash Gurugunti
  - Robert Chen
---

## Vulnerability Title

Denial Of Service Due To Authority Change

### Overview


The bug report describes an issue with the OAppLzReceive instruction, which is used to send tokens received through LayerZero. The problem occurs when the receiver_token_account is frozen, meaning it cannot be used to receive tokens. Instead of throwing an error, the instruction emits an event, which allows the user to continue with the transaction. This could potentially lead to a failed transaction if the receiver_token_account is frozen. The bug report suggests implementing token tracking and a withdrawal function for the admin to resolve this issue. The bug has been fixed in version 09c4980.

### Original Finding Content

## OAppLzReceive Instruction

In the OAppLzReceive instruction, the `receiver_token_account` is used to send the tokens received through LayerZero. The `receiver_token_account` is the ATA (Associated Token Account) for the receiver on `token_mint`.

While transferring the received funds, an event is emitted instead of erroring out if the `receiver_token_account` is frozen, presumably to ensure the user is not able to fail the execution of the instruction by freezing the token account.

> _src/instructions/oappinstr/oapplzreceive.rs rust_
```rust
if ctx.accounts.receiver_token_account.is_frozen() {
    emit!(Into::<FrozenWithdrawn>::into(vault_withdraw_params.clone()));
} else {
    transfer(
        ctx.accounts
            .transfer_token_ctx()
            .with_signer(&[&vault_authority_seeds[..]]),
        amount_to_transfer, // should be u64 here
    )?;
    emit!(Into::<VaultWithdrawn>::into(vault_withdraw_params.clone()));
}
```

Although the user could change the authority of the `receiver_token_account` to a different public key other than the receiver to make the instruction fail.

## Remediation

Implement token tracking and a withdrawal function for the admin.

## Patch

Resolved in commit `09c4980`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Orderly Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Akash Gurugunti, Robert Chen |

### Source Links

- **Source**: https://orderly.network/
- **GitHub**: https://github.com/OrderlyNetwork
- **Contest**: https://orderly.network/

### Keywords for Search

`vulnerability`

