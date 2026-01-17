---
# Core Classification
protocol: Exponent Generic Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53215
audit_firm: OtterSec
contest_link: https://www.exponent.finance/income
source_link: https://www.exponent.finance/income
github_link: https://github.com/exponent-finance/exponent-core

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - Robert Chen
---

## Vulnerability Title

Incorrect Hook Length Allocation

### Overview

See description below for full details.

### Original Finding Content

## ModifyHook Reallocation Explanation

Currently, in `ModifyHook`, the reallocation of the `SyMeta` account is based on the lengths of `pre_mint_hook_discriminator` and `post_redeem_hook_discriminator` within the meta account. The reallocating logic looks at the current lengths of these fields in the meta account to determine how much space needs to be allocated. If the new hook configuration has a different length for these discriminators, the meta account’s reallocation may not be appropriate.

> _ src/instructions/admin/modify_hook.rs rust

```rust
#[derive(Accounts)]
pub struct ModifyHook<'info> {
    [...]
    #[account(
        mut,
        // realloc to make room for one new emission
        realloc = SyMeta::len(meta.emissions.len(), meta.interface_accounts.len(),
        meta.hook.pre_mint_hook_discriminator.len(),
        meta.hook.post_redeem_hook_discriminator.len()),
        realloc::payer = fee_payer,
        realloc::zero = false,
    )]
    pub meta: Account<'info, SyMeta>,
    [...]
}
```

## Remediation

Utilize the lengths of the hook discriminators from the input hook passed as part of the instruction, rather than from the meta account.

## Patch

Resolved in #1913.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Generic Standard |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://www.exponent.finance/income
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/income

### Keywords for Search

`vulnerability`

