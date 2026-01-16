---
# Core Classification
protocol: Pump_2025-06-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63280
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Pump-security-review_2025-06-26.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Any wallet can self-assign as super_admin for arbitrary mint

### Overview


This bug report discusses a medium severity issue where an arbitrary signer can be accepted as a super_admin during the initialization process. This means that there is no verification of the relationship between the signer and the target mint. This can be exploited by anyone to disable the whitelist and take control without any risk or major cost. The report recommends that the initialization process should be controlled by the mint authority.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

An arbitrary signer is accepted as super_admin at initialize_extra_account_metas and does not verify any relationship between that signer and the target mint:

```
#[account(init, seeds = [TRANSFER_HOOK_STATE_SEED.as_bytes(), mint.key().as_ref()], ...)]
pub transfer_hook_state: Account<'info, TransferHookState>,
```

There is no constraint on mint.mint_authority or mint.freeze_authority.
No additional account (e.g., extension authority) is required to sign.
Once the PDA at [TRANSFER_HOOK_STATE_SEED, mint] is initialized, we cannot initialize it again.

Due to the mentioned points, anyone can initialize the PDA before the real token team, disable the whitelist, and walk away with no risk or major cost.

Because toggle_off_transfer_whitelist is one-way, there is no recovery path.

## Recommendations

Gate initialization behind mint authority control:

```
pub struct InitializeExtraAccountMeta<'info> {
    #[account(constraint = mint.mint_authority == COption::Some(super_admin.key()).into())]
    pub mint: InterfaceAccount<'info, Mint>,
    #[account(mut, signer)]
    pub super_admin: Signer<'info>,
    // ...
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pump_2025-06-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Pump-security-review_2025-06-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

