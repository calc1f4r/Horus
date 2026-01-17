---
# Core Classification
protocol: Gatekeeper_2025-06-28
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58695
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gatekeeper-security-review_2025-06-28.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Improper PDA validation in `handler` enables arbitrary data clearing

### Overview


This report describes a bug in the `clear_data_sandwich_validators_bitmap` instruction that can lead to unauthorized modification of account data. The handler does not properly validate the PDA account, which allows a malicious signer to supply a different PDA account and still pass the check. This can result in the incorrect clearing of bitmap data belonging to a different PDA, potentially wiping valid data belonging to another authority. To fix this, it is recommended to derive the PDA account in the `ClearDataSandwichValidatorsBitmap` struct itself.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** High

## Description

The `clear_data_sandwich_validators_bitmap` instruction's handler does **not properly validate** the `sandwich_validators` PDA account. This oversight allows a malicious signer to **supply a different PDA account** (belonging to another signer or authority) and still pass the check.

As a result, the handler may **incorrectly clear bitmap data** belonging to a different PDA by potentially **wiping valid data**  corresponding to another authority.

This poses a **critical risk**, as it enables unauthorized modification of account data that should be protected by strict PDA derivation and validation.

## Recommendations

Derive the PDA account in the `ClearDataSandwichValidatorsBitmap` struct it self like below :
```rust
pub struct ClearDataSandwichValidatorsBitmap<'info> {
    
@>  #[account(
        mut,
        seeds = [SandwichValidators::SEED_PREFIX, multisig_authority.key().as_ref(), &epoch_arg.to_le_bytes()],
        bump
    )]
    pub sandwich_validators: AccountLoader<'info, SandwichValidators>,
    #[account(mut)]
    pub multisig_authority: Signer<'info>,
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gatekeeper_2025-06-28 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gatekeeper-security-review_2025-06-28.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

