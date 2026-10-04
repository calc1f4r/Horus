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
solodit_id: 48091
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

Arbitrary Update Of Last Epoch Mixed

### Overview


The bug report describes a problem in the suifrens.move and capy_labs.move files, which are written in the programming language Rust. The issue is related to a function called suifren_update_last_epoch_mixed, which is used to prevent users from mixing their SuiFrens without following a countdown period. However, since the function is public, users can set an arbitrary value for last_epoch_mixed and bypass the checks in the capy_labs::mix function. This could potentially lead to security issues. The suggested solution is to change the visibility of the function to public(friend). The bug has been fixed in a recent patch.

### Original Finding Content

## Overview of `suifrens.move` and `capy_labs.move`

In `suifrens.move`, `suifren_update_last_epoch_mixed` sets the new epoch of mixed, which is intended to prevent users from frequently mixing their SuiFrens without following a countdown period. However, since the function is public, users may set an arbitrary value for `last_epoch_mixed` and bypass the checks in `capy_labs::mix`.

## Code Snippets

### `sources/suifrens.move` (RUST)

```rust
public fun suifren_update_last_epoch_mixed<T>(fren: &mut SuiFren<T>, epoch: u64) {
    fren.last_epoch_mixed = epoch;
}
```

### `sources/capy_labs.move` (RUST)

```rust
public fun mix<T>(
    app: &mut CapyLabsApp,
    sf1: &mut SuiFren<T>,
    sf2: &mut SuiFren<T>,
    clock: &Clock,
    birth_location: vector<u8>,
    ctx: &mut TxContext
): SuiFren<T> {
    [...]
    let last_epoch_mixed_1 = suifrens::suifren_last_epoch_mixed(sf1);
    let last_epoch_mixed_2 = suifrens::suifren_last_epoch_mixed(sf2);
    let epochs_passed_1 = current_epoch - last_epoch_mixed_1;
    let epochs_passed_2 = current_epoch - last_epoch_mixed_2;
    assert!(
        current_epoch == 0 ||
        (epochs_passed_1 >= app.cool_down_period &&
        epochs_passed_2 >= app.cool_down_period),
        EStillInCoolDownPeriod
    );
    [...]
}
```

## Remediation

- Set the visibility of the function to `public(friend)`.

## Patch

- Fixed in commit `b142be2`.

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

