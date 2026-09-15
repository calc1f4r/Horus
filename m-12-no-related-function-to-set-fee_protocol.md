---
# Core Classification
protocol: Superposition
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41530
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-superposition
source_link: https://code4rena.com/reports/2024-08-superposition
github_link: https://github.com/code-423n4/2024-08-superposition-findings/issues/8

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
finders_count: 7
finders:
  - oakcobalt
  - zhaojohnson
  - wasm\_it
  - shaflow2
  - DadeKuma
---

## Vulnerability Title

[M-12] No related function to set `fee_protocol`

### Overview


The report states that there is a bug in the code that prevents the protocol from accumulating fees. This is because there are no functions to set the `fee_protocol` rate, which is needed for the protocol to collect fees. The report suggests adding relevant functions to enable protocol fees and provides code snippets as a recommended mitigation step. The bug has been confirmed and commented on by the team and the severity is considered medium as it only affects potential earnings for the protocol.

### Original Finding Content


There are no related functions to set `fee_protocol`, which prevents the protocol from accumulating protocol fees.

### Proof of Concept

The pool contract defines the protocol fee rate `fee_protocol`, but there is no function to set it.

```rust
#[solidity_storage]
pub struct StoragePool {
    ...
    fee_protocol: StorageU8,
    fee_growth_global_0: StorageU256,
    fee_growth_global_1: StorageU256,
    protocol_fee_0: StorageU128,
    protocol_fee_1: StorageU128,
    ...
}
```

The contract also defines the `collect_protocol` and `collect_protocol_7540_F_A_9_F` functions to collect fees. However, since the protocol fee rate cannot be set, the protocol will never accumulate any protocol fees.

[pkg/seawater/src/lib.rs](https://github.com/code-423n4/2024-08-superposition/blob/4528c9d2dbe1550d2660dac903a8246076044905/pkg/seawater/src/lib.rs#L1132)

```rust
    #[allow(non_snake_case)]
    pub fn collect_protocol_7540_F_A_9_F(
        &mut self,
        pool: Address,
        amount_0: u128,
        amount_1: u128,
        recipient: Address,
    ) -> Result<(u128, u128), Revert> {
        ...
    }
```

[pkg/seawater/src/pool.rs](https://github.com/code-423n4/2024-08-superposition/blob/4528c9d2dbe1550d2660dac903a8246076044905/pkg/seawater/src/pool.rs#L538)

```rust
    pub fn collect_protocol(
        &mut self,
        amount_0: u128,
        amount_1: u128,
    ) -> Result<(u128, u128), Revert> {
        ...
    }
```

### Recommended Mitigation Steps

Add the relevant functions to enable protocol fees.

`pkg/seawater/src/pool.rs`:

```diff
+    pub fn set_fee_protocol(&mut self, new_fee_protocol: U256) {
+        self.fee_protocol.set(new_fee_protocol);
+    }
```

`pkg/seawater/src/lib.rs`:

```diff
+    #[allow(non_snake_case)]
+    pub fn set_fee_protocol(
+        &mut self,
+        pool: Address,
+        new_fee_protocol: U256,
+    ) -> Result<(), Revert> {
+        assert_eq_or!(
+            msg::sender(),
+            self.seawater_admin.get(),
+            Error::SeawaterAdminOnly
+        );
+
+        self.pools.setter(pool).set_fee_protocol(new_fee_protocol);
+
+        Ok(())
+    }
```

**[af-afk (Superposition) confirmed and commented](https://github.com/code-423n4/2024-08-superposition-findings/issues/8#issuecomment-2368238751):**
 > See [commit](https://github.com/fluidity-money/long.so/commit/7706459ed85400117bcad1aa00425240699fd2b6).

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-08-superposition-findings/issues/8#issuecomment-2369656227):**
 > The submission and its duplicates have correctly identified that there is no mechanism to set the protocol fee in the system, causing fees to never accumulate in the current implementation.
> 
> I believe a severity of medium is appropriate given that its only harm is prospective earnings for the protocol itself.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Superposition |
| Report Date | N/A |
| Finders | oakcobalt, zhaojohnson, wasm\_it, shaflow2, DadeKuma, peanuts, prapandey031 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-superposition
- **GitHub**: https://github.com/code-423n4/2024-08-superposition-findings/issues/8
- **Contest**: https://code4rena.com/reports/2024-08-superposition

### Keywords for Search

`vulnerability`

