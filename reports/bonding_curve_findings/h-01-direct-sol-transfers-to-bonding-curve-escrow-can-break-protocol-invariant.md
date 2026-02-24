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
solodit_id: 45296
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

[H-01] Direct SOL transfers to bonding curve escrow can break protocol invariant

### Overview


This bug report discusses a problem with the bonding curve protocol. The protocol has a rule that the amount of SOL in the `bonding_curve_sol_escrow` account must match the `real_sol_reserves` state variable. However, this rule is only checked during swap operations and does not account for external transfers to the escrow account. This can cause the protocol to stop working until fixed. The report recommends adding a function to synchronize the `real_sol_reserves` with the actual SOL balance in the escrow account.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The bonding curve protocol maintains an invariant that the `real_sol_reserves` state variable must exactly match the SOL balance (lamports) in the `bonding_curve_sol_escrow` account. This invariant is checked at the end of every swap operation:

```rust
if sol_escrow_lamports != bonding_curve.real_sol_reserves {
    msg!(
        "real_sol_r:{}, bonding_lamps:{}",
        bonding_curve.real_sol_reserves,
        sol_escrow_lamports
    );
    msg!("Invariant failed: real_sol_reserves != bonding_curve_pool_lamports");
    return Err(ContractError::BondingCurveInvariant.into());
}
```

However, the `real_sol_reserves` is only updated during swap operations, while the escrow account's SOL balance can be modified externally through direct transfers. An external SOL transfer to the escrow would increase `sol_escrow_lamports` without updating `real_sol_reserves`, causing the invariant check to fail and making the protocol unusable until fixed.

Note: check the other issue "DOS Attack Vector on Bonding Curve Creation Through Escrow Pre-funding" as it is similiar.

## Recommendations

Add a cleanup function that can synchronize `real_sol_reserves` with the actual lamport balance if needed.

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

