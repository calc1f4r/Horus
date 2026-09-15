---
# Core Classification
protocol: Pyth Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48823
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/governance.

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
  - Kevin Chow
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Unstable Use of Zero-Copy with non-POD Data

### Overview

See description below for full details.

### Original Finding Content

## PositionData Account Deserialization

The `PositionData` account is deserialized via Anchor’s zero-copy mechanism, which requires the structures serialized to have a stable layout, not contain padding, and accept any bit-pattern as a valid value in order to maintain correctness and avoid undefined behavior. 

However, `PositionData` contained Rust enums that were not annotated with a specific `repr`. This includes both the standard library’s `Option<T>` on elements of the positions array, `unlocking_start`, and the `TargetWithParameters` enum.

```rust
// src/state/positions.rs
pub struct Position {
    pub amount: u64,
    pub activation_epoch: u64,
    pub unlocking_start: Option<u64>,
    pub target_with_parameters: TargetWithParameters,
}

// src/state/positions.rs
pub enum TargetWithParameters {
    VOTING,
    STAKING {
        product: Pubkey,
        publisher: Publisher,
    },
}
```

Since these enums are not `repr(C)`, Rust makes absolutely no guarantees about the layout of these structures in memory—and by extension, their layout when serialized into the on-chain account. It is explicitly allowed for these layouts to change between compilations with the same compiler version, which makes them unsuitable for permanent storage. 

The presence of padding bytes in the structure due to the alignment of types used also leads to uninitialized bytes being exposed in the account data, and can potentially lead to undefined behavior.

Finally, there is no guarantee from Rust that the all-zeros initial state of the account is a valid value for the Rust structure. This could give rise to undefined behavior when initializing the account.

## Remediation

- Avoid zero-copying any structure that does not fulfill the conditions listed in the safety section of Anchor’s zero-copy docs.
- We recommend serializing and deserializing the individual `Positions` in a `PositionData` on-demand using a general-purpose serializer such as Borsh.

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: #164

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Governance |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/governance.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

