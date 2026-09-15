---
# Core Classification
protocol: Hedge Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48839
audit_firm: OtterSec
contest_link: https://www.hedge.so/
source_link: https://www.hedge.so/
github_link: https://github.com/Hedge-Finance/hedge-vault/.

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
  - Robert Chen
  - Mohan Pedhapati
  - OtterSec
---

## Vulnerability Title

Hard-coded Emergency Collateral Ratio

### Overview

See description below for full details.

### Original Finding Content

## Emergency Collateral Ratio Hardcoding Issue

It was noticed that the emergency collateral ratio `emergency_mode_threshold` in the `AddCollateralType` processor is hardcoded. Once the vault is deployed, it is not possible to change this value to different collaterals, so as to have different thresholds.

## Code Snippet

```rust
processors/add_collateral_type.rs
pub fn exec(
    ctx: Context<AddCollateralType>,
    vault_type_name: String,
    loan_init_fee: u64,
    min_collateral_ratio: u64,
    interest_rate_per_second: u128,
    min_debt_per_vault: u64,
    max_debt_extended: u64,
    can_be_redeemed: bool,
    _override_current_time: i64,
) -> Result<()> {
    [...]
    // Set emergency mode threshold
    vault_type_account.emergency_mode_threshold = 150_u64;
    [...]
}
```

## Remediation

It makes more sense to use a parameter instead of a hard-coded threshold value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hedge Vault |
| Report Date | N/A |
| Finders | Robert Chen, Mohan Pedhapati, OtterSec |

### Source Links

- **Source**: https://www.hedge.so/
- **GitHub**: https://github.com/Hedge-Finance/hedge-vault/.
- **Contest**: https://www.hedge.so/

### Keywords for Search

`vulnerability`

