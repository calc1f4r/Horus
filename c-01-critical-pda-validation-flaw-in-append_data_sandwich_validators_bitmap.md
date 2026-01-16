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
solodit_id: 58694
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

[C-01] Critical PDA validation flaw in `append_data_sandwich_validators_bitmap`

### Overview


Severity: High

Description: The instruction `append_data_sandwich_validators_bitmap` is not properly validating the `sandwich_validators` PDA account. This allows one authority to add data to the PDA account of a different authority, resulting in unauthorized state modifications and potentially leading to cross-authority data corruption or manipulation. This is a critical security risk.

Recommendations: The PDA account should be derived inside the `AppendDataSandwichValidatorsBitmap` context instead of using the passed account to the instruction.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** High

## Description

The `append_data_sandwich_validators_bitmap` instruction does **not correctly validate** the `sandwich_validators` PDA account. Specifically, the `AppendDataSandwichValidatorsBitmap` context used in this instruction is not Deriving the PDA account from the seeds. 

This flaw allows one authority to **append data to the validator bitmap of a different authority’s PDA**, leading to **unauthorized state modifications**.

Unlike a benign validation oversight, this issue poses a **critical security risk**, as it breaks isolation between authorities and can lead to **cross-authority data corruption or manipulation** and will re-write the Data of that PDA account from the 16th byte making it as a critical bug.

## Recommendations

Derive the PDA account inside AppendDataSandwichValidatorsBitmap instead of using the passed account to the instruction :
```rust
pub struct AppendDataSandwichValidatorsBitmap<'info> {
@>   #[account(mut,
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

