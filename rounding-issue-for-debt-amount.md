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
solodit_id: 48688
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

Rounding Issue for Debt Amount

### Overview

See description below for full details.

### Original Finding Content

## Repay Instruction Summary

In the Repay instruction, the repay amount for debt is rounded downwards. The remaining fractional part of the debt is cleared as dust.

```rust
let repay_amount = vault.floor_to_debt_amount(amount);
vault_type.decrease_debt(repay_amount)?;
vault.decrease_debt_and_clear_dust(repay_amount)?;
```

## Decrease Debt and Clear Dust Function

```rust
fn decrease_debt_and_clear_dust(&mut self, amount: u64) -> Result<()> {
    fp_sub(&mut self.debt_amount, amount)?;
    if Fix::from_bits(self.debt_amount) < 1 {
        self.debt_amount = 0;
    }
    Ok(())
}
```

## Issues

This leads to two issues:

1. The value of `total_debt` in `VaultType` becomes out-of-sync, since the fractional part is remaining in the `total_debt`.
2. A user can skip a small amount of interest, but the interest amount was getting collected by the admin from `debt_originator`.

## Proof of Concept

Let’s assume that `interestRate = 292471208 / 2**64` for one slot equals 400ms.

1. `interest_accum = interestRate * (2.5 * 3600 * 24) = 3.4246575 * 10**(-6)` (for one day)
2. `debt_amount = 0.000292 BTC` (7 dollars).
3. `interest = 292000 * 3.4246575 * 10**(-6) = 0.99999999` (which is cleared as dust)

Using this method, a user can skip interest of `0.000292 BTC` (~7 dollars) for 1 day in one account. A malicious attacker can use multiple accounts to get much more debt without interest.

---

© 2022 OtterSec LLC. All Rights Reserved. 

## Remediation

Round the interest amount of the Vault upwards while collecting interest from Vault.

## Patch

The interest amount was rounded up in the `Vault.collect_interest` function. Fixed in commit `50ae25c`.

```diff
let fp_accrued_interests = fp_vault_type_interest_accum
// NOTE: fp_vault_type_interest_accum >
.sub(fp_vault_interest_accum)
.checked_mul(fp_vault_debt_amount)
.ok_or(ParrotError::NumberOverflow)?
+ .ceil();
```

---

© 2022 OtterSec LLC. All Rights Reserved.

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

