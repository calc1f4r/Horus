---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48088
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

RPC Node Crashes Due To An Overflow

### Overview


The bug report discusses an issue in the code of a Rust application, specifically in the execution_engine.rs file. The function "check_total_coins" is supposed to calculate the total amount of coins from a given input, but it does not handle the case where the total amount exceeds the maximum value allowed. This results in incorrect values being returned and ultimately causing the application to crash. The suggested solution is to handle this scenario by returning an appropriate error message. The code has been fixed in a recent patch.

### Original Finding Content

## Code Issue Report: check_total_coins Function

In `execution_engine.rs`, `check_total_coins` calculates the total amount of coins from `&[Coin]`. However, this function does not handle the scenario where the total amount of coins exceeds the maximum `u64` value. In this case, the function returns incorrect values, crashing the application.

## Current Implementation

```rust
fn check_total_coins(coins: &[Coin], amounts: &[u64]) -> Result<(u64, u64), ExecutionError> {
    let total_amount: u64 = amounts.iter().sum();
    let total_coins = coins.iter().fold(0, |acc, c| acc + c.value());
    if total_amount > total_coins {
        return Err(ExecutionError::new_with_source(
            ExecutionErrorKind::InsufficientBalance,
            format!("Attempting to pay a total amount {:?} that is greater than the sum of input coin values {:?}", total_amount, total_coins),
        ));
    }
    Ok((total_coins, total_amount))
}
```

## Problem

The `check_total_coins` function does not handle cases where the total amount of coins exceeds the maximum `u64` value. This can lead to overflow, resulting in an application crash.

## Remediation

Handle the scenario where the total amount of coins exceeds `u64` by returning an appropriate error message.

### Updated Implementation

```diff
@@ -540,15 +540,21 @@
 fn check_total_coins(coins: &[Coin], amounts: &[u64]) -> Result<(u64, u64), ExecutionError> {
-    let total_amount: u64 = amounts.iter().sum();
-    let total_coins = coins.iter().fold(0, |acc, c| acc + c.value());
+    let total_amount: Option<u64> = amounts.iter().try_fold(0_u64, |acc, &a| acc.checked_add(a));
+    let total_coins = coins.iter().try_fold(0_u64, |acc, c| acc.checked_add(c.value()));
+    if total_amount.is_none() || total_coins.is_none() {
+        return Err(ExecutionError::new_with_source(
+            ExecutionErrorKind::Overflow,
+            "Value overflow",
+        ));
+    }
     if total_amount > total_coins {
         return Err(ExecutionError::new_with_source(
             ExecutionErrorKind::InsufficientBalance,
             format!("Attempting to pay a total amount {:?} that is greater than the sum of input coin values {:?}", total_amount, total_coins),
         ));
     }
-    Ok((total_coins, total_amount))
+    Ok((total_coins.unwrap(), total_amount.unwrap()))
 }
```

## Patch

Fixed in commit `7485c45`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

