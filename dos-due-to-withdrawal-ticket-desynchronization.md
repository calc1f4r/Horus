---
# Core Classification
protocol: Jito Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46925
audit_firm: OtterSec
contest_link: https://www.jito.network/
source_link: https://www.jito.network/
github_link: https://github.com/jito-foundation/restaking

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
finders_count: 2
finders:
  - Robert Chen
  - Nicola Vella
---

## Vulnerability Title

DOS Due to Withdrawal Ticket Desynchronization

### Overview


This report discusses a potential attack on a system that manages VRT tokens. The attack can occur if an attacker manipulates the system by sending tokens directly to a specific account. This can cause inconsistencies between the recorded amount of tokens in different accounts, leading to a denial-of-service scenario. The issue has been identified and resolved in a recent update.

### Original Finding Content

## Denial of Service (DoS) Vulnerability in vault_program::process_burn_withdrawal_ticket

There is a potential Denial of Service (DoS) attack in `vault_program::process_burn_withdrawal_ticket` that may occur if an attacker manipulates the state of the system by directly sending VRT tokens to the `vault_staker_withdrawal_ticket_token_account`. This will result in inconsistencies between the amount of VRT tokens recorded in the token account and the amount recorded in the `VaultStakerWithdrawalTicket` account.

The direct transfer will increase the balance of tokens in the token account without updating `VaultStakerWithdrawalTicket`, creating a desynchronization between these two values since `vault_staker_withdrawal_ticket.vrt_amount()` would still reflect the original amount of tokens expected by the withdrawal process.

## Relevant Code Snippet

```rust
pub fn process_burn_withdrawal_ticket(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    min_amount_out: u64,
) -> ProgramResult {
    [...]
    // close token account
    invoke_signed(
        &close_account(
            &spl_token::id(),
            vault_staker_withdrawal_ticket_token_account.key,
            staker.key,
            vault_staker_withdrawal_ticket_info.key,
            &[],
        )?,
        &[
            vault_staker_withdrawal_ticket_token_account.clone(),
            staker.clone(),
            vault_staker_withdrawal_ticket_info.clone(),
        ],
        &[&seed_slices],
    )?;
    close_program_account(program_id, vault_staker_withdrawal_ticket_info, staker)?;
    [...]
}
```

The `close_account` checks that the amount stored in the token account is zero before allowing the account to be closed. If the amounts are out of sync, the `close_account` operation may fail, as it verifies that the account’s balance is zero. This effectively prevents the staker from closing their withdrawal ticket and claiming tokens, resulting in a denial-of-service scenario.

## Remediation

Ensure the program always verifies the actual balance of the token account directly via SPL Token Program methods before allowing operations that rely on the amount of tokens.

## Patch

Resolved in PR#140.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jito Restaking |
| Report Date | N/A |
| Finders | Robert Chen, Nicola Vella |

### Source Links

- **Source**: https://www.jito.network/
- **GitHub**: https://github.com/jito-foundation/restaking
- **Contest**: https://www.jito.network/

### Keywords for Search

`vulnerability`

