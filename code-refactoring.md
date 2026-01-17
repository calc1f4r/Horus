---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46817
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Code Refactoring

### Overview

See description below for full details.

### Original Finding Content

## Adrena Audit 05 — General Findings

## 1. Internal Position Functions

In `internal_increase_position_short`, `internal_increase_position_long`, `internal_open_position_short`, `internal_open_position_long`, and `internal_swap` do not need to be invoked with `transfer_authority` signer.

> Source: `_adrena/src/state/cortex.rs`

```rust
pub fn internal_increase_position_short<'a>([...]) -> Result<()> {
    [...]
    let cpi_context = anchor_lang::context::CpiContext::new(cpi_program, cpi_accounts)
        .with_signer(authority_seeds);
    [...]
}
```

## 2. Custody Accounting Update

In `custody::update_accounting_after_open_position_short`, the division and multiplication by `position.price` for the calculation of `accounting.weighted_price` may be avoided as the division and subsequent multiplication by `position.price` can cancel each other out. Thus, calculating `quantity` separately for this purpose is unnecessary. `weighted_price` may be directly computed as `position_size_usd as u128 * Cortex::BPS_POWER`.

> Source: `_adrena/src/state/custody.rs`

```rust
pub fn update_accounting_after_open_position_short(
    [...]
) -> Result<()> {
    [...]
    // Update weight and quantity
    {
        [...]
        let quantity = (position_size_usd as u128 * Cortex::BPS_POWER) / position.price as u128;
        accounting.weighted_price += position.price as u128 * quantity;
        accounting.total_quantity += quantity;
    }
    Ok(())
}
```

## 3. Liquidation Stats Increment

`stats.liquidation_position_count` is incremented with `+=` in `liquidate_short` and with `saturating_add` in `liquidate_long`. Utilize the same method in both functions for consistency.

---

## Remediation

Incorporate the above-stated modifications.

## Patch

3 resolved in e418473

---

© 2024 Otter Audits LLC. All Rights Reserved. 52 / 59

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

