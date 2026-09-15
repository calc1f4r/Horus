---
# Core Classification
protocol: Aurory
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47969
audit_firm: OtterSec
contest_link: https://aurory.io/
source_link: https://aurory.io/
github_link: github.com/Aurory-Game/ocil

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
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Incorrect Account And Bump

### Overview


The withdraw_v2 function is not working correctly because it is using the wrong variables. This can cause a runtime error and prevent users from making withdrawals. To fix this, the vault_ta and vault_bump variables need to be replaced with burn_ta and burn_bump. This has been addressed in the code by replacing the incorrect variables.

### Original Finding Content

## Withdraw_v2 Runtime Error and Remediation

`Withdraw_v2` checks the `withdraw_from_burner_ta` variable to determine whether the withdrawal will occur from `burn_ta` or `vault_ta`. However, if `withdraw_from_burner_ta` is set to true, it utilizes `vault_ta` and `vault_bump` instead of `burn_ta` and `burn_bump`. This may result in a runtime error and a denial of service.

## Remediation

Replace `vault_ta` and `vault_bump` with `burn_ta` and `burn_bump` respectively.

### File: programs/casier/src/lib.rs Diff

```diff
@@ -242,11 +242,11 @@ pub mod casier {
 CpiContext::new_with_signer(
 ctx.accounts.token_program.to_account_info(),
 anchor_spl::token::Transfer {
 - from: ctx.accounts.vault_ta.to_account_info(),
 + from: ctx.accounts.burn_ta.to_account_info(),
 to: ctx.accounts.user_ta.to_account_info(),
 - authority: ctx.accounts.vault_ta.to_account_info(),
 + authority: ctx.accounts.burn_ta.to_account_info(),
 },
 - &[&[ctx.accounts.mint.key().as_ref(), &[vault_bump]]],
 + &[&[ctx.accounts.mint.key().as_ref(), &[burn_bump]]],
 ),
 withdraw_amount.into(),
 )?;
```

## Patch

Fixed in `91217b3` by replacing the `vault_ta` and `vault_bump` with `burn_ta` and `burn_bump` respectively.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aurory |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://aurory.io/
- **GitHub**: github.com/Aurory-Game/ocil
- **Contest**: https://aurory.io/

### Keywords for Search

`vulnerability`

