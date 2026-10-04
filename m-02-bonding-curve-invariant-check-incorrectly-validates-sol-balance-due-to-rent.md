---
# Core Classification
protocol: Pump Science
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49578
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-pump-science
source_link: https://code4rena.com/reports/2025-01-pump-science
github_link: https://code4rena.com/audits/2025-01-pump-science/submissions/F-589

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
  - Evo
---

## Vulnerability Title

[M-02] Bonding Curve Invariant Check Incorrectly Validates SOL Balance Due to Rent Inclusion

### Overview


The report discusses a bug in the Pump Science program's bonding curve invariant check. This check fails to properly account for rent when comparing SOL balances, leading to incorrect validation of the protocol's core invariant. This is due to the fact that the `sol_escrow_lamports` variable, which includes rent, is compared directly to the `real_sol_reserves` variable, which tracks only the actual SOL reserves without rent. As a result, the check could pass when it should fail. The report recommends subtracting the rent-exemption amount from `sol_escrow_lamports` before comparing it to `real_sol_reserves` in the invariant check to mitigate this issue.

### Original Finding Content



<https://github.com/code-423n4/2025-01-pump-science/blob/main/programs/pump-science/src/state/bonding_curve/curve.rs# L306>

The bonding curve invariant check fails to account for rent when comparing SOL balances, leading to incorrect validation of the protocol’s core invariant. Since `sol_escrow_lamports` includes rent while `real_sol_reserves` doesn’t, the invariant check could pass when it should fail.

### Proof of Concept

The issue exists in the bonding curve invariant check in [curve.rs:L306](https://github.com/code-423n4/2025-01-pump-science/blob/main/programs/pump-science/src/state/bonding_curve/curve.rs# L306):
```

// Get raw lamports which includes rent
let sol_escrow_lamports = sol_escrow.lamports();

// Ensure real sol reserves are equal to bonding curve pool lamports
if sol_escrow_lamports < bonding_curve.real_sol_reserves {
    msg!(
        "real_sol_r:{}, bonding_lamps:{}",
        bonding_curve.real_sol_reserves,
        sol_escrow_lamports
    );
    msg!("Invariant failed: real_sol_reserves != bonding_curve_pool_lamports");
    return Err(ContractError::BondingCurveInvariant.into());
}
```

The issue arises because:

1. `sol_escrow_lamports` is retrieved using `lamports()` which returns the total balance including rent
2. This is compared directly against `real_sol_reserves` which tracks only the actual SOL reserves without rent
3. The comparison `sol_escrow_lamports < bonding_curve.real_sol_reserves` will incorrectly pass when `sol_escrow_lamports` has insufficient SOL (excluding rent) but the rent amount makes up the difference

For example:

* If `real_sol_reserves` = 100 SOL (100,000,000,000 lamports)
* And actual available SOL = 99.99795072 SOL (99,997,960,720 lamports)
* And rent = 0.00204928 SOL (2,039,280 lamports)
* Then `sol_escrow_lamports` = 100 SOL (100,000,000,000 lamports)
* The check 100 < 100 is false, so the invariant passes
* But it should fail since the actual available SOL (99.99795072) is less than required (100)

Evidence of the original intent to handle rent can be seen in the commented out code:
```

// let rent_exemption_balance: u64 =
//     Rent::get()?.minimum_balance(8 + BondingCurve::INIT_SPACE as usize);
// let bonding_curve_pool_lamports: u64 = lamports - rent_exemption_balance;
```

Which will cause the issue.

### Recommended Mitigation Steps

Subtract the rent-exemption amount from `sol_escrow_lamports` before comparing to `real_sol_reserves` in the invariant check.

**Kulture (Pump Science) confirmed**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Pump Science |
| Report Date | N/A |
| Finders | Evo |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-pump-science
- **GitHub**: https://code4rena.com/audits/2025-01-pump-science/submissions/F-589
- **Contest**: https://code4rena.com/reports/2025-01-pump-science

### Keywords for Search

`vulnerability`

