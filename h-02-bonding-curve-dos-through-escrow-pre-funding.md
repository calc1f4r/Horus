---
# Core Classification
protocol: PumpScience_2024-12-24
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45297
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
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

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Bonding Curve DOS through escrow pre-funding

### Overview


The bug report states that an attacker can fund the sol_escrow account with SOL before the bonding curve is created. This is possible because the account's address can be calculated by anyone who knows the mint address, and anyone can send SOL to this address before the curve is created. The code also has an invariant check that will fail if SOL is present in the escrow account. To fix this, it is recommended to either initialize the `real_sol_reserves` value to match any existing SOL balance in the account during creation, or to add a mechanism that will transfer any existing SOL to the creator or administrator before continuing with curve creation.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The sol_escrow account can be preemptively funded with SOL by an attacker before the bonding curve is created. Since the `create_bonding_curve` instruction initializes `real_sol_reserves` to 0, but the invariant check verifies that the actual SOL balance matches this value, the presence of any SOL in the escrow account will cause the curve creation to fail.

This is possible because:

- The sol_escrow PDA address is deterministic and can be calculated by anyone who knows the mint address
- Anyone can send SOL to this address before the curve is created
- The invariant strictly enforces `sol_escrow_lamports == real_sol_reserves`

Code snippets:

```rust
// In create_bonding_curve.rs
pub fn handler(ctx: Context<CreateBondingCurve>, params: CreateBondingCurveParams) -> Result<()> {
    // real_sol_reserves initialized to 0
    ctx.accounts.bonding_curve.update_from_params(...);

    // Invariant check will fail if escrow has SOL
    BondingCurve::invariant(locker)?;
}

// In curve.rs
pub fn invariant<'info>(ctx: &mut BondingCurveLockerCtx<'info>) -> Result<()> {
    if sol_escrow_lamports != bonding_curve.real_sol_reserves {
        return Err(ContractError::BondingCurveInvariant.into());
    }
}
```

## Recommendations

Initialize `real_sol_reserves` to match any existing SOL balance in the escrow during creation.

If that's not desirable, add a SOL sweep mechanism during curve creation that transfers any existing SOL to the creator, for example:

- Check if there's any existing SOL in the escrow
- If found, sweep it to the creator/admin using a signed CPI
- Then continue with regular curve creation

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | PumpScience_2024-12-24 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

