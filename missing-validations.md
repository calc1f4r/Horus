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
solodit_id: 47255
audit_firm: OtterSec
contest_link: https://turbos.finance/
source_link: https://turbos.finance/
github_link: https://github.com/turbos-finance/liquidity-vault

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
  - Bartłomiej Wierzbiński
  - Robert Chen
  - MichałBochnak
---

## Vulnerability Title

Missing Validations

### Overview

See description below for full details.

### Original Finding Content

## Audit Findings

## Findings

1. **Faulty Validation in Configuration**
   - The functions `config::add_operator` and `config::set_tier` are missing a version validation check, resulting in possible version mismatch errors. The functions should call `checked_package_version(global_config)` to ensure the current package version in the `GlobalConfig` matches the constant defined in the module (`VERSION`).

2. **Package Version Check**
   - The function `set_package_version` fails to explicitly check whether the new version is an upgrade (i.e., whether the new version is greater than the old version). If someone accidentally attempts to set a version lower than the current version (downgrade), the function will still update the configuration without raising any warnings. The function should check that the `new_version` is greater than `global_config.package_version`.

3. **Explicit Validation of Parameters**
   - When the `vault`, `clmm_pool`, and `strategy` objects are passed as parameters to functions, explicitly validate their relationships to ensure data consistency and prevent possible manipulation of values.

4. **Recipient Address Validation**
   - The function `vault::collect_clmm_reward_direct_return` should validate the recipient address before using it, as the recipient argument may be manipulated to spoof this value in the emitted event.

   ```rust
   > _vault.move_rust
   public fun collect_clmm_reward_direct_return<CoinTypeA, CoinTypeB, FeeType,
   → RewardCoinType>(
       global_config: &GlobalConfig,
       strategy: &mut Strategy,
       vault: &Vault,
       clmm_pool: &mut Pool<CoinTypeA, CoinTypeB, FeeType>,
       clmm_positions: &mut Positions,
       clmm_reward_vault: &mut PoolRewardVault<RewardCoinType>,
       clmm_reward_index: u64,
       recipient: address,
       clock: &Clock,
       clmm_versioned: &Versioned,
       ctx: &mut TxContext
   ): Coin<RewardCoinType> {
       config::checked_package_version(global_config);
       assert!(strategy.status == 0, EStrategyLocked);
       assert!(strategy.clmm_pool_id == object::id(clmm_pool), ENotTheCorrespondingStrategy);
       [...]
   }
   ```

## Remediation
Implement the above-mentioned modifications to the code base.

© 2024 Otter Audits LLC. All Rights Reserved. 12/21

## Turbos Finance Audit 05 — General Findings

### Patch
Resolved in commit `971cfd9`.

© 2024 Otter Audits LLC. All Rights Reserved. 13/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

