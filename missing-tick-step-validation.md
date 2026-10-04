---
# Core Classification
protocol: Turbos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47252
audit_firm: OtterSec
contest_link: https://turbos.finance/
source_link: https://turbos.finance/
github_link: https://github.com/turbos-finance/liquidity-vault

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
finders_count: 3
finders:
  - Bartłomiej Wierzbiński
  - Robert Chen
  - MichałBochnak
---

## Vulnerability Title

Missing Tick Step Validation

### Overview


The bug report discusses a potential issue within the vault module. The base_tick_step and limit_tick_step values, which are user-provided inputs, are not properly validated. This means that a malicious user could enter very high values for these steps, which could result in an integer overflow and disrupt the check_rebalance function. The report suggests either validating the values in the open_vault function or using the strategy values instead. The issue has been resolved in version 9333ce4.

### Original Finding Content

## Open Vault Vulnerability

In `open_vault` within the vault module, the `base_tick_step` and `limit_tick_step` values are user-provided inputs and are not validated. This means a malicious user may enter substantially high values for these steps. Inside `check_rebalance`, these user-provided steps are multiplied by `tick_spacing`. This multiplication results in an integer overflow if the product (`limit_tick_step * tick_spacing` or `base_tick_step * tick_spacing`) is large. Consequently, the function may abort if an overflow occurs, effectively disrupting `check_rebalance_loop` and influencing the re-balancing logic.

```rust
> _vault.move_rust
public fun check_rebalance<CoinTypeA, CoinTypeB, FeeType>(
    global_config: &GlobalConfig,
    strategy: &mut Strategy,
    vault_id: ID,
    clmm_pool: &mut Pool<CoinTypeA, CoinTypeB, FeeType>,
    ctx: &mut TxContext
): CheckRebalance {
    [...]
    let base_tick_step = vault_info.base_tick_step;
    let limit_tick_step = vault_info.limit_tick_step;
    [...]
}
```

## Remediation

Either validate the values of `base_tick_step` and `limit_tick_step` in `open_vault` or utilize the strategy values instead.

## Patch

Resolved in `9333ce4` 

© 2024 Otter Audits LLC. All Rights Reserved. 7/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Turbos |
| Report Date | N/A |
| Finders | Bartłomiej Wierzbiński, Robert Chen, MichałBochnak |

### Source Links

- **Source**: https://turbos.finance/
- **GitHub**: https://github.com/turbos-finance/liquidity-vault
- **Contest**: https://turbos.finance/

### Keywords for Search

`vulnerability`

