---
# Core Classification
protocol: Parrot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48690
audit_firm: OtterSec
contest_link: https://parrot.fi/mint/
source_link: https://parrot.fi/mint/
github_link: github.com/gopartyparrot/parrot-monorepo.

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
finders_count: 4
finders:
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Refactoring Constraints Using has_one Attribute

### Overview

See description below for full details.

### Original Finding Content

## Simplifying Constraints in Anchor

In many instructions, the constraints on accounts can be simplified by using the `has_one` attribute of Anchor.

## Example

```rust
// src/lib.rs
pub struct UpdateDebtType<'info> {
    #[account(mut)]
    debt_type: Box<Account<'info, DebtType>>,
    /// CHECK: ..
    #[account(constraint = &debt_type.owner == owner.key)]
    owner: AccountInfo<'info>,
}
```

These are constraints that can be refactored using `has_one`:

1. **UpdateDebtType instruction** -> owner
2. **BurnDebtOriginator instruction** -> owner, debt_originator, debt_token
3. **InitVaultType instruction** -> owner
4. **UpdateVaultType instruction** -> owner
5. **InvestFromVaultType instruction** -> owner, collateral_token_holder
6. **CollectVaultInterests instruction** -> owner, debt_originator, interests_holder
7. **Stake instruction** -> collateral_to (rename to `collateral_token_holder` and use `has_one`)
8. **Borrow instruction** -> debt_token, debt_originator, collateral_token_mint (rename to `collateral_token`), oracle (rename to `price_oracle`)
9. **Repay instruction** -> debt_token, debt_originator
10. **Unstake instruction** -> debt_token, oracle, collateral_token, collateral_token_holder
11. **Liquidate instruction** -> oracle, collateral_token, collateral_token_holder, debt_token, debt_originator

## Remediation

These constraints can be refactored and simplified by using the `has_one` attribute of Anchor.

```rust
// src/lib.rs
pub struct UpdateDebtType<'info> {
    #[account(mut, has_one = owner)]
    debt_type: Box<Account<'info, DebtType>>,
    owner: Signer<'info>,
}
```

© 2022 OtterSec LLC. All Rights Reserved.  
Parrot Audit 06 | General Findings

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Parrot |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://parrot.fi/mint/
- **GitHub**: github.com/gopartyparrot/parrot-monorepo.
- **Contest**: https://parrot.fi/mint/

### Keywords for Search

`vulnerability`

