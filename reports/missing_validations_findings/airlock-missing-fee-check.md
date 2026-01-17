---
# Core Classification
protocol: Magna Airlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48724
audit_firm: OtterSec
contest_link: https://www.magna.so/
source_link: https://www.magna.so/
github_link: https://github.com/magna-eng/airlock-sol-ottersec

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
  - Rajvardhan Agarwal
---

## Vulnerability Title

Airlock Missing Fee Check

### Overview


The bug report states that there is an issue with the create instruction in the program. It does not check if the new_schedule.fee_destination is a valid TokenAccount, which could result in locked funds if an invalid Pubkey is provided. This can be seen in the code snippets provided. Additionally, the airlock cannot be cancelled because the fee transfer would also fail. To reproduce the bug, one can invoke the create instruction with a random Pubkey as the fee_destination, set fee_bps to a non-zero amount, and attempt to withdraw funds, which will fail due to the invalid fee account. The solution is to properly validate the fee_destination account in the create instruction and ensure it belongs to the correct mint. The bug has been fixed in the latest update.

### Original Finding Content

## Vulnerability Report: Fee Destination Validation Issue

In the create instruction, the program does not check if `new_schedule.fee_destination` is a valid `TokenAccount`. This could potentially lead to locked funds if an invalid Pubkey is provided for the fee destination account.

In the following code snippets, it can be seen that `new_schedule.fee_destination` is not properly validated.

```rust
// programs/piecewise/lib.rs
pub fn create(
    ctx: Context<Create>,
    new_schedule: PiecewiseSchedule,
    schedule_id: String,
    fund_now: bool
) -> Result<()> {
    new_schedule.validate()?;
    ctx.accounts.schedule.set_inner(new_schedule);
```

```rust
// programs/piecewise/lib.rs
pub fn validate(&self) -> Result<()> {
    [...]
    require!(0 == self.fee_bps || self.fee_destination != Pubkey::default(), UnlockErrorCode::InvalidFeeDestination);
    [...]
    Ok(())
}
```

Moreover, note that the airlock cannot be cancelled as the fee transfer would also fail.

```rust
// programs/piecewise/lib.rs
let transfer_ctx = CpiContext::new_with_signer(
    token_program.to_account_info(),
    token::Transfer {
        authority: schedule.to_account_info(),
        from: schedule_ata.to_account_info(),
        to: fee_destination.to_account_info(),
    },
    signer_seeds,
);
token::transfer(transfer_ctx, fee_amount)?;
```

## Proof of Concept

1. Invoke the create instruction with `fee_destination` as a random Pubkey.
2. `fee_bps` can be set to any non-zero amount.
3. Attempt to invoke the `withdraw_available` instruction to withdraw releasable funds. This transaction will fail as the fee account is invalid.

## Remediation

The `fee_destination` account must be passed in the create instruction and properly validated to ensure that it is a `TokenAccount` and belongs to the correct mint. For more information, please refer to the code snippet below.

```rust
// programs/piecewise/lib.rs
pub struct Create<'info> {
    [...]
    schedule_ata: Account<'info, token::TokenAccount>,
    #[account(mut, token::mint = token_mint, address = new_schedule.fee_destination)]
    fee_destination: Account<'info, token::TokenAccount>
}
```

## Patch

The `fee_destination` is now validated properly. Fixed in #12.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Magna Airlock |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.magna.so/
- **GitHub**: https://github.com/magna-eng/airlock-sol-ottersec
- **Contest**: https://www.magna.so/

### Keywords for Search

`vulnerability`

