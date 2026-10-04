---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17707
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jim Miller
  - Sam Moelius
  - Natalie Chin
---

## Vulnerability Title

Incorrect equality check in do_liquidate

### Overview


This bug report is about a data validation issue in the frame/oracle/src/lib.rs and composable/frame/vault/src/lib.rs files. The do_liquidate function, which is responsible for executing privileged operations of liquidating a strategy, is not correctly checking that the caller is a vault manager. As a result, an attacker could potentially change the amount of funds allocated to a vault strategy, reducing the yield available to vault liquidity providers.

To fix this issue, the != should be changed to == in the do_liquidate function to ensure that only vault managers can update strategies and allocations. Additionally, the expectations on vault managers should be documented, including those regarding the timing of strategy liquidations.

To prevent similar issues in the future, unit tests should be added to ensure that the code behaves as expected, including corner cases.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** frame/oracle/src/lib.rs

**Difficulty:** High

### Access Controls

**Type:** Access Controls  
**Target:** composable/frame/vault/src/lib.rs

## Description

The `do_liquidate` function, which executes the privileged operation of liquidating a strategy, should be callable only by vault managers. However, because of a typo in the function, it checks that the caller is *not* a vault manager. The incorrect equality check could enable an attacker to change the amount of funds allocated to a vault strategy by moving funds out of the strategy. While this would not result in a loss of funds, it would result in significantly less yield on the strategy.

```rust
impl <T: Config> Pallet<T> {
    /// liquidates strategy allocation
    pub fn do_liquidate(
        origin: OriginFor<T>,
        vault_id: &VaultIndex,
        strategy_account_id: &T::AccountId,
    ) -> DispatchResult {
        let from = ensure_signed(origin)?;
        let vault = Vaults::<T>::try_get(&vault_id).map_err(|_| Error::<T>::VaultDoesNotExist)?;
        ensure!(from != vault.manager, Error::<T>::OnlyManagerCanDoThisOperation);
        Allocations::<T>::remove(vault_id, strategy_account_id);
        Ok(())
    }
}
```

_Figure 7.1: frame/vault/src/lib.rs#L493-L506_

Additionally, if implemented correctly, the function would allow a vault manager to liquidate any strategy that he or she wanted to. As such, a rogue manager could pull funds out of a vault’s strategies, causing depositors to receive less yield than expected. This ability would introduce a management-centralization risk and should be more clearly documented at the very least.

## Exploit Scenario

Eve, an attacker, calls a function that uses `do_liquidate` as a helper function. This enables her to liquidate a strategy in a vault, significantly reducing the yield available to vault liquidity providers.

## Recommendations

**Short term:** In the `do_liquidate` function, change the `!=` to `==` to ensure that only vault managers can update strategies and allocations and that attackers cannot manipulate yield availability. Additionally, document the expectations on vault managers, including those regarding the timing of strategy liquidations.

**Long term:** Add unit tests, including for corner cases, to ensure that the code behaves as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Jim Miller, Sam Moelius, Natalie Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf

### Keywords for Search

`vulnerability`

