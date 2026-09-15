---
# Core Classification
protocol: Exponent Jito Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46729
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core/tree/fix-kysol-market-calc

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Code Maturity

### Overview

See description below for full details.

### Original Finding Content

## Jito Restaking Admin Control Guidelines

## 1. Utilize `init_if_needed` for Token Escrow Account

In the `InitSy` instruction, make sure to use `init_if_needed` for the `token_vrt_escrow` account. This ensures that the account is created only if it does not already exist.

```rust
// jito_restaking_standard/src/instructions/admin/init_sy.rs
pub struct InitSy<'info> {
    [...]
    #[account(
        associated_token::authority = sy_meta,
        associated_token::mint = vrt_mint,
        associated_token::token_program = token_program,
    )]
    pub token_vrt_escrow: InterfaceAccount<'info, TokenAccount>,
    [...]
}
```

## 2. Establish Independent Administrative Controls for Jito Restaking

Currently, Jito Restaking utilizes `marginfi_standard` from `admin_state` for all admin instructions. As a result, those with administrative control over MarginFi automatically gain access to Jito Restaking’s admin functions unnecessarily. This creates challenges in establishing granular controls specific to Jito Restaking.

### Action Item
Create a new set of principles specific to Jito Restaking to ensure that admin control over Jito Restaking remains independent.

## Remediation
Implement the above-mentioned suggestions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Jito Restaking |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core/tree/fix-kysol-market-calc
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

