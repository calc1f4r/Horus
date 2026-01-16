---
# Core Classification
protocol: ComposableFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47369
audit_firm: OtterSec
contest_link: https://www.picasso.network/
source_link: https://www.picasso.network/
github_link: https://github.com/ComposableFi/emulated-light-client

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
  - Ajay Shankar Kunapareddy
  - Akash Gurugunti
---

## Vulnerability Title

Lack Of Instruction Sysvar Validation

### Overview


This bug report discusses an issue with the instruction sysvar account, which is used for deposit and set_service instructions. The validation for this account is not being performed in two specific functions, validate_remaining_accounts and set_stake, which could potentially allow for unauthorized instructions to be injected into CPI calls. The report suggests that the fix for this issue is to include explicit validation for the instruction sysvar account in these functions. This has been fixed by checking the instruction sysvar account in b221448.

### Original Finding Content

## Instruction Sysvar Account Vulnerability

The instruction sysvar account is passed to both `deposit` and `set_service` instructions, but its validation is not performed in `validate_remaining_accounts` and `set_stake`. Thus, it may be possible to replace or manipulate the instruction sysvar account; they might be able to inject unauthorized instructions into the CPI calls.

> _restaking/programs/restaking/src/lib.rs_

## Deposit Struct

```rust
#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub depositor: Signer<'info>,
    [...]
    /// CHECK:
    pub instruction: AccountInfo<'info>,
    [...]
}
```

## SetService Struct

```rust
#[derive(Accounts)]
pub struct SetService<'info> {
    #[account(mut)]
    pub depositor: Signer<'info>,
    [...]
    /// CHECK:
    pub instruction: AccountInfo<'info>,
    [...]
}
```

## Remediation

Both the `validation::validate_remaining_accounts` and `set_stake` should include explicit validation for the instruction sysvar account. The validations should ensure that the account’s address should match the expected value.

## Patch

Fixed by checking the instruction sysvar account in b221448.

© 2024 Otter Audits LLC. All Rights Reserved. 9/20

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | ComposableFi |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Akash Gurugunti |

### Source Links

- **Source**: https://www.picasso.network/
- **GitHub**: https://github.com/ComposableFi/emulated-light-client
- **Contest**: https://www.picasso.network/

### Keywords for Search

`vulnerability`

