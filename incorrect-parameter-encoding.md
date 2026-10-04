---
# Core Classification
protocol: Marginfi Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46933
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
  - Akash Gurugunti
---

## Vulnerability Title

Incorrect Parameter Encoding

### Overview


The report describes a bug in the marginfi_cpi::withdraw_from_lending_account function, which is used to withdraw funds from a lending account. The bug is related to the incorrect encoding of the withdraw_all parameter in the instruction data. This parameter is supposed to be a boolean flag, but it is incorrectly assigned as a single byte instead of a two-byte representation. This causes the Marginfi program to expect an Option<bool> but receive a single byte instead. The bug has been resolved in a patch (PR#508) and can be fixed by encoding the withdraw_all parameter as Option<bool>.

### Original Finding Content

## Issue with `withdraw_all` Parameter in `withdraw_from_lending_account`

In `marginfi_cpi::withdraw_from_lending_account`, there is an incorrect encoding of the `withdraw_all` parameter in the instruction data. `withdraw_from_lending_account` allows a user to withdraw funds from their lending account. It constructs and sends a cross-program invocation (CPI) to the Marginfi program with the appropriate parameters to perform this withdrawal.

```rust
pub fn withdraw_from_lending_account<'info>(
    ctx: CpiContext<'_, '_, '_, 'info, LendingAccountWithdraw<'info>>,
    amount: u64,
    withdraw_all: bool,
) -> Result<()> {
    [...]
}
```

One of these parameters, `withdraw_all`, is a boolean flag indicating whether to withdraw the entire balance from the lending account. However, the `withdraw_all` field in the instruction is incorrectly assigned as a single byte (1), while the Marginfi program expects the `withdraw_all` parameter to be an `Option<bool>`, which is a two-byte representation. Thus, the Marginfi program expects an `Option<bool>`, but it receives a single byte.

## Remediation

Encode the `withdraw_all` parameter as `Option<bool>`.

## Patch

Resolved in PR#508.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Marginfi Integration |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

